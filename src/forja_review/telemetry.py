"""OpenTelemetry: spans de cada review e de cada chamada ao modelo.

Destino padrão: JSONL local (um span por linha), que o `forja-evals online` lê. Com
`OTEL_EXPORTER_OTLP_ENDPOINT` definido e o extra `otlp` instalado, também exporta por OTLP/HTTP
(Jaeger, Tempo, Honeycomb...). Nomes e atributos vêm do contrato `forja_contracts.telemetry`.
"""

from __future__ import annotations

import os
import threading
from collections.abc import Sequence
from pathlib import Path

from forja_contracts.telemetry import SERVICE_REVIEW
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import ReadableSpan, TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, SpanExporter, SpanExportResult


class JsonlSpanExporter(SpanExporter):
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

    def export(self, spans: Sequence[ReadableSpan]) -> SpanExportResult:
        with self._lock, self.path.open("a", encoding="utf-8", newline="\n") as f:
            for s in spans:
                f.write(s.to_json(indent=None) + "\n")
        return SpanExportResult.SUCCESS

    def shutdown(self) -> None:
        pass


def setup(jsonl_path: str | Path | None) -> tuple[TracerProvider, trace.Tracer]:
    """Provider próprio (não o global), para testes e CLI não se atrapalharem."""
    provider = TracerProvider(resource=Resource.create({"service.name": SERVICE_REVIEW}))
    if jsonl_path:
        # Simple (síncrono): o volume é baixo (algumas chamadas por PR) e nada se perde num crash.
        provider.add_span_processor(SimpleSpanProcessor(JsonlSpanExporter(jsonl_path)))
    if os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT"):
        try:
            from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
            from opentelemetry.sdk.trace.export import BatchSpanProcessor
        except ImportError as e:  # pragma: no cover
            raise RuntimeError("OTLP configurado mas o extra não está instalado: uv sync --extra otlp") from e
        provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))
    return provider, provider.get_tracer("forja_review")
