"""Parser de diff unificado e regras de quais arquivos revisar.

Dois formatos de entrada:
- o `patch` de cada arquivo na API do GitHub (`GET /pulls/{n}/files`): só os hunks, sem cabeçalho;
- a saída de `git diff` (modo local): vários arquivos com cabeçalhos `diff --git`.

O que importa para a review é o número da linha **do lado novo** (RIGHT): é nele que a API de
review do GitHub aceita comentário, e só em linhas que aparecem num hunk.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from fnmatch import fnmatch
from typing import Any

HUNK_RE = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@(.*)$")


@dataclass
class Line:
    kind: str  # "+", "-" ou " "
    old: int | None
    new: int | None
    text: str


@dataclass
class Hunk:
    header: str
    lines: list[Line] = field(default_factory=list)


@dataclass
class FileDiff:
    path: str
    status: str = "modified"  # added, modified, removed, renamed
    hunks: list[Hunk] = field(default_factory=list)
    binary: bool = False
    old_path: str | None = None

    @property
    def added(self) -> int:
        return sum(ln.kind == "+" for h in self.hunks for ln in h.lines)

    @property
    def deleted(self) -> int:
        return sum(ln.kind == "-" for h in self.hunks for ln in h.lines)

    def added_lines(self) -> set[int]:
        return {ln.new for h in self.hunks for ln in h.lines if ln.kind == "+" and ln.new is not None}

    def commentable(self) -> set[int]:
        """Linhas do lado novo que aparecem no diff (adicionadas ou de contexto)."""
        return {ln.new for h in self.hunks for ln in h.lines if ln.new is not None}

    def line_text(self, n: int) -> str | None:
        for h in self.hunks:
            for ln in h.lines:
                if ln.new == n:
                    return ln.text
        return None

    @classmethod
    def from_github(cls, f: dict[str, Any]) -> FileDiff:
        patch = f.get("patch")
        return cls(
            path=f["filename"],
            status=f.get("status", "modified"),
            hunks=parse_patch(patch) if patch else [],
            # Sem `patch`: binário ou diff grande demais (a API omite). Nos dois casos não há o que ler.
            binary=patch is None,
            old_path=f.get("previous_filename"),
        )


def parse_patch(patch: str) -> list[Hunk]:
    hunks: list[Hunk] = []
    old = new = 0
    for raw in patch.splitlines():
        if m := HUNK_RE.match(raw):
            old, new = int(m[1]), int(m[3])
            hunks.append(Hunk(raw))
            continue
        if not hunks or raw.startswith("\\"):  # "\ No newline at end of file"
            continue
        kind, text = (raw[0], raw[1:]) if raw else (" ", "")
        if kind == "+":
            hunks[-1].lines.append(Line("+", None, new, text))
            new += 1
        elif kind == "-":
            hunks[-1].lines.append(Line("-", old, None, text))
            old += 1
        else:
            hunks[-1].lines.append(Line(" ", old, new, text))
            old += 1
            new += 1
    return hunks


def parse_unified(diff: str) -> list[FileDiff]:
    """Saída de `git diff` com vários arquivos."""
    files: list[FileDiff] = []
    body: list[str] = []

    def flush() -> None:
        if files:
            files[-1].hunks = parse_patch("\n".join(body))
        body.clear()

    for raw in diff.splitlines():
        if raw.startswith("diff --git "):
            flush()
            m = re.match(r"diff --git a/(.+?) b/(.+)$", raw)
            a, b = (m[1], m[2]) if m else ("", "")
            files.append(FileDiff(path=b, old_path=a if a != b else None))
            if a != b:
                files[-1].status = "renamed"
        elif not files:
            continue
        elif raw.startswith("new file mode"):
            files[-1].status = "added"
        elif raw.startswith("deleted file mode"):
            files[-1].status = "removed"
        elif raw.startswith("Binary files") or raw.startswith("GIT binary patch"):
            files[-1].binary = True
        elif raw.startswith(("--- ", "+++ ", "index ", "similarity ", "rename ", "old mode", "new mode")):
            continue
        else:
            body.append(raw)
    flush()
    return files


SKIP_GLOBS = [
    # lockfiles e gerados
    "*package-lock.json",
    "*yarn.lock",
    "*pnpm-lock.yaml",
    "*uv.lock",
    "*poetry.lock",
    "*Pipfile.lock",
    "*Cargo.lock",
    "*go.sum",
    "*composer.lock",
    "*.min.js",
    "*.min.css",
    "*.map",
    "*.snap",
    "*.ipynb",
    # pastas de terceiros/build
    "node_modules/*",
    "*/node_modules/*",
    "vendor/*",
    "dist/*",
    "build/*",
    # binários comuns que às vezes vêm com patch vazio
    "*.png",
    "*.jpg",
    "*.jpeg",
    "*.gif",
    "*.pdf",
    "*.ico",
    "*.woff*",
    "*.safetensors",
    "*.gguf",
]


def skip_reason(f: FileDiff, extra_globs: list[str] | None = None) -> str | None:
    """Por que não revisar este arquivo (ou None se é para revisar)."""
    if f.status == "removed":
        return "removido"
    if f.binary:
        return "binário ou diff grande demais"
    if not f.added:
        return "sem linhas adicionadas"
    for g in SKIP_GLOBS + (extra_globs or []):
        if fnmatch(f.path, g):
            return f"ignorado ({g})"
    return None
