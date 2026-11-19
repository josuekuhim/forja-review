"""Da resposta do modelo a comentários publicáveis.

Modelo pequeno erra o formato. Cada falha vira um `problema` (que vai para o trace) em vez de
derrubar a review: JSON inválido, comentário malformado, linha fora do diff, duplicata, excesso.
"""

from __future__ import annotations

import json
import re
import unicodedata
from dataclasses import dataclass, field

from forja_review.diff import FileDiff

SEVERIDADES = ("bug", "risco", "sugestao")
_ALIAS = {"sugestão": "sugestao", "erro": "bug", "critico": "bug", "crítico": "bug", "aviso": "risco"}
# Comentário que descreve a mudança em vez de apontar problema ("Adicionou a função X"). Modelo
# pequeno faz muito isso; no PR vira ruído. Imperativo ("Adicione um timeout") passa.
_DESCRITIVO = re.compile(
    r"^(?:(?:a|o|esta|essa) \w+ |foi )*"
    r"(adicionou|adiciona|adicionad[oa]|corrigiu|implementou|criou|definiu|incluiu|alterou|agora)\b"
)
_FENCE = re.compile(r"```(?:json)?\s*(.*?)```", re.S)


@dataclass
class Comment:
    path: str
    linha: int
    severidade: str
    comentario: str


@dataclass
class Parsed:
    resumo: str = ""
    comentarios: list[Comment] = field(default_factory=list)
    problemas: list[str] = field(default_factory=list)


def _norm(t: str) -> str:
    t = unicodedata.normalize("NFKD", t.casefold())
    return "".join(c for c in t if not unicodedata.combining(c)).lstrip("`*_ ")


def extract_json(text: str) -> dict | None:
    cands = [m.strip() for m in _FENCE.findall(text)]
    if (a := text.find("{")) >= 0 and (b := text.rfind("}")) > a:
        cands.append(text[a : b + 1])
    for c in cands:
        try:
            obj = json.loads(c)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict):
            return obj
        if isinstance(obj, list):  # só a lista de comentários
            return {"comentarios": obj}
    return None


def parse(text: str, f: FileDiff, *, max_comentarios: int = 3) -> Parsed:
    out = Parsed()
    obj = extract_json(text)
    if obj is None:
        out.problemas.append("json_invalido")
        return out
    out.resumo = str(obj.get("resumo") or "").strip()
    raw = obj.get("comentarios") or []
    if not isinstance(raw, list):
        out.problemas.append("comentarios_nao_lista")
        return out

    ok_lines = f.commentable()
    seen: set[tuple[int, str]] = set()
    for c in raw:
        if not isinstance(c, dict):
            out.problemas.append("comentario_malformado")
            continue
        try:
            linha = int(c.get("linha"))
        except (TypeError, ValueError):
            out.problemas.append("linha_invalida")
            continue
        texto = str(c.get("comentario") or "").strip()
        if len(texto) < 10:
            out.problemas.append("comentario_vazio")
            continue
        if _DESCRITIVO.match(_norm(texto)):
            out.problemas.append("comentario_descritivo")
            continue
        if linha not in ok_lines:
            out.problemas.append("linha_fora_do_diff")
            continue
        sev = str(c.get("severidade") or "sugestao").strip().lower()
        sev = _ALIAS.get(sev, sev)
        if sev not in SEVERIDADES:
            sev = "sugestao"
        key = (linha, texto.casefold())
        if key in seen:
            out.problemas.append("duplicado")
            continue
        seen.add(key)
        out.comentarios.append(Comment(f.path, linha, sev, texto))

    if len(out.comentarios) > max_comentarios:
        out.problemas.append("excesso_de_comentarios")
        ordem = {s: i for i, s in enumerate(SEVERIDADES)}
        out.comentarios = sorted(out.comentarios, key=lambda c: ordem[c.severidade])[:max_comentarios]
    out.comentarios.sort(key=lambda c: c.linha)
    return out
