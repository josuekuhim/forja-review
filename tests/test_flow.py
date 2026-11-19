"""Fluxo inteiro: webhook → fila → worker → modelo → review publicada → feedback → traces."""

import hashlib
import hmac
import json

import httpx
import jwt
import pytest
from fastapi.testclient import TestClient
from forja_contracts import telemetry as T

from forja_review import telemetry
from forja_review.app import create_app, triage, verify_signature
from forja_review.diff import FileDiff
from forja_review.github import GitHubApp
from forja_review.llm import LLM, LLMConfig
from forja_review.review import ReviewConfig, review_files
from forja_review.store import Store
from forja_review.worker import Worker
from tests.conftest import FakeGitHub, FakeLLM, github_files

SECRET = "segredo-de-teste"


def pr_event(action="opened", sha="abc1234def", draft=False, sender="User", inst=42):
    return {
        "action": action,
        "pull_request": {"number": 7, "draft": draft, "head": {"sha": sha}},
        "repository": {"full_name": "eu/repo"},
        "sender": {"type": sender},
        "installation": {"id": inst} if inst else None,
    }


def signed(payload: dict, event: str = "pull_request", secret: str = SECRET):
    body = json.dumps(payload).encode()
    sig = "sha256=" + hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    return {"content": body, "headers": {"X-GitHub-Event": event, "X-Hub-Signature-256": sig}}


@pytest.fixture
def env(tmp_path, rsa_pem):
    gh_fake, llm_fake = FakeGitHub(), FakeLLM()
    store = Store(tmp_path / "db.sqlite")
    provider, tracer = telemetry.setup(tmp_path / "spans.jsonl")
    gh = GitHubApp(1, rsa_pem[0], transport=httpx.MockTransport(gh_fake))
    llm = LLM(LLMConfig(model="qwen-teste", max_retries=2), transport=httpx.MockTransport(llm_fake))
    w = Worker(store, gh, llm, ReviewConfig(), tracer, backoff_s=0)
    yield {
        "gh": gh_fake,
        "llm": llm_fake,
        "store": store,
        "worker": w,
        "spans": tmp_path / "spans.jsonl",
        "app": gh,
    }
    provider.shutdown()
    store.close()


def test_assinatura():
    body = b'{"a": 1}'
    good = "sha256=" + hmac.new(b"s", body, hashlib.sha256).hexdigest()
    assert verify_signature("s", body, good)
    assert not verify_signature("s", body + b" ", good)
    assert not verify_signature("outro", body, good)
    assert not verify_signature("s", body, None)


@pytest.mark.parametrize(
    "kw,motivo",
    [
        ({"draft": True}, "rascunho"),
        ({"sender": "Bot"}, "bot"),
        ({"action": "closed"}, "closed"),
        ({"inst": None}, "installation"),
    ],
)
def test_triage_ignora(kw, motivo):
    job, m = triage("pull_request", pr_event(**kw))
    assert job is None and motivo in m


def test_webhook_enfileira_uma_vez_por_commit(tmp_path):
    store = Store(tmp_path / "db.sqlite")
    c = TestClient(create_app(store, SECRET))
    r = c.post("/webhook", **signed(pr_event()))
    assert r.status_code == 202 and r.json() == {"job": 1, "novo": True}
    # GitHub reentrega e o `synchronize` do mesmo commit: não duplica
    assert c.post("/webhook", **signed(pr_event("synchronize"))).json() == {"job": 1, "novo": False}
    assert c.post("/webhook", **signed(pr_event("synchronize", sha="novo999"))).json()["job"] == 2
    assert c.post("/webhook", **signed(pr_event(), secret="errado")).status_code == 401
    assert c.post("/webhook", **signed({}, event="ping")).json()["motivo"] == "pong"
    assert c.get("/health").json() == {"ok": True, "fila": 2}


def test_jwt_e_cache_do_token(rsa_pem):
    pem, pub = rsa_pem
    fake = FakeGitHub()
    app = GitHubApp(123, pem, transport=httpx.MockTransport(fake))
    claims = jwt.decode(app.jwt(now=1_000_000), pub, algorithms=["RS256"], options={"verify_exp": False})
    assert claims == {"iat": 999_940, "exp": 1_000_540, "iss": "123"}

    import asyncio

    async def go():
        a = await app.installation_token(42)
        b = await app.installation_token(42)
        return a, b

    assert asyncio.run(go()) == ("ghs_42", "ghs_42")
    assert fake.token_requests == 1  # segunda vez veio do cache


