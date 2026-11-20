"""Configuração por variáveis de ambiente (12-factor). Segredos nunca vão para o repositório."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from forja_review.llm import LLMConfig
from forja_review.review import ReviewConfig


def _env(name: str, default: str | None = None) -> str | None:
    return os.environ.get(f"FORJA_REVIEW_{name}", default)


@dataclass
class Settings:
    app_id: str | None = None
    private_key_path: str | None = None
    webhook_secret: str | None = None
    db: str = "forja-review.sqlite"
    traces: str | None = "traces/spans.jsonl"
    llm: LLMConfig = field(default_factory=LLMConfig)
    review: ReviewConfig = field(default_factory=ReviewConfig)

    @classmethod
    def from_env(cls) -> Settings:
        llm = LLMConfig(
            base_url=_env("LLM_BASE_URL", LLMConfig.base_url),
            model=_env("LLM_MODEL", LLMConfig.model),
            api_key_env=_env("LLM_API_KEY_ENV"),
            max_tokens=int(_env("LLM_MAX_TOKENS", str(LLMConfig.max_tokens))),
            timeout_s=float(_env("LLM_TIMEOUT_S", str(LLMConfig.timeout_s))),
            json_mode=_env("LLM_JSON_MODE", "0") == "1",
        )
        review = ReviewConfig(
            max_arquivos=int(_env("MAX_ARQUIVOS", str(ReviewConfig.max_arquivos))),
            concorrencia=int(_env("CONCORRENCIA", str(ReviewConfig.concorrencia))),
            capturar_conteudo=_env("CAPTURAR_CONTEUDO", "1") == "1",
            prompt=_env("PROMPT", ReviewConfig.prompt),
            ignorar=[g for g in (_env("IGNORAR") or "").split(",") if g],
        )
        return cls(
            app_id=_env("APP_ID"),
            private_key_path=_env("PRIVATE_KEY_PATH"),
            webhook_secret=_env("WEBHOOK_SECRET"),
            db=_env("DB", cls.db),
            traces=_env("TRACES", cls.traces) or None,
            llm=llm,
            review=review,
        )

    def private_key(self) -> str:
        if not self.private_key_path:
            raise RuntimeError("defina FORJA_REVIEW_PRIVATE_KEY_PATH (a chave .pem do GitHub App)")
        return Path(self.private_key_path).read_text(encoding="utf-8")

    def require_app(self) -> None:
        faltando = [
            n
            for n, v in (
                ("FORJA_REVIEW_APP_ID", self.app_id),
                ("FORJA_REVIEW_PRIVATE_KEY_PATH", self.private_key_path),
                ("FORJA_REVIEW_WEBHOOK_SECRET", self.webhook_secret),
            )
            if not v
        ]
        if faltando:
            raise RuntimeError("faltam variáveis: " + ", ".join(faltando) + " (veja .env.example)")
