from __future__ import annotations

import asyncio
import json
import logging
import subprocess
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Annotated

import typer

from forja_review import render, telemetry
from forja_review.diff import parse_unified
from forja_review.llm import LLM
from forja_review.review import review_files
from forja_review.settings import Settings

app = typer.Typer(help="forja-review: revisão de pull requests em português.", no_args_is_help=True)

for _s in (sys.stdout, sys.stderr):  # Windows: stdout redirecionado vem em cp1252
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8")


def _settings(base_url: str | None, model: str | None, json_mode: bool | None) -> Settings:
    s = Settings.from_env()
    if base_url:
        s.llm.base_url = base_url
    if model:
        s.llm.model = model
    if json_mode is not None:
        s.llm.json_mode = json_mode
    return s


@app.command()
def local(
    rev: Annotated[str, typer.Argument(help="Intervalo do git diff (ex.: main...HEAD, HEAD~1)")] = "HEAD~1",
    repo_dir: Annotated[Path, typer.Option(help="Repositório git")] = Path("."),
    diff_file: Annotated[
        Path | None, typer.Option("--diff", help="Lê um diff de arquivo em vez do git")
    ] = None,
    base_url: Annotated[str | None, typer.Option(help="Endpoint OpenAI-compatível")] = None,
    model: Annotated[str | None, typer.Option(help="Nome do modelo")] = None,
    json_mode: Annotated[bool | None, typer.Option(help="Pede response_format json_object")] = None,
    out: Annotated[Path | None, typer.Option(help="Salva o resultado em Markdown")] = None,
    json_out: Annotated[Path | None, typer.Option(help="Salva comentários e métricas em JSON")] = None,
    prompt_estilo: Annotated[
        str | None, typer.Option("--prompt", help="completo (padrão) ou curto (modelo pós-treinado)")
    ] = None,
) -> None:
    """Revisa um diff local, sem GitHub. Útil para testar modelo e prompt."""
    s = _settings(base_url, model, json_mode)
    if prompt_estilo:
        s.review.prompt = prompt_estilo
    if diff_file:
        text = diff_file.read_text(encoding="utf-8")
    else:
        text = subprocess.run(
            ["git", "-C", str(repo_dir), "diff", "--no-color", "--no-ext-diff", rev],
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=True,
        ).stdout
    files = parse_unified(text)
    if not files:
        typer.echo("diff vazio")
        raise typer.Exit()
    provider, tracer = telemetry.setup(s.traces)

    async def go():
        llm = LLM(s.llm)
        try:
            return await review_files(files, llm, s.review, tracer, repo="local", sha=rev)
        finally:
            await llm.aclose()

    rv = asyncio.run(go())
    provider.shutdown()
    md = render.terminal(rv, files)
    typer.echo(md)
    if out:
        out.write_text(md, encoding="utf-8")
    if json_out:
        calls = rv.chamadas
        data = {
            "modelo": rv.modelo,
            "endpoint": s.llm.base_url,
            "comentarios": [asdict(c) for c in rv.comentarios],
            "arquivos": [
                {"path": f.path, "pulado": f.pulado, "resumo": f.resumo, "problemas": f.problemas}
                for f in rv.arquivos
            ],
            "chamadas": len(calls),
            "tokens_entrada": sum(c.prompt_tokens for c in calls),
            "tokens_saida": sum(c.completion_tokens for c in calls),
            "segundos_no_modelo": round(sum(c.latency_s for c in calls), 1),
        }
        json_out.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


@app.command()
def serve(
    host: str = "127.0.0.1",
    port: int = 8080,
    base_url: Annotated[str | None, typer.Option()] = None,
    model: Annotated[str | None, typer.Option()] = None,
) -> None:
    """Sobe o GitHub App (webhook + worker). Configuração em FORJA_REVIEW_* (veja .env.example)."""
    import uvicorn

    from forja_review.app import create_app
    from forja_review.github import GitHubApp
    from forja_review.store import Store
    from forja_review.worker import Worker

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    s = _settings(base_url, model, None)
    s.require_app()
    store = Store(s.db)
    _, tracer = telemetry.setup(s.traces)
    worker = Worker(store, GitHubApp(s.app_id, s.private_key()), LLM(s.llm), s.review, tracer)
    uvicorn.run(create_app(store, s.webhook_secret, worker), host=host, port=port)


@app.command()
def feedback(max_age_days: float = 30) -> None:
    """Busca 👍/👎 dos comentários publicados (reação não gera webhook). Rode num cron."""
    from forja_review.github import GitHubApp
    from forja_review.store import Store
    from forja_review.worker import Worker

    s = Settings.from_env()
    s.require_app()
    store = Store(s.db)
    provider, tracer = telemetry.setup(s.traces)
    w = Worker(store, GitHubApp(s.app_id, s.private_key()), LLM(s.llm), s.review, tracer)
    n = asyncio.run(w.sync_feedback(max_age_days))
    provider.shutdown()
    typer.echo(f"{n} comentário(s) com feedback novo")
    typer.echo(json.dumps(store.stats(), indent=2, ensure_ascii=False))


@app.command()
def stats() -> None:
    """X PRs revisados, Y% dos comentários marcados como úteis."""
    from forja_review.store import Store

    typer.echo(json.dumps(Store(Settings.from_env().db).stats(), indent=2, ensure_ascii=False))
