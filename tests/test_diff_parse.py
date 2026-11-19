import pytest

from forja_review import prompt
from forja_review.diff import FileDiff, parse_patch, parse_unified, skip_reason
from forja_review.parse import extract_json, parse
from tests.conftest import PATCH_MEDIA

GIT_DIFF = """diff --git a/src/a.py b/src/a.py
index 111..222 100644
--- a/src/a.py
+++ b/src/a.py
@@ -10,4 +10,5 @@ def f():
     x = 1
-    y = 2
+    y = 3
+    z = 4
     return x
\\ No newline at end of file
diff --git a/img.png b/img.png
new file mode 100644
Binary files /dev/null and b/img.png differ
diff --git a/old.py b/new.py
similarity index 90%
rename from old.py
rename to new.py
--- a/old.py
+++ b/new.py
@@ -1 +1 @@
-a = 1
+a = 2
diff --git a/gone.py b/gone.py
deleted file mode 100644
--- a/gone.py
+++ /dev/null
@@ -1 +0,0 @@
-x
"""


def test_parse_patch_numera_lado_novo():
    (h,) = parse_patch(PATCH_MEDIA)
    f = FileDiff("s.py", hunks=[h])
    assert f.added_lines() == {2, 3, 4}
    assert f.commentable() == {1, 2, 3, 4, 5, 6}
    assert f.line_text(4) == "    return total / n"
    assert (f.added, f.deleted) == (3, 1)


def test_parse_unified_varios_arquivos():
    a, img, ren, gone = parse_unified(GIT_DIFF)
    assert a.path == "src/a.py" and a.added_lines() == {11, 12} and a.commentable() == {10, 11, 12, 13}
    assert img.binary and img.status == "added"
    assert ren.status == "renamed" and ren.old_path == "old.py" and ren.added_lines() == {1}
    assert gone.status == "removed"


@pytest.mark.parametrize(
    "f,motivo",
    [
        (FileDiff("uv.lock", hunks=parse_patch("@@ -1 +1 @@\n-a\n+b")), "ignorado (*uv.lock)"),
        (FileDiff("web/node_modules/x.js", hunks=parse_patch("@@ -1 +1 @@\n-a\n+b")), "ignorado"),
        (FileDiff("a.py", binary=True), "binário"),
        (FileDiff("a.py", status="removed"), "removido"),
        (FileDiff("a.py", hunks=parse_patch("@@ -1,2 +1 @@\n a\n-b")), "sem linhas adicionadas"),
        (FileDiff("a.py", hunks=parse_patch("@@ -1 +1 @@\n-a\n+b")), None),
    ],
)
def test_skip(f, motivo):
    r = skip_reason(f)
    assert (r is None) if motivo is None else motivo in r


def test_chunks_respeita_limite_e_corta_hunk_gigante():
    linhas = "\n".join(f"+linha {i} " + "x" * 50 for i in range(200))
    f = FileDiff("big.py", hunks=parse_patch("@@ -0,0 +1,200 @@\n" + linhas) + parse_patch(PATCH_MEDIA))
    cs = prompt.chunks(f, max_chars=2000)
    assert len(cs) > 3
    numeros = [ln.new for c in cs for h in c for ln in h.lines if ln.new is not None]
    assert numeros[:200] == list(range(1, 201))  # nada perdido, numeração preservada
    assert sum(len(x) for c in cs[:-1] for h in c for x in prompt.render_hunk(h)) > 0


def test_prompt_mostra_numero_da_linha():
    f = FileDiff("s.py", hunks=parse_patch(PATCH_MEDIA))
    user = prompt.messages(f, f.hunks, max_comentarios=3)[1]["content"]
    assert "    4 +     return total / n" in user
    assert "      -     return sum(xs) / len(xs)" in user


@pytest.mark.parametrize(
    "texto",
    [
        '{"resumo": "x", "comentarios": []}',
        'Aqui:\n```json\n{"resumo": "x", "comentarios": []}\n```\nFim.',
        'lixo antes {"resumo": "x", "comentarios": []} lixo depois',
    ],
)
def test_extract_json(texto):
    assert extract_json(texto) == {"resumo": "x", "comentarios": []}


def test_parse_ancora_e_registra_problemas():
    f = FileDiff("s.py", hunks=parse_patch(PATCH_MEDIA))
    texto = """{"resumo": "Separa a média.", "comentarios": [
        {"linha": 4, "severidade": "Crítico", "comentario": "Divisão por zero com lista vazia."},
        {"linha": 4, "severidade": "bug", "comentario": "Divisão por zero com lista vazia."},
        {"linha": 50, "severidade": "bug", "comentario": "Linha inventada pelo modelo."},
        {"linha": "três", "comentario": "Linha que não é número."},
        {"linha": 2, "severidade": "elogio", "comentario": "Nome total é claro e direto."},
        {"linha": 3, "comentario": "ok"},
        "texto solto"
    ]}"""
    p = parse(texto, f, max_comentarios=3)
    assert p.resumo == "Separa a média."
    assert [(c.linha, c.severidade) for c in p.comentarios] == [(2, "sugestao"), (4, "bug")]
    assert sorted(p.problemas) == sorted(
        ["duplicado", "linha_fora_do_diff", "linha_invalida", "comentario_vazio", "comentario_malformado"]
    )


def test_parse_json_invalido_e_excesso():
    f = FileDiff("s.py", hunks=parse_patch(PATCH_MEDIA))
    assert parse("não sei revisar isso", f).problemas == ["json_invalido"]
    muitos = [
        {"linha": n, "severidade": s, "comentario": f"comentário número {n} aqui"}
        for n, s in [(1, "sugestao"), (2, "risco"), (3, "bug"), (4, "sugestao")]
    ]
    p = parse('{"comentarios": ' + __import__("json").dumps(muitos) + "}", f, max_comentarios=2)
    assert [c.severidade for c in p.comentarios] == ["risco", "bug"]  # fica o mais grave, em ordem de linha
    assert "excesso_de_comentarios" in p.problemas


@pytest.mark.parametrize(
    "texto,descritivo",
    [
        ("Adicionou a função percentual para calcular o percentual.", True),
        ("A função foi adicionada para buscar usuários.", True),
        ("Corrigiu a consulta para buscar emails.", True),
        ("Agora a função exporta os emails para um arquivo.", True),
        ("Adicione um timeout: requests.get(url, timeout=10).", False),
        ("Divisão por zero quando total é 0; trate antes de dividir.", False),
        ("`requests.get` sem timeout pode travar o worker.", False),
    ],
)
def test_filtro_de_comentario_descritivo(texto, descritivo):
    f = FileDiff("s.py", hunks=parse_patch(PATCH_MEDIA))
    p = parse(__import__("json").dumps({"comentarios": [{"linha": 4, "comentario": texto}]}), f)
    assert (p.problemas == ["comentario_descritivo"]) is descritivo
    assert (len(p.comentarios) == 0) is descritivo
