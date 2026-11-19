"""Fila durável e registro das reviews em SQLite.

Por que não Redis: o volume é de alguns PRs por hora, e SQLite em WAL aguenta isso com folga,
sobrevive a restart e não exige mais um serviço. A fila tem as garantias que importam:
- **idempotência:** (repo, pr, sha) é único. O GitHub reentrega webhooks e o `synchronize` chega
  repetido; o mesmo commit nunca é revisado duas vezes;
- **at-least-once:** job `rodando` de um processo que morreu volta para `pendente` no próximo start;
- **retry com limite:** erro de infraestrutura tenta de novo até `max_tentativas`.
"""

from __future__ import annotations

import sqlite3
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

SCHEMA = """
CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY,
    repo TEXT NOT NULL,
    pr INTEGER NOT NULL,
    sha TEXT NOT NULL,
    installation_id INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'pendente',  -- pendente, rodando, feito, erro, ignorado
    tentativas INTEGER NOT NULL DEFAULT 0,
    proxima_em REAL NOT NULL DEFAULT 0,
    erro TEXT,
    criado_em REAL NOT NULL,
    atualizado_em REAL NOT NULL,
    UNIQUE (repo, pr, sha)
);
CREATE TABLE IF NOT EXISTS reviews (
    job_id INTEGER PRIMARY KEY REFERENCES jobs(id),
    review_id INTEGER,
    trace_id TEXT,
    modelo TEXT,
    n_comentarios INTEGER,
    inline INTEGER,
    criado_em REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS comentarios (
    comment_id INTEGER PRIMARY KEY,
    job_id INTEGER NOT NULL REFERENCES jobs(id),
    path TEXT NOT NULL,
    linha INTEGER NOT NULL,
    severidade TEXT NOT NULL,
    up INTEGER NOT NULL DEFAULT 0,
    down INTEGER NOT NULL DEFAULT 0,
    feedback_em REAL
);
"""


@dataclass
class Job:
    id: int
    repo: str
    pr: int
    sha: str
    installation_id: int
    tentativas: int


