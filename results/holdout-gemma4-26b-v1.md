### 🔎 forja-review

**O que muda**

- `svc/cache.py`: Implementa lógica de expiração invertida no método `get`.
- `svc/pedidos.py`: Adiciona funções para aplicar descontos em pedidos e consultar o valor do frete via API.

**4 comentários nas linhas** (2 bugs, 2 riscos).

<sub>Modelo `gemma-4-26b-a4b-q4`. Reaja com 👍 ou 👎 nos comentários: é assim que medimos se a revisão ajuda. Revisão automática; pode errar.</sub>

--- svc/cache.py:11
    if time.time() - quando < self.ttl:
    🐛 **Bug**: A lógica está invertida: o código deleta itens válidos (`< self.ttl`) e mantém itens expirados. Corrija a condição para `time.time() - quando >= self.ttl` e garanta que o método retorne `None` quando o item for removido por expiração.

--- svc/pedidos.py:8
    def aplicar_desconto(itens, cupom, descontos={}):
    🐛 **Bug**: Argumento padrão mutável (`descontos={}`) é compartilhado entre todas as chamadas da função. Use `descontos=None` e inicialize como `{}` dentro da função.

--- svc/pedidos.py:16
    r = requests.get(f"https://frete.exemplo.com/{cep}")
    ⚠️ **Risco**: A chamada de rede não possui um parâmetro `timeout`. Sem isso, a aplicação pode ficar travada indefinidamente caso o servidor não responda.

--- svc/pedidos.py:17
    return r.json()["valor"]
    ⚠️ **Risco**: A resposta da requisição não é validada. Use `r.raise_for_status()` para checar erros HTTP e verifique se a chave 'valor' existe no JSON para evitar `KeyError`.

[2 chamadas, 1470 tokens de entrada, 9131 de saída, 1341.0 s no modelo]