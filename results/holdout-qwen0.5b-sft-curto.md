### 🔎 forja-review

**O que muda**

- `svc/cache.py`: Adiciona ao arquivo uma função que guarda o valor de um item na cache.
- `svc/pedidos.py`: Adiciona ao arquivo 2 funções: uma que calcula o desconto de um pedido; uma que busca a cotação de frete.

**2 comentários nas linhas** (2 bugs).

<sub>Modelo `review-sft`. Reaja com 👍 ou 👎 nos comentários: é assim que medimos se a revisão ajuda. Revisão automática; pode errar.</sub>

--- svc/cache.py:10
    valor, quando = self.dados[chave]
    🐛 **Bug**: Chave vaza: outra chamada devolve o valor de um que já acabou. Use índice e `None` como padrão.

--- svc/pedidos.py:11
    return total(itens) * 0.9
    🐛 **Bug**: O desconto já vale para o pedido atual: a mesma pessoa pode usar o cupom em um pedido antigo. Use `cupom=None` e tire o valor da sessão antes de ser guardado.

[2 chamadas, 567 tokens de entrada, 183 de saída, 80.3 s no modelo]