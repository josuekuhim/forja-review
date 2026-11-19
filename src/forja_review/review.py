"""Orquestra a review de um conjunto de arquivos: filtra, divide, chama o modelo, ancora e mede."""

from __future__ import annotations

import asyncio
import json
from dataclasses import asdict, dataclass, field

from forja_contracts import telemetry as T
from opentelemetry import trace

from forja_review import prompt
from forja_review.diff import FileDiff, skip_reason
from forja_review.llm import LLM, Completion
from forja_review.parse import SEVERIDADES, Comment, parse


@dataclass
class ReviewConfig:
    max_comentarios_por_arquivo: int = 3
    max_chars_por_chamada: int = 8000
    max_arquivos: int = 15
    concorrencia: int = 1  # o forja-serve em CPU faz batching, mas 1 por vez dá latência previsível
    ignorar: list[str] = field(default_factory=list)  # globs extras
    capturar_conteudo: bool = True  # diff e resposta vão para o trace (desligue para repos privados)


@dataclass
class FileResult:
    path: str
    pulado: str | None = None
    resumo: str = ""
    comentarios: list[Comment] = field(default_factory=list)
    problemas: list[str] = field(default_factory=list)
    chamadas: list[Completion] = field(default_factory=list)


@dataclass
class Review:
    arquivos: list[FileResult]
    modelo: str
    trace_id: str = ""  # liga a review publicada ao trace (e o feedback, que chega depois)

    @property
    def comentarios(self) -> list[Comment]:
        return [c for f in self.arquivos for c in f.comentarios]

    @property
    def chamadas(self) -> list[Completion]:
        return [c for f in self.arquivos for c in f.chamadas]

    def contagem(self) -> dict[str, int]:
        return {s: sum(c.severidade == s for c in self.comentarios) for s in SEVERIDADES}


async def review_files(
    files: list[FileDiff],
    llm: LLM,
    cfg: ReviewConfig,
    tracer: trace.Tracer,
    *,
    repo: str = "local",
    pr: int | None = None,
    sha: str = "",
    titulo: str | None = None,
) -> Review:
    results = [FileResult(f.path, pulado=skip_reason(f, cfg.ignorar)) for f in files]
    todo = [(f, r) for f, r in zip(files, results, strict=True) if r.pulado is None]
    for _, r in todo[cfg.max_arquivos :]:
        r.pulado = f"limite de {cfg.max_arquivos} arquivos por review"
    todo = todo[: cfg.max_arquivos]
    sem = asyncio.Semaphore(cfg.concorrencia)
    base_attrs = {T.ATTR_REPO: repo, T.ATTR_SHA: sha, T.ATTR_MODEL: llm.cfg.model}
    if pr is not None:
        base_attrs[T.ATTR_PR] = pr

    async def one(f: FileDiff, r: FileResult) -> None:
        for i, hunks in enumerate(prompt.chunks(f, cfg.max_chars_por_chamada)):
            msgs = prompt.messages(f, hunks, max_comentarios=cfg.max_comentarios_por_arquivo, titulo=titulo)
            async with sem:
                with tracer.start_as_current_span(T.SPAN_LLM) as span:
                    span.set_attributes({**base_attrs, T.ATTR_FILE: f.path, T.ATTR_CHUNK: i})
                    if cfg.capturar_conteudo:
                        span.set_attribute(T.ATTR_INPUT_MESSAGES, json.dumps(msgs, ensure_ascii=False))
                    comp = await llm.chat(msgs)
                    p = parse(comp.text, f, max_comentarios=cfg.max_comentarios_por_arquivo)
                    if comp.finish_reason == "length":
                        # Cortada por max_tokens (modelo com raciocínio gasta o orçamento antes do JSON).
                        # Não é erro de formato: é configuração. Registra separado para não confundir.
                        p.problemas = ["resposta_cortada"] + [x for x in p.problemas if x != "json_invalido"]
                    span.set_attributes(
                        {
                            T.ATTR_INPUT_TOKENS: comp.prompt_tokens,
                            T.ATTR_OUTPUT_TOKENS: comp.completion_tokens,
                            T.ATTR_FINISH: [comp.finish_reason or ""],
                            T.ATTR_PROBLEMS: json.dumps(p.problemas),
                            T.ATTR_COMMENTS: json.dumps(
                                [
                                    {"arquivo": c.path, **{k: v for k, v in asdict(c).items() if k != "path"}}
                                    for c in p.comentarios
                                ],
                                ensure_ascii=False,
                            ),
                        }
                    )
                    if cfg.capturar_conteudo:
                        span.set_attribute(T.ATTR_OUTPUT_TEXT, comp.text)
            r.chamadas.append(comp)
            r.resumo = r.resumo or p.resumo
            r.comentarios += p.comentarios
            r.problemas += p.problemas
        if len(r.comentarios) > cfg.max_comentarios_por_arquivo:  # somando os pedaços
            ordem = {s: i for i, s in enumerate(SEVERIDADES)}
            r.comentarios = sorted(r.comentarios, key=lambda c: ordem[c.severidade])
            r.comentarios = sorted(r.comentarios[: cfg.max_comentarios_por_arquivo], key=lambda c: c.linha)

    with tracer.start_as_current_span(T.SPAN_REVIEW) as span:
        span.set_attributes({**base_attrs, "forja.files": len(files), "forja.files_reviewed": len(todo)})
        await asyncio.gather(*(one(f, r) for f, r in todo))
        span.set_attribute("forja.comments_total", sum(len(r.comentarios) for r in results))
        trace_id = format(span.get_span_context().trace_id, "032x")
    return Review(results, llm.cfg.model, trace_id)
