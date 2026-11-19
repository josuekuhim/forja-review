"""Texto que aparece no GitHub (corpo da review e comentários) e no terminal (modo local)."""

from __future__ import annotations

from forja_review.diff import FileDiff
from forja_review.parse import Comment
from forja_review.review import Review

ROTULO = {"bug": "🐛 **Bug**", "risco": "⚠️ **Risco**", "sugestao": "💡 **Sugestão**"}
NOMES = {"bug": ("bug", "bugs"), "risco": ("risco", "riscos"), "sugestao": ("sugestão", "sugestões")}
MARCADOR = "<!-- forja-review -->"  # para achar as reviews do bot depois


def comment_body(c: Comment) -> str:
    return f"{ROTULO.get(c.severidade, ROTULO['sugestao'])}: {c.comentario}"


def review_body(rv: Review, sha: str = "", inline: bool = True) -> str:
    lines = [MARCADOR, "### 🔎 forja-review", ""]
    resumos = [(f.path, f.resumo) for f in rv.arquivos if f.pulado is None and f.resumo]
    if resumos:
        lines += ["**O que muda**", ""] + [f"- `{p}`: {r}" for p, r in resumos] + [""]
    n = len(rv.comentarios)
    cont = rv.contagem()
    if n:
        partes = [f"{v} {NOMES[k][v > 1]}" for k, v in cont.items() if v]
        onde = "nas linhas" if inline else "abaixo"
        lines.append(f"**{n} comentário{'s' if n > 1 else ''} {onde}** ({', '.join(partes)}).")
    else:
        lines.append("Não encontrei problemas nas linhas alteradas.")
    if not inline and n:
        lines += [""] + [f"- `{c.path}:{c.linha}` {comment_body(c)}" for c in rv.comentarios]
    pulados = [(f.path, f.pulado) for f in rv.arquivos if f.pulado]
    if pulados:
        lines += ["", "<details><summary>Arquivos não revisados</summary>", ""]
        lines += [f"- `{p}`: {m}" for p, m in pulados] + ["", "</details>"]
    commit = f" no commit `{sha[:7]}`" if sha else ""
    lines += [
        "",
        f"<sub>Modelo `{rv.modelo}`{commit}. Reaja com 👍 ou 👎 nos comentários: é assim que medimos se a "
        "revisão ajuda. Revisão automática; pode errar.</sub>",
    ]
    return "\n".join(lines)


def terminal(rv: Review, files: list[FileDiff]) -> str:
    by_path = {f.path: f for f in files}
    out = [review_body(rv).replace(MARCADOR + "\n", ""), ""]
    for c in rv.comentarios:
        code = (by_path[c.path].line_text(c.linha) or "").strip()
        out += [f"--- {c.path}:{c.linha}", f"    {code}", f"    {comment_body(c)}", ""]
    stats = rv.chamadas
    if stats:
        tin = sum(c.prompt_tokens for c in stats)
        tout = sum(c.completion_tokens for c in stats)
        lat = sum(c.latency_s for c in stats)
        out.append(
            f"[{len(stats)} chamadas, {tin} tokens de entrada, {tout} de saída, {lat:.1f} s no modelo]"
        )
    return "\n".join(out)
