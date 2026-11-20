### 🔎 forja-review

**O que muda**

- `svc/cache.py`: Adiciona ao arquivo uma função que guarda um valor em cache.
- `svc/pedidos.py`: Adiciona ao arquivo 2 funções: uma que aplica desconto a itens de um pedido; uma que busca a cotação de um endereço.

**1 comentário nas linhas** (1 bug).

<sub>Modelo `review-dpo`. Reaja com 👍 ou 👎 nos comentários: é assim que medimos se a revisão ajuda. Revisão automática; pode errar.</sub>

--- svc/pedidos.py:10
    if cupom == "PROMO10":
    🐛 **Bug**: Se o cupom já estiver no dicionário, o descuento aumenta e o novo descuento sombra o antigo. Use `cupom in descontos` para verificar se o descuento já existe.

[2 chamadas, 567 tokens de entrada, 136 de saída, 43.5 s no modelo]