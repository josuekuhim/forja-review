### 🔎 forja-review

**O que muda**

- `app/paginacao.py`: Altera o cálculo do índice inicial da paginação e a contagem de páginas totais.
- `app/relatorio.py`: Adiciona funções para calcular percentual e identificar a maior venda em uma lista.
- `app/usuarios.py`: Adiciona funções para buscar usuários por nome e exportar e-mails para um arquivo.

**7 comentários nas linhas** (4 bugs, 3 riscos).

<sub>Modelo `gemma-4-26b-a4b-q4`. Reaja com 👍 ou 👎 nos comentários: é assim que medimos se a revisão ajuda. Revisão automática; pode errar.</sub>

--- app/paginacao.py:2
    inicio = numero * tamanho
    🐛 **Bug**: O cálculo `numero * tamanho` ignora os primeiros itens se a contagem de páginas começar em 1. O correto é `(numero - 1) * tamanho`.

--- app/paginacao.py:7
    return n_itens // tamanho
    🐛 **Bug**: A divisão inteira `//` arredonda para baixo, o que faz com que o último lote de itens seja ignorado se não for um múltiplo exato. Use `math.ceil(n_itens / tamanho)` ou `(n_itens + tamanho - 1) // tamanho`.

--- app/relatorio.py:6
    return round(parte / total * 100, 1)
    ⚠️ **Risco**: Divisão por zero se `total` for 0. Adicione uma verificação para evitar o erro.

--- app/relatorio.py:10
    maior = vendas[0]
    🐛 **Bug**: Lança `IndexError` se a lista `vendas` estiver vazia. Verifique se a lista não está vazia antes de acessar o índice 0.

--- app/usuarios.py:14
    cur = conn.execute(f"SELECT id, nome, email FROM usuarios WHERE nome = '{nome}'")
    🐛 **Bug**: Risco de SQL Injection. Use consultas parametrizadas em vez de f-strings para evitar ataques: `conn.execute('... WHERE nome = ?', (nome,))`.

--- app/usuarios.py:19
    conn = conectar(caminho_db)
    ⚠️ **Risco**: A conexão com o banco de dados é aberta mas não é fechada. Use o gerenciador de contexto `with conectar(caminho_db) as conn:` ou chame `conn.close()`.

--- app/usuarios.py:20
    arquivo = open(saida, "w")
    ⚠️ **Risco**: O arquivo é aberto mas não é fechado. Use `with open(saida, 'w') as arquivo:` para garantir o fechamento e o flush dos dados.

[3 chamadas, 2210 tokens de entrada, 5390 de saída, 748.9 s no modelo]