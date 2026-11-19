### 🔎 forja-review

**O que muda**

- `app/paginacao.py`: Adiciona a função `total_paginas` que calcula a quantidade de páginas para uma lista de itens.
- `app/relatorio.py`: Adiciona funções para calcular a média, percentual e maior venda de vendas.

**3 comentários nas linhas** (3 bugs).

<sub>Modelo `qwen2.5-coder-0.5b`. Reaja com 👍 ou 👎 nos comentários: é assim que medimos se a revisão ajuda. Revisão automática; pode errar.</sub>

--- app/relatorio.py:1
    def media(valores):
    🐛 **Bug**: A função `media` retorna 0.0 se a lista está vazia

--- app/relatorio.py:2
    return sum(valores) / len(valores)
    🐛 **Bug**: A função `percentual` retorna 0.0 se a parte ou total for zero

--- app/relatorio.py:3
    
    🐛 **Bug**: A função `maior_venda` retorna o primeiro item da lista de vendas com maior valor.

[3 chamadas, 2239 tokens de entrada, 446 de saída, 70.9 s no modelo]