async def test_worker_publica_review_e_registra(env):
    store, w, gh = env["store"], env["worker"], env["gh"]
    job_id, _ = store.enqueue("eu/repo", 7, "abc1234def", 42)
    assert await w.run_once()
    assert store.status(job_id) == "feito"

    (rv,) = gh.reviews
    assert rv["commit_id"] == "abc1234def" and rv["event"] == "COMMENT"
    # só o comentário ancorado na linha 4 sobrevive; o da linha 99 foi descartado
    assert rv["comments"] == [
        {
            "path": "src/stats.py",
            "line": 4,
            "side": "RIGHT",
            "body": "🐛 **Bug**: Divisão por zero quando xs é vazia; trate n == 0.",
        }
    ]
    assert "`src/stats.py`: Separa a média em passos." in rv["body"]
    assert "uv.lock" in rv["body"] and "logo.png" in rv["body"]  # listados como não revisados
    # 2 arquivos revisados (stats.py e README), lock e binário pulados
    assert len(env["llm"].calls) == 2
    assert store.stats()["prs_revisados"] == 1 and store.stats()["comentarios"] == 1
    assert any(a.startswith("Bearer ghs_42") for a in gh.auth)


async def test_fallback_sem_inline_quando_github_recusa_linha(env):
    env["gh"].reject_inline = True
    store, w = env["store"], env["worker"]
    job_id, _ = store.enqueue("eu/repo", 7, "abc1234def", 42)
    await w.run_once()
    assert store.status(job_id) == "feito"
    (rv,) = env["gh"].reviews
    assert rv["comments"] == [] and "`src/stats.py:4`" in rv["body"]


async def test_commit_antigo_e_ignorado(env):
    env["gh"].head_sha = "commit-mais-novo"
    job_id, _ = env["store"].enqueue("eu/repo", 7, "abc1234def", 42)
    await env["worker"].run_once()
    assert env["store"].status(job_id) == "ignorado" and env["gh"].reviews == []


async def test_modelo_fora_do_ar_volta_para_fila_e_depois_desiste(env):
    env["llm"].fail = 100
    store, w = env["store"], env["worker"]
    job_id, _ = store.enqueue("eu/repo", 7, "abc1234def", 42)
    for esperado in ("pendente", "pendente", "erro"):  # max_tentativas = 3
        await w.run_once()
        assert store.status(job_id) == esperado
    assert not await w.run_once()  # fila vazia


def test_recover_devolve_jobs_interrompidos(tmp_path):
    s = Store(tmp_path / "db.sqlite")
    jid, _ = s.enqueue("eu/repo", 1, "x", 1)
    assert s.claim().id == jid and s.claim() is None
    assert s.recover() == 1 and s.status(jid) == "pendente"


async def test_feedback_e_traces(env):
    store, w, gh = env["store"], env["worker"], env["gh"]
    store.enqueue("eu/repo", 7, "abc1234def", 42)
    await w.run_once()
    gh.reactions[5000] = [
        {"content": "+1", "user": {"type": "User"}},
        {"content": "+1", "user": {"type": "User"}},
        {"content": "-1", "user": {"type": "User"}},
        {"content": "+1", "user": {"type": "Bot"}},  # reação de bot não conta
    ]
    assert await w.sync_feedback() == 1
    assert await w.sync_feedback() == 0  # nada mudou: não re-emite
    st = store.stats()
    assert (st["comentarios_com_feedback"], st["comentarios_uteis"], st["taxa_util"]) == (1, 1, 1.0)

    calls, fb = T.load_interactions(env["spans"])
    assert {c.arquivo for c in calls} == {"src/stats.py", "README.md"}
    c = next(c for c in calls if c.arquivo == "src/stats.py")
    assert (c.repo, c.pr, c.modelo, c.input_tokens) == ("eu/repo", 7, "qwen-teste", 100)
    assert "linha_fora_do_diff" in c.problemas and c.comentarios[0].linha == 4
    assert c.mensagens[1]["content"].startswith("Pull request: Média")
    (f,) = fb
    assert (f.comment_id, f.up, f.down, f.arquivo, f.linha) == (5000, 2, 1, "src/stats.py", 4)
    assert f.review_trace_id == c.trace_id  # o feedback aponta para o trace da review


async def test_sem_captura_de_conteudo(tmp_path):
    provider, tracer = telemetry.setup(tmp_path / "s.jsonl")
    llm = LLM(LLMConfig(), transport=httpx.MockTransport(FakeLLM()))
    files = [FileDiff.from_github(f) for f in github_files()]
    await review_files(files, llm, ReviewConfig(capturar_conteudo=False), tracer)
    provider.shutdown()
    calls, _ = T.load_interactions(tmp_path / "s.jsonl")
    assert calls and all(c.mensagens == [] and c.saida == "" for c in calls)
    assert any(c.comentarios for c in calls)  # o resultado estruturado continua


async def test_resposta_cortada_nao_conta_como_json_invalido(tmp_path):
    def cortado(req: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={"choices": [{"message": {"content": ""}, "finish_reason": "length"}], "usage": {}},
        )

    provider, tracer = telemetry.setup(tmp_path / "s.jsonl")
    llm = LLM(LLMConfig(), transport=httpx.MockTransport(cortado))
    files = [FileDiff.from_github(f) for f in github_files()[:1]]
    rv = await review_files(files, llm, ReviewConfig(), tracer)
    provider.shutdown()
    assert rv.arquivos[0].problemas == ["resposta_cortada"]
