### 🔎 forja-review

**O que muda**

- `app/relatorio.py`: O arquivo `app/relatorio.py` foi modificado para incluir a função `percentual` que calcula o percentual de vendas.
- `app/usuarios.py`: O arquivo `app/usuarios.py` foi modificado para incluir novas funções para buscar usuários por ID e nome, além de exportar os emails de todos os usuários.

**5 comentários nas linhas** (5 bugs).

<sub>Modelo `qwen-base`. Reaja com 👍 ou 👎 nos comentários: é assim que medimos se a revisão ajuda. Revisão automática; pode errar.</sub>

--- app/relatorio.py:12
    if v["valor"] > maior["valor"]:
    🐛 **Bug**: A função `percentual` está incorreta. A função deve calcular o percentual de vendas, não o valor da venda.

--- app/relatorio.py:13
    maior = v
    🐛 **Bug**: A função `percentual` está incorreta. A função deve calcular o percentual de vendas, não o valor da venda.

--- app/relatorio.py:14
    return maior
    🐛 **Bug**: A função `percentual` está incorreta. A função deve calcular o percentual de vendas, não o valor da venda.

--- app/usuarios.py:8
    def buscar_usuario(conn, user_id):
    🐛 **Bug**: A função `buscar_usuario` foi adicionada para buscar um usuário pelo ID. No entanto, a função `buscar_por_nome` foi adicionada para buscar um usuário pelo nome. Ambas funções devem ser usadas corretamente.

--- app/usuarios.py:12
    
    🐛 **Bug**: A função `exportar_emails` foi adicionada para exportar os emails de todos os usuários. No entanto, a função `buscar_usuario` foi adicionada para buscar um usuário pelo ID. Ambas funções devem ser usadas corretamente.

[3 chamadas, 838 tokens de entrada, 933 de saída, 202.2 s no modelo]