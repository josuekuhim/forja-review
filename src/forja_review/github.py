"""GitHub App: autenticação (JWT → token de instalação) e as poucas chamadas REST que a review usa.

Permissões mínimas do App: Pull requests (read & write), Contents (read), Metadata (read).
Evento: `pull_request`. Veja `github-app.yml`.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from datetime import datetime
from typing import Any

import httpx
import jwt

API = "https://api.github.com"
HEADERS = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}


class GitHubError(RuntimeError):
    def __init__(self, status: int, msg: str) -> None:
        super().__init__(f"GitHub HTTP {status}: {msg}")
        self.status = status


def _check(r: httpx.Response) -> Any:
    if r.status_code >= 400:
        raise GitHubError(r.status_code, r.text[:300])
    return r.json() if r.content else None


@dataclass
class _Token:
    value: str
    expires_at: float


class GitHubApp:
    def __init__(
        self,
        app_id: str | int,
        private_key_pem: str,
        api: str = API,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        self.app_id = str(app_id)
        self.key = private_key_pem
        self.api = api
        self.transport = transport
        self._tokens: dict[int, _Token] = {}
        self.http = httpx.AsyncClient(base_url=api, headers=HEADERS, timeout=30, transport=transport)

    async def aclose(self) -> None:
        await self.http.aclose()

    def jwt(self, now: float | None = None) -> str:
        now = int(now or time.time())
        # iat 60 s no passado tolera relógio adiantado; exp máximo do GitHub é 10 min.
        payload = {"iat": now - 60, "exp": now + 540, "iss": self.app_id}
        return jwt.encode(payload, self.key, algorithm="RS256")

    async def installation_token(self, installation_id: int) -> str:
        t = self._tokens.get(installation_id)
        if t and t.expires_at - 300 > time.time():  # renova com 5 min de folga
            return t.value
        r = await self.http.post(
            f"/app/installations/{installation_id}/access_tokens",
            headers={"Authorization": f"Bearer {self.jwt()}"},
        )
        d = _check(r)
        exp = datetime.fromisoformat(d["expires_at"]).timestamp()  # "2026-11-19T12:00:00Z"
        self._tokens[installation_id] = _Token(d["token"], exp)
        return d["token"]

    async def repo_installation(self, repo: str) -> int:
        """Id da instalação do App no repositório (para revisar sob demanda, sem webhook)."""
        r = await self.http.get(f"/repos/{repo}/installation", headers={"Authorization": f"Bearer {self.jwt()}"})
        return int(_check(r)["id"])

    async def client(self, installation_id: int) -> GitHubClient:
        return GitHubClient(await self.installation_token(installation_id), self.api, self.transport)


class GitHubClient:
    def __init__(self, token: str, api: str = API, transport: httpx.AsyncBaseTransport | None = None) -> None:
        self.http = httpx.AsyncClient(
            base_url=api,
            headers={**HEADERS, "Authorization": f"Bearer {token}"},
            timeout=30,
            transport=transport,
        )

    async def __aenter__(self) -> GitHubClient:
        return self

    async def __aexit__(self, *exc: object) -> None:
        await self.http.aclose()

    async def pull(self, repo: str, number: int) -> dict[str, Any]:
        return _check(await self.http.get(f"/repos/{repo}/pulls/{number}"))

    async def pull_files(self, repo: str, number: int, max_files: int = 300) -> list[dict[str, Any]]:
        files: list[dict[str, Any]] = []
        page = 1
        while len(files) < max_files:
            batch = _check(
                await self.http.get(
                    f"/repos/{repo}/pulls/{number}/files", params={"per_page": 100, "page": page}
                )
            )
            files += batch
            if len(batch) < 100:
                break
            page += 1
        return files[:max_files]

    async def create_review(
        self, repo: str, number: int, commit_id: str, body: str, comments: list[dict[str, Any]]
    ) -> dict[str, Any]:
        payload = {"commit_id": commit_id, "body": body, "event": "COMMENT", "comments": comments}
        return _check(await self.http.post(f"/repos/{repo}/pulls/{number}/reviews", json=payload))

    async def review_comments(self, repo: str, number: int, review_id: int) -> list[dict[str, Any]]:
        """Comentários inline de uma review, com `line`.

        Usa a lista de comentários do PR filtrada pela review: o endpoint
        `/pulls/{n}/reviews/{id}/comments` devolve `line: null` (só a `position` no diff), e sem a linha
        não dá para ligar o comentário publicado ao que o modelo gerou.
        """
        out: list[dict[str, Any]] = []
        page = 1
        while True:
            batch = _check(
                await self.http.get(
                    f"/repos/{repo}/pulls/{number}/comments", params={"per_page": 100, "page": page}
                )
            )
            out += [c for c in batch if c.get("pull_request_review_id") == review_id]
            if len(batch) < 100:
                return out
            page += 1

    async def comment_reactions(self, repo: str, comment_id: int) -> list[dict[str, Any]]:
        return _check(
            await self.http.get(
                f"/repos/{repo}/pulls/comments/{comment_id}/reactions", params={"per_page": 100}
            )
        )
