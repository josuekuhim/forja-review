"""Servidor do GitHub App: recebe webhooks, valida a assinatura, enfileira e responde rápido.

O GitHub dá 10 s para responder ao webhook e reentrega em caso de erro. Por isso a review **nunca**
roda no request: o endpoint só valida, enfileira (idempotente por commit) e devolve 202. O worker
roda no mesmo processo (lifespan) e consome a fila.
"""

from __future__ import annotations

import asyncio
import contextlib
import hashlib
import hmac
import json
import logging
from collections.abc import AsyncIterator
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from forja_review.store import Store
from forja_review.worker import Worker

log = logging.getLogger("forja_review")

ACOES = {"opened", "synchronize", "reopened", "ready_for_review"}


def verify_signature(secret: str, body: bytes, header: str | None) -> bool:
    if not header or not header.startswith("sha256="):
        return False
    expected = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, header.removeprefix("sha256="))


def triage(event: str, payload: dict[str, Any]) -> tuple[dict[str, Any] | None, str]:
    """Decide se o evento vira job. Retorna (job, motivo)."""
    if event == "ping":
        return None, "pong"
    if event != "pull_request":
        return None, f"evento {event} ignorado"
    action = payload.get("action")
    if action not in ACOES:
        return None, f"ação {action} ignorada"
    pr = payload["pull_request"]
    if pr.get("draft"):
        return None, "PR em rascunho"
    if (payload.get("sender") or {}).get("type") == "Bot":
        return None, "PR aberto por bot"
    inst = (payload.get("installation") or {}).get("id")
    if not inst:
        return None, "sem installation (o webhook não veio de um GitHub App)"
    return {
        "repo": payload["repository"]["full_name"],
        "pr": int(pr["number"]),
        "sha": pr["head"]["sha"],
        "installation_id": int(inst),
    }, "enfileirado"


def create_app(store: Store, webhook_secret: str, worker: Worker | None = None) -> FastAPI:
    @contextlib.asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        stop = asyncio.Event()
        task = asyncio.create_task(worker.run(stop)) if worker else None
        try:
            yield
        finally:
            stop.set()
            if task:
                worker.wake.set()
                await task

    app = FastAPI(title="forja-review", lifespan=lifespan)

    @app.get("/health")
    async def health() -> dict[str, Any]:
        return {"ok": True, "fila": store.pending()}

    @app.get("/stats")
    async def stats() -> dict[str, Any]:
        return store.stats()

    @app.post("/webhook")
    async def webhook(request: Request) -> JSONResponse:
        body = await request.body()
        if not verify_signature(webhook_secret, body, request.headers.get("X-Hub-Signature-256")):
            return JSONResponse({"erro": "assinatura inválida"}, status_code=401)
        event = request.headers.get("X-GitHub-Event", "")
        job, motivo = triage(event, json.loads(body or b"{}"))
        if job is None:
            return JSONResponse({"ok": True, "motivo": motivo})
        job_id, criado = store.enqueue(**job)
        if criado and worker:
            worker.wake.set()
        log.info("%s#%d@%s → job %d (%s)", job["repo"], job["pr"], job["sha"][:7], job_id, criado)
        return JSONResponse({"job": job_id, "novo": criado}, status_code=202)

    return app
