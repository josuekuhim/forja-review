"""Cliente mínimo de `/v1/chat/completions` (forja-serve, llama.cpp, vLLM ou API externa)."""

from __future__ import annotations

import asyncio
import os
import random
import time
from dataclasses import dataclass

import httpx

RETRYABLE = {408, 409, 429, 500, 502, 503, 504}


@dataclass
class Completion:
    text: str
    prompt_tokens: int
    completion_tokens: int
    latency_s: float
    finish_reason: str | None
    model: str


@dataclass
class LLMConfig:
    base_url: str = "http://127.0.0.1:8000/v1"
    model: str = "qwen2.5-coder-0.5b"
    api_key_env: str | None = None
    temperature: float = 0.0
    max_tokens: int = 512
    timeout_s: float = 600.0
    # `response_format: json_object`. O llama.cpp transforma isso em gramática (JSON garantido);
    # o forja-serve ignora o campo. Desligado por padrão para funcionar em qualquer servidor.
    json_mode: bool = False
    max_retries: int = 3


class LLM:
    def __init__(self, cfg: LLMConfig, transport: httpx.AsyncBaseTransport | None = None) -> None:
        self.cfg = cfg
        headers = {}
        if cfg.api_key_env:
            key = os.environ.get(cfg.api_key_env)
            if not key:
                raise RuntimeError(f"variável de ambiente {cfg.api_key_env} não definida")
            headers["Authorization"] = f"Bearer {key}"
        self.http = httpx.AsyncClient(
            base_url=cfg.base_url.rstrip("/") + "/",
            headers=headers,
            timeout=cfg.timeout_s,
            transport=transport,
        )

    async def aclose(self) -> None:
        await self.http.aclose()

    async def chat(self, messages: list[dict[str, str]]) -> Completion:
        body: dict = {
            "model": self.cfg.model,
            "messages": messages,
            "temperature": self.cfg.temperature,
            "max_tokens": self.cfg.max_tokens,
            "seed": 0,
        }
        if self.cfg.json_mode:
            body["response_format"] = {"type": "json_object"}
        last: Exception | None = None
        for attempt in range(self.cfg.max_retries + 1):
            t0 = time.perf_counter()
            try:
                r = await self.http.post("chat/completions", json=body)
            except (httpx.TimeoutException, httpx.TransportError) as e:
                last = e
            else:
                if r.status_code == 200:
                    d = r.json()
                    ch = d["choices"][0]
                    u = d.get("usage") or {}
                    return Completion(
                        text=ch["message"].get("content") or "",
                        prompt_tokens=int(u.get("prompt_tokens", 0)),
                        completion_tokens=int(u.get("completion_tokens", 0)),
                        latency_s=time.perf_counter() - t0,
                        finish_reason=ch.get("finish_reason"),
                        model=d.get("model") or self.cfg.model,
                    )
                if r.status_code not in RETRYABLE:
                    raise RuntimeError(f"LLM HTTP {r.status_code}: {r.text[:300]}")
                last = RuntimeError(f"LLM HTTP {r.status_code}")
            if attempt < self.cfg.max_retries:
                await asyncio.sleep(min(30.0, 2**attempt * (0.5 + random.random())))
        raise RuntimeError(
            f"LLM falhou após {self.cfg.max_retries + 1} tentativas: {type(last).__name__}: {last}"
        )
