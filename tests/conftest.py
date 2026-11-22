"""GitHub e modelo falsos (httpx.MockTransport) para testar o fluxo inteiro sem rede."""

from __future__ import annotations

import json
import re

import httpx
import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

PATCH_MEDIA = """@@ -1,3 +1,5 @@
 def media(xs):
-    return sum(xs) / len(xs)
+    total = sum(xs)
+    n = len(xs)
+    return total / n


"""

PATCH_README = """@@ -1,2 +1,3 @@
 # Projeto
+Agora com média.

"""


def github_files() -> list[dict]:
    return [
        {"filename": "src/stats.py", "status": "modified", "patch": PATCH_MEDIA},
        {"filename": "README.md", "status": "modified", "patch": PATCH_README},
        {"filename": "uv.lock", "status": "modified", "patch": "@@ -1 +1 @@\n-a\n+b"},
        {"filename": "logo.png", "status": "added"},  # binário: sem patch
    ]


def llm_answer(user: str) -> str:
    if "src/stats.py" in user:
        return (
            "Claro! Aqui está:\n```json\n"
            + json.dumps(
                {
                    "resumo": "Separa a média em passos.",
                    "comentarios": [
                        {
                            "linha": 4,
                            "severidade": "bug",
                            "comentario": "Divisão por zero quando xs é vazia; trate n == 0.",
                        },
                        {"linha": 99, "severidade": "risco", "comentario": "Linha que não existe no diff."},
                    ],
                },
                ensure_ascii=False,
            )
            + "\n```"
        )
    return json.dumps({"resumo": "Atualiza o README.", "comentarios": []})


class FakeLLM:
    def __init__(self, fail: int = 0) -> None:
        self.calls: list[dict] = []
        self.fail = fail

    def __call__(self, req: httpx.Request) -> httpx.Response:
        body = json.loads(req.content)
        self.calls.append(body)
        if self.fail > 0:
            self.fail -= 1
            return httpx.Response(503, json={"error": "ocupado"})
        text = llm_answer(body["messages"][-1]["content"])
        return httpx.Response(
            200,
            json={
                "model": body["model"],
                "choices": [{"message": {"role": "assistant", "content": text}, "finish_reason": "stop"}],
                "usage": {"prompt_tokens": 100, "completion_tokens": 30},
            },
        )


class FakeGitHub:
    def __init__(self, head_sha: str = "abc1234def", reject_inline: bool = False) -> None:
        self.head_sha = head_sha
        self.reject_inline = reject_inline
        self.reviews: list[dict] = []
        self.token_requests = 0
        self.reactions: dict[int, list[dict]] = {}
        self.auth: list[str] = []

    def __call__(self, req: httpx.Request) -> httpx.Response:
        path, method = req.url.path, req.method
        self.auth.append(req.headers.get("Authorization", ""))
        if m := re.fullmatch(r"/app/installations/(\d+)/access_tokens", path):
            self.token_requests += 1
            return httpx.Response(201, json={"token": f"ghs_{m[1]}", "expires_at": "2099-01-01T00:00:00Z"})
        if re.fullmatch(r"/repos/[^/]+/[^/]+/installation", path):
            return httpx.Response(200, json={"id": 42})
        if re.fullmatch(r"/repos/[^/]+/[^/]+/pulls/\d+", path):
            return httpx.Response(
                200, json={"number": 7, "state": "open", "title": "Média", "head": {"sha": self.head_sha}}
            )
        if path.endswith("/files"):
            return httpx.Response(200, json=github_files())
        if path.endswith("/reviews") and method == "POST":
            body = json.loads(req.content)
            if self.reject_inline and body["comments"]:
                return httpx.Response(422, json={"message": "line must be part of the diff"})
            rid = 900 + len(self.reviews)
            self.reviews.append({"id": rid, **body})
            return httpx.Response(200, json={"id": rid})
        if m := re.fullmatch(r"/repos/[^/]+/[^/]+/pulls/\d+/reviews/(\d+)/comments", path):
            # Como o GitHub de verdade: este endpoint não traz a linha, só a posição no diff.
            rv = next(r for r in self.reviews if r["id"] == int(m[1]))
            return httpx.Response(
                200,
                json=[
                    {"id": 5000 + i, "path": c["path"], "line": None, "position": i + 1}
                    for i, c in enumerate(rv["comments"])
                ],
            )
        if re.fullmatch(r"/repos/[^/]+/[^/]+/pulls/\d+/comments", path):
            comentarios = [
                {"id": 5000 + i, "pull_request_review_id": rv["id"], "path": c["path"], "line": c["line"]}
                for rv in self.reviews
                for i, c in enumerate(rv["comments"])
            ]
            comentarios.append(
                {"id": 1, "pull_request_review_id": 1, "path": "outro.py", "line": 4}
            )  # de outra review
            return httpx.Response(200, json=comentarios)
        if m := re.fullmatch(r"/repos/[^/]+/[^/]+/pulls/comments/(\d+)/reactions", path):
            return httpx.Response(200, json=self.reactions.get(int(m[1]), []))
        return httpx.Response(404, json={"message": f"rota falsa não existe: {method} {path}"})


@pytest.fixture(scope="session")
def rsa_pem() -> tuple[str, object]:
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    pem = key.private_bytes(
        serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption()
    ).decode()
    return pem, key.public_key()
