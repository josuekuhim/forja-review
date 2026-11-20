### 🔎 forja-review

**O que muda**

- `app/paginacao.py`: Adiciona ao arquivo uma função que calcula o número de páginas.
- `app/relatorio.py`: Adiciona ao arquivo 2 funções: uma que calcula o percentual de um item; uma que devolve o maior venda.
- `app/usuarios.py`: Adiciona ao arquivo 2 funções: uma que busca usuarios por `nome`; uma que exporta e-mails de todos os usuários.

**3 comentários nas linhas** (3 bugs).

<sub>Modelo `review-sft`. Reaja com 👍 ou 👎 nos comentários: é assim que medimos se a revisão ajuda. Revisão automática; pode errar.</sub>

--- app/paginacao.py:7
    return n_itens // tamanho
    🐛 **Bug**: `n_itens // tamanho` trunca: com resto, a última página parcial some. Arredonde para cima (`math.ceil` ou `-(-a // b)`).

--- app/relatorio.py:10
    maior = vendas[0]
    🐛 **Bug**: `maior` é o mesmo no primeiro itereio e no último: um item vira `maior` em seguida. Filtre numa nova lista: `[v for v in vendas if v["valor"] > maior["valor"]]`.

--- app/usuarios.py:14
    cur = conn.execute(f"SELECT id, nome, email FROM usuarios WHERE nome = '{nome}'")
    🐛 **Bug**: SQL injection: `nome` entra direto no texto da query. Passe como parâmetro (`?`) em vez de interpolar.

[3 chamadas, 838 tokens de entrada, 290 de saída, 109.0 s no modelo]