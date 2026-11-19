"""Consome a fila: busca o PR, revisa, publica e registra. Também sincroniza o feedback (👍/👎)."""

from __future__ import annotations

import asyncio
import contextlib
import logging

from forja_contracts import telemetry as T
from opentelemetry import trace

from forja_review import render
from forja_review.diff import FileDiff
from forja_review.github import GitHubApp, GitHubError
from forja_review.llm import LLM
from forja_review.review import ReviewConfig, review_files
from forja_review.store import Job, Store

log = logging.getLogger("forja_review")


class Worker:
    def __init__(
        self,
        store: Store,
        gh: GitHubApp,
        llm: LLM,
        cfg: ReviewConfig,
        tracer: trace.Tracer,
        *,
        max_tentativas: int = 3,
        poll_s: float = 1.0,
        backoff_s: float = 30.0,
    ) -> None:
        self.store, self.gh, self.llm, self.cfg, self.tracer = store, gh, llm, cfg, tracer
        self.max_tentativas, self.poll_s, self.backoff_s = max_tentativas, poll_s, backoff_s
        self.wake = asyncio.Event()

    async def run(self, stop: asyncio.Event) -> None:
        n = self.store.recover()
        if n:
            log.warning("%d job(s) interrompidos voltaram para a fila", n)
        while not stop.is_set():
            if not await self.run_once():
                self.wake.clear()
                with contextlib.suppress(TimeoutError):
                    await asyncio.wait_for(self.wake.wait(), timeout=self.poll_s)

    async def run_once(self) -> bool:
        job = self.store.claim()
        if job is None:
            return False
        try:
            status = await self.process(job)
            self.store.finish(job.id, status)
            log.info("job %d %s#%d@%s: %s", job.id, job.repo, job.pr, job.sha[:7], status)
        except GitHubError as e:
            if e.status in (403, 404, 410, 422):  # sem permissão, PR sumiu: não adianta tentar de novo
                self.store.finish(job.id, "erro", str(e))
            else:
                self.store.fail(job, str(e), self.max_tentativas, self.backoff_s)
            log.exception("job %d falhou", job.id)
        except Exception as e:  # modelo fora do ar, timeout: tenta de novo com backoff
            self.store.fail(job, f"{type(e).__name__}: {e}", self.max_tentativas, self.backoff_s)
            log.exception("job %d falhou", job.id)
        return True

    async def process(self, job: Job) -> str:
        async with await self.gh.client(job.installation_id) as gh:
            pr = await gh.pull(job.repo, job.pr)
            if pr["head"]["sha"] != job.sha:
                return "ignorado"  # chegou commit novo; o job dele revisa o estado atual
            if pr.get("state") != "open":
                return "ignorado"
            files = [FileDiff.from_github(f) for f in await gh.pull_files(job.repo, job.pr)]
            rv = await review_files(
                files,
                self.llm,
                self.cfg,
                self.tracer,
                repo=job.repo,
                pr=job.pr,
                sha=job.sha,
                titulo=pr.get("title"),
            )
            comments = [
                {"path": c.path, "line": c.linha, "side": "RIGHT", "body": render.comment_body(c)}
                for c in rv.comentarios
            ]
            inline = True
            try:
                posted = await gh.create_review(
                    job.repo, job.pr, job.sha, render.review_body(rv, job.sha), comments
                )
            except GitHubError as e:
                # 422: alguma linha não está no diff segundo o GitHub (ex.: o diff mudou entre o
                # fetch e o post). Publica tudo no corpo para não perder a review.
                if e.status != 422 or not comments:
                    raise
                inline = False
                posted = await gh.create_review(
                    job.repo, job.pr, job.sha, render.review_body(rv, job.sha, inline=False), []
                )
            self.store.record_review(job.id, posted["id"], rv.trace_id, rv.modelo, len(comments), inline)
            if inline and comments:
                by_key = {(c.path, c.linha): c for c in rv.comentarios}
                for gc in await gh.review_comments(job.repo, job.pr, posted["id"]):
                    c = by_key.get((gc["path"], gc.get("line")))
                    if c:
                        self.store.record_comment(gc["id"], job.id, c.path, c.linha, c.severidade)
        return "feito"

    async def sync_feedback(self, max_age_days: float = 30) -> int:
        """Lê as reações dos comentários publicados. Reação não gera webhook: tem de ir buscar."""
        changed = 0
        rows = self.store.comments_to_sync(max_age_days)
        by_inst: dict[int, list[dict]] = {}
        for r in rows:
            by_inst.setdefault(r["installation_id"], []).append(r)
        for inst, items in by_inst.items():
            async with await self.gh.client(inst) as gh:
                for r in items:
                    reacts = await gh.comment_reactions(r["repo"], r["comment_id"])
                    humanos = [x for x in reacts if (x.get("user") or {}).get("type") != "Bot"]
                    up = sum(x["content"] == "+1" for x in humanos)
                    down = sum(x["content"] == "-1" for x in humanos)
                    if (up, down) == (r["up"], r["down"]):
                        continue
                    self.store.set_feedback(r["comment_id"], up, down)
                    changed += 1
                    with self.tracer.start_as_current_span(T.SPAN_FEEDBACK) as span:
                        span.set_attributes(
                            {
                                T.ATTR_REPO: r["repo"],
                                T.ATTR_PR: r["pr"],
                                T.ATTR_COMMENT_ID: r["comment_id"],
                                T.ATTR_FILE: r["path"],
                                T.ATTR_LINE: r["linha"],
                                T.ATTR_REVIEW_TRACE: r["trace_id"] or "",
                                T.ATTR_FEEDBACK_UP: up,
                                T.ATTR_FEEDBACK_DOWN: down,
                            }
                        )
        return changed