class Store:
    def __init__(self, path: str | Path = "forja-review.sqlite") -> None:
        self.db = sqlite3.connect(str(path), check_same_thread=False, isolation_level=None)
        self.db.row_factory = sqlite3.Row
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.executescript(SCHEMA)
        self._lock = threading.Lock()

    def close(self) -> None:
        self.db.close()

    def _x(self, sql: str, args: tuple = ()) -> sqlite3.Cursor:
        with self._lock:
            return self.db.execute(sql, args)

    # ------------------------------------------------------------------ fila

    def enqueue(self, repo: str, pr: int, sha: str, installation_id: int) -> tuple[int, bool]:
        """Retorna (id, criado). `criado=False`: esse commit já estava na fila ou já foi revisado."""
        now = time.time()
        with self._lock:
            cur = self.db.execute(
                "INSERT OR IGNORE INTO jobs (repo, pr, sha, installation_id, criado_em, atualizado_em)"
                " VALUES (?, ?, ?, ?, ?, ?)",
                (repo, pr, sha, installation_id, now, now),
            )
            if cur.rowcount:
                return int(cur.lastrowid), True
            row = self.db.execute(
                "SELECT id FROM jobs WHERE repo = ? AND pr = ? AND sha = ?", (repo, pr, sha)
            ).fetchone()
            return int(row["id"]), False

    def claim(self) -> Job | None:
        now = time.time()
        with self._lock:
            row = self.db.execute(
                "UPDATE jobs SET status = 'rodando', tentativas = tentativas + 1, atualizado_em = ?"
                " WHERE id = (SELECT id FROM jobs WHERE status = 'pendente' AND proxima_em <= ?"
                "             ORDER BY id LIMIT 1)"
                " RETURNING id, repo, pr, sha, installation_id, tentativas",
                (now, now),
            ).fetchone()
        return Job(**dict(row)) if row else None

    def finish(self, job_id: int, status: str, erro: str | None = None) -> None:
        self._x(
            "UPDATE jobs SET status = ?, erro = ?, atualizado_em = ? WHERE id = ?",
            (status, erro, time.time(), job_id),
        )

    def fail(self, job: Job, erro: str, max_tentativas: int, backoff_s: float = 30.0) -> str:
        """Erro de infraestrutura: volta para a fila com backoff, ou desiste."""
        if job.tentativas >= max_tentativas:
            self.finish(job.id, "erro", erro)
            return "erro"
        self._x(
            "UPDATE jobs SET status = 'pendente', erro = ?, proxima_em = ?, atualizado_em = ? WHERE id = ?",
            (erro, time.time() + backoff_s * 2 ** (job.tentativas - 1), time.time(), job.id),
        )
        return "pendente"

    def recover(self) -> int:
        """No start: jobs que ficaram `rodando` (processo morreu no meio) voltam para a fila."""
        return self._x(
            "UPDATE jobs SET status = 'pendente', atualizado_em = ? WHERE status = 'rodando'", (time.time(),)
        ).rowcount

    def status(self, job_id: int) -> str:
        return self._x("SELECT status FROM jobs WHERE id = ?", (job_id,)).fetchone()["status"]

    def pending(self) -> int:
        return self._x("SELECT COUNT(*) AS n FROM jobs WHERE status = 'pendente'").fetchone()["n"]

    # ------------------------------------------------------------------ reviews e feedback

    def record_review(
        self, job_id: int, review_id: int, trace_id: str, modelo: str, n: int, inline: bool
    ) -> None:
        self._x(
            "INSERT OR REPLACE INTO reviews VALUES (?, ?, ?, ?, ?, ?, ?)",
            (job_id, review_id, trace_id, modelo, n, int(inline), time.time()),
        )

    def record_comment(self, comment_id: int, job_id: int, path: str, linha: int, severidade: str) -> None:
        self._x(
            "INSERT OR IGNORE INTO comentarios (comment_id, job_id, path, linha, severidade)"
            " VALUES (?, ?, ?, ?, ?)",
            (comment_id, job_id, path, linha, severidade),
        )

    def comments_to_sync(self, max_age_days: float = 30) -> list[dict[str, Any]]:
        since = time.time() - max_age_days * 86400
        rows = self._x(
            "SELECT c.comment_id, c.path, c.linha, c.up, c.down, j.repo, j.pr, j.installation_id,"
            " r.trace_id FROM comentarios c JOIN jobs j ON j.id = c.job_id"
            " JOIN reviews r ON r.job_id = c.job_id WHERE r.criado_em >= ? ORDER BY j.installation_id",
            (since,),
        ).fetchall()
        return [dict(r) for r in rows]

    def set_feedback(self, comment_id: int, up: int, down: int) -> None:
        self._x(
            "UPDATE comentarios SET up = ?, down = ?, feedback_em = ? WHERE comment_id = ?",
            (up, down, time.time(), comment_id),
        )

    def stats(self) -> dict[str, Any]:
        q = lambda sql: self._x(sql).fetchone()[0]  # noqa: E731
        com_fb = q("SELECT COUNT(*) FROM comentarios WHERE up + down > 0")
        uteis = q("SELECT COUNT(*) FROM comentarios WHERE up > down")
        return {
            "prs_revisados": q(
                "SELECT COUNT(DISTINCT j.repo || '#' || j.pr) FROM reviews r JOIN jobs j ON j.id = r.job_id"
            ),
            "reviews": q("SELECT COUNT(*) FROM reviews"),
            "comentarios": q("SELECT COUNT(*) FROM comentarios"),
            "comentarios_com_feedback": com_fb,
            "comentarios_uteis": uteis,
            "taxa_util": (uteis / com_fb) if com_fb else None,
            "jobs": {r[0]: r[1] for r in self._x("SELECT status, COUNT(*) FROM jobs GROUP BY status")},
        }
