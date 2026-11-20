### 🔎 forja-review

**O que muda**

- `app/paginacao.py`: Adiciona ao arquivo uma função que calcula o número de páginas.
- `app/relatorio.py`: Adiciona ao arquivo 2 funções: uma que calcula o percentual de um item; uma que devolve o maior venda.
- `app/usuarios.py`: Adiciona ao arquivo 2 funções: uma que busca usuarios por nome; uma que exporta e-mails de todos os usuários.

**3 comentários nas linhas** (2 bugs, 1 risco).

<sub>Modelo `review-dpo`. Reaja com 👍 ou 👎 nos comentários: é assim que medimos se a revisão ajuda. Revisão automática; pode errar.</sub>

--- app/relatorio.py:10
    maior = vendas[0]
    🐛 **Bug**: `maior` é o mesmo em todos os itereiros: o primeiro vale o que `vendas[0]` vem antes, e então todos se sobraem. Itere sobre `vendas` numa nova lista: `maior = max(venda["valor"] for venda in vendas)`.

--- app/usuarios.py:14
    cur = conn.execute(f"SELECT id, nome, email FROM usuarios WHERE nome = '{nome}'")
    🐛 **Bug**: SQL injection: `nome` entra direto no texto da query. Passe como parâmetro (`?`) em vez de interpolar.

--- app/usuarios.py:20
    arquivo = open(saida, "w")
    ⚠️ **Risco**: Conexão `conn` não é fechada: o servidor fica ocupado por conexões não utilizadas. Feche com `closing(...)` ou `conn.close()` num `finally`.

[3 chamadas, 838 tokens de entrada, 305 de saída, 99.9 s no modelo]