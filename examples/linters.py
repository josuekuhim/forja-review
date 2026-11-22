"""Linha de base sem ML: ruff (regras de bug/segurança) e bandit nos mesmos diffs, no formato do `--json-out`.

Cada arquivo é reconstruído a partir do lado novo do diff (linhas fora dos hunks viram linhas em branco,
para a numeração bater). Só vale achado em linha adicionada, a mesma regra que a ancoragem aplica ao modelo.
Cada regra é traduzida para uma frase que cita a classe de bug que ela detecta; o `recall.py` decide com a
mesma checagem de palavra-chave usada para o modelo. Regra sem tradução fica só com o código (vira extra).

    uv run python examples/linters.py examples/pr-holdout.diff --ferramenta ruff --json-out r.json
    uv run python examples/recall.py examples/gabarito-holdout.json r.json
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from forja_review.diff import parse_unified

for _s in (sys.stdout, sys.stderr):
    _s.reconfigure(encoding="utf-8")

# Regras do ruff que procuram bug ou risco (não estilo). S101 (assert) fica de fora: não é bug em review.
RUFF_SELECT = "B,S,BLE,E722,SIM115,PLW"
RUFF_IGNORE = "S101"

# Frase por regra: diz o problema com as palavras que um revisor usaria. Sem a classe certa, não pontua.
FRASES = {
    "B006": "argumento padrão mutável compartilhado entre chamadas",
    "B008": "chamada em argumento padrão: avaliada uma vez e compartilhada",
    "S608": "query SQL montada com string: risco de injeção, use placeholder",
    "S113": "requests sem timeout",
    "S602": "subprocess com shell=True",
    "S604": "chamada com shell=True",
    "S605": "processo iniciado com shell",
    "S607": "subprocess com caminho parcial",
    "S603": "subprocess sem validar a entrada",
    "SIM115": "arquivo aberto sem with: não fecha",
    "E722": "except genérico engole o erro",
    "BLE001": "except Exception engole o erro",
    "S110": "except com pass engole o erro",
    "S112": "except com continue engole o erro",
    "B909": "lista modificada enquanto itera",
    "PLW2901": "variável do laço sobrescrita",
    # bandit
    "B105": "senha fixa no código",
    "B110": "except com pass engole o erro",
    "B112": "except com continue engole o erro",
    "B113": "requests sem timeout",
    "B602": "subprocess com shell=True",
    "B604": "chamada com shell=True",
    "B605": "processo iniciado com shell",
    "B607": "subprocess com caminho parcial",
    "B603": "subprocess sem validar a entrada",
    "B608": "query SQL montada com string: risco de injeção, use placeholder",
}


def reconstroi(diff: str, raiz: Path) -> dict[str, set[int]]:
    """Escreve o lado novo de cada arquivo em `raiz`; devolve as linhas comentáveis por caminho."""
    comentaveis = {}
    for f in parse_unified(diff):
        ok = f.commentable()
        if not ok:
            continue
        n = max(ok)
        linhas = [f.line_text(i) or "" for i in range(1, n + 1)]
        p = raiz / f.path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("\n".join(linhas) + "\n", encoding="utf-8")
        comentaveis[f.path] = ok
    return comentaveis


def roda_ruff(raiz: Path) -> list[tuple[str, int, str, str]]:
    r = subprocess.run(
        [
            shutil.which("ruff") or "ruff",
            "check",
            "--no-cache",
            "--preview",
            "--select",
            RUFF_SELECT,
            "--ignore",
            RUFF_IGNORE,
            "--output-format",
            "json",
            "--exit-zero",
            ".",
        ],
        cwd=raiz,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    )
    return [
        (
            Path(d["filename"]).resolve().relative_to(raiz.resolve()).as_posix(),
            d["location"]["row"],
            d["code"],
            d["message"],
        )
        for d in json.loads(r.stdout or "[]")
    ]


def roda_bandit(raiz: Path) -> list[tuple[str, int, str, str]]:
    r = subprocess.run(
        [shutil.which("bandit") or "bandit", "-r", ".", "-f", "json", "-q", "--skip", "B101"],
        cwd=raiz,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    out = json.loads(r.stdout or "{}")
    return [
        (Path(x["filename"]).as_posix().removeprefix("./"), x["line_number"], x["test_id"], x["issue_text"])
        for x in out.get("results", [])
    ]


ap = argparse.ArgumentParser()
ap.add_argument("diff")
ap.add_argument("--ferramenta", choices=["ruff", "bandit"], default="ruff")
ap.add_argument("--json-out", required=True)
a = ap.parse_args()

t0 = time.time()
with tempfile.TemporaryDirectory() as tmp:
    raiz = Path(tmp)
    comentaveis = reconstroi(Path(a.diff).read_text(encoding="utf-8"), raiz)
    achados = roda_ruff(raiz) if a.ferramenta == "ruff" else roda_bandit(raiz)
seg = time.time() - t0

comentarios, vistos = [], set()
sintaxe = sum(
    1 for x in achados if x[2] is None
)  # trecho fora dos hunks quebrou a reconstrução: artefato, não achado
for path, linha, code, msg in sorted(achados, key=lambda x: (x[0], x[1], x[2] or "")):
    if code is None:
        continue
    if linha not in comentaveis.get(path, set()) or (path, linha, code) in vistos:
        continue  # fora das linhas adicionadas: o modelo também não pode comentar ali
    vistos.add((path, linha, code))
    texto = f"[{code}] {FRASES[code]}" if code in FRASES else f"[{code}]"
    comentarios.append(
        {"path": path, "linha": linha, "severidade": "risco", "comentario": texto, "mensagem": msg}
    )

res = {
    "modelo": a.ferramenta + (f" ({RUFF_SELECT}; --preview)" if a.ferramenta == "ruff" else ""),
    "comentarios": comentarios,
    "arquivos": [{"path": p, "pulado": None, "resumo": "", "problemas": []} for p in comentaveis],
    "chamadas": 0,
    "tokens_entrada": 0,
    "tokens_saida": 0,
    "segundos_no_modelo": round(seg, 1),
    "erros_de_sintaxe_da_reconstrucao": sintaxe,
}
Path(a.json_out).write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
print(
    f"{a.ferramenta}: {len(comentarios)} achados em linhas adicionadas ({len(achados)} no total, {sintaxe} de sintaxe da reconstrução), {seg:.1f} s"
)
