"""Prompt da review. O diff vai com o número da linha nova à esquerda, para o modelo apontar linhas
que existem; a ancoragem (`parse.anchor`) descarta o que não bate.

Um arquivo grande vira vários pedaços (hunks inteiros, até `max_chars`), cada um numa chamada.
"""

from __future__ import annotations

from forja_review.diff import FileDiff, Hunk

SYSTEM = """Você é um revisor de código sênior. Revise o diff de UM arquivo de um pull request e responda em português do Brasil.

Procure PROBLEMAS nas linhas adicionadas (marcadas com +), por exemplo:
- entrada vazia, None, zero (lista vazia, divisão por zero, índice fora do intervalo, chave ausente);
- condição invertida, off-by-one, arredondamento errado;
- SQL ou comando montado com f-string/concatenação (injeção);
- arquivo, conexão ou lock aberto e não fechado;
- chamada de rede sem timeout ou sem checar o status;
- argumento padrão mutável, estado compartilhado, condição de corrida.

Regras:
- Cada comentário aponta um problema e diz como corrigir. NUNCA descreva o que o código faz ou o que foi adicionado: isso vai só no "resumo".
- Não comente estilo, nomes, docstrings ou formatação.
- Use o número que aparece à esquerda da linha.
- No máximo {max_comentarios} comentários. Se não houver problema real, devolva "comentarios": [].
- "severidade": "bug" (quebra), "risco" (quebra em algum caso) ou "sugestao" (melhoria clara).

Exemplo. Diff:
    3 + def remove_negativos(xs):
    4 +     for x in xs:
    5 +         if x < 0:
    6 +             xs.remove(x)
    7 +     return xs is []
Resposta:
{{"resumo": "Adiciona uma função que remove números negativos da lista.", "comentarios": [{{"linha": 6, "severidade": "bug", "comentario": "Remover itens da lista enquanto itera sobre ela pula elementos: [-1, -2] vira [-2]. Use uma nova lista: [x for x in xs if x >= 0]."}}, {{"linha": 7, "severidade": "bug", "comentario": "`is []` compara identidade e é sempre False. Para testar lista vazia use `not xs`; para devolver a lista, `return xs`."}}]}}

Responda APENAS com JSON, sem texto antes ou depois, neste formato:
{{"resumo": "o que a mudança faz, em 1 frase", "comentarios": [{{"linha": 12, "severidade": "bug", "comentario": "..."}}]}}"""

STATUS = {"added": "novo", "modified": "modificado", "renamed": "renomeado", "removed": "removido"}


def render_hunk(h: Hunk) -> list[str]:
    out = [h.header]
    for ln in h.lines:
        num = f"{ln.new:>5}" if ln.new is not None else "     "
        out.append(f"{num} {ln.kind} {ln.text}")
    return out


def chunks(f: FileDiff, max_chars: int) -> list[list[Hunk]]:
    """Agrupa hunks inteiros até `max_chars`. Um hunk sozinho maior que isso é cortado."""
    groups: list[list[Hunk]] = [[]]
    size = 0
    for h in f.hunks:
        hs = sum(len(x) + 1 for x in render_hunk(h))
        if hs > max_chars:
            # Corta o hunk gigante em pedaços de linhas, mantendo a numeração.
            part = Hunk(h.header + " (parte)")
            psize = 0
            for ln in h.lines:
                ls = len(ln.text) + 10
                if psize + ls > max_chars and part.lines:
                    groups.append([part])
                    part, psize = Hunk(h.header + " (parte)"), 0
                part.lines.append(ln)
                psize += ls
            groups.append([part])
            groups.append([])
            size = 0
            continue
        if size + hs > max_chars and groups[-1]:
            groups.append([])
            size = 0
        groups[-1].append(h)
        size += hs
    return [g for g in groups if g]


def messages(
    f: FileDiff, hunks: list[Hunk], *, max_comentarios: int, titulo: str | None = None
) -> list[dict[str, str]]:
    body = [f"Arquivo: {f.path} ({STATUS.get(f.status, f.status)})"]
    if f.old_path:
        body[0] += f", antes {f.old_path}"
    if titulo:
        body.insert(0, f"Pull request: {titulo}")
    body.append("")
    for h in hunks:
        body += render_hunk(h)
    return [
        {"role": "system", "content": SYSTEM.format(max_comentarios=max_comentarios)},
        {"role": "user", "content": "\n".join(body)},
    ]
