"""Compara os comentários de `forja-review local --json-out` com o gabarito de bugs plantados.

Achou = há comentário no mesmo arquivo a até `tolerancia_linhas` da linha do bug. Comentários que
não batem com nenhum bug contam como "extras": nem todo extra é errado, mas é ruído a ler.

    uv run python examples/recall.py examples/gabarito-bugs-plantados.json resultado.json
"""

import json
import sys
import unicodedata

for _s in (sys.stdout, sys.stderr):
    _s.reconfigure(encoding="utf-8")


def norm(t: str) -> str:
    t = unicodedata.normalize("NFKD", t.casefold())
    return "".join(c for c in t if not unicodedata.combining(c))


with open(sys.argv[1], encoding="utf-8") as fh:
    gab = json.load(fh)
with open(sys.argv[2], encoding="utf-8") as fh:
    res = json.load(fh)
tol = gab["tolerancia_linhas"]
coms = res["comentarios"]


def perto(b, c):
    return c["path"] == b["arquivo"] and abs(c["linha"] - b["linha"]) <= tol


def bate(b, c):
    return perto(b, c) and any(norm(k) in norm(c["comentario"]) for k in b["palavras_chave"])


achados = [b for b in gab["bugs"] if any(bate(b, c) for c in coms)]
extras = [c for c in coms if not any(bate(b, c) for b in gab["bugs"])]
so_posicao = [b for b in gab["bugs"] if b not in achados and any(perto(b, c) for c in coms)]
print(f"modelo: {res['modelo']}")
print(f"bugs achados: {len(achados)}/{len(gab['bugs'])}  comentários: {len(coms)}  extras: {len(extras)}")
for b in gab["bugs"]:
    m = "x" if b in achados else ("~" if b in so_posicao else " ")
    print(f"  [{m}] {b['arquivo']}:{b['linha']}  {b['descricao']}")
print("  ([~] = comentou perto, mas sem falar do problema)")
for c in extras:
    print(f"  extra {c['path']}:{c['linha']} ({c['severidade']}) {c['comentario'][:90]}")
probs = [p for a in res["arquivos"] for p in a["problemas"]]
print(f"problemas de formato: {probs or 'nenhum'}")
print(
    f"{res['chamadas']} chamadas, {res['tokens_entrada']} tokens in, {res['tokens_saida']} out, {res['segundos_no_modelo']} s"
)
