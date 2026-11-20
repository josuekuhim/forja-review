### 🔎 forja-review

**O que muda**

- `backend/funcionarios_utils.py`: Adiciona funções para buscar funcionários por setor e verificar se o estoque é suficiente para um novo pedido.
- `jobs/alunos.py`: Adiciona funções para mesclar, arredondar e contar status de alunos.
- `backend/orders_service.py`: Adiciona funções para arredondar e verificar se um host está online.
- `src/servicos/partidas_utils.py`: Adiciona funções para arredondar e calcular a média de pontos por jogador.
- `svc/produtos.py`: Adiciona uma função para registrar visitas e contar o status de produtos.
- `app/readings_repo.py`: Adiciona funções para obter o primeiro registro de um dispositivo específico e para calcular a média de valores por dispositivo.
- `lib/pedidos.py`: Adiciona funções para arredondar e mesclar dados de pedidos.
- `api/consultas_service.py`: Adiciona uma função para obter a média de médicos movidos por um valor específico.
- `svc/alunos.py`: Adiciona funções para calcular cabecalho de páginação e médias de movimentos.
- `backend/consultas_utils.py`: Adiciona funções para calcular a média por médico e verificar se há necessidade de reabastecer.
- `backend/alunos_service_2.py`: Adiciona funções para arredondar e contar status de alunos.
- `svc/viagens.py`: Adiciona uma função para remover IDs negativos da lista.

**27 comentários nas linhas** (27 bugs).

<sub>Modelo `qwen-base`. Reaja com 👍 ou 👎 nos comentários: é assim que medimos se a revisão ajuda. Revisão automática; pode errar.</sub>

--- backend/funcionarios_utils.py:1
    import os
    🐛 **Bug**: Função `primeiro_de` deve retornar o primeiro funcionário com o setor especificado.

--- backend/funcionarios_utils.py:2
    import subprocess
    🐛 **Bug**: Função `precisa_reabastecer` deve verificar se o estoque é suficiente para um novo pedido.

--- backend/funcionarios_utils.py:3
    
    🐛 **Bug**: Função `responde` deve usar `subprocess.run` para executar o ping e verificar o retorno.

--- backend/orders_service.py:1
    import os
    🐛 **Bug**: Arredondar valores com duas casas decimais e verificar se o host está online.

--- backend/orders_service.py:11
    return "1 received" in saida
    🐛 **Bug**: O método `os.popen` é usado para executar o comando `ping` e obter a saída. A saída é convertida para uma string e usada como um dicionário para armazenar os resultados.

--- backend/orders_service.py:12
    
    🐛 **Bug**: A função `mesclar` recebe dois parâmetros: `padrao` e `extra`. O `padrao` é um dicionário que define o padrão para o resultado, e o `extra` é um dicionário que adiciona novos valores ao padrão.

--- src/servicos/partidas_utils.py:12
    return sum(selecionados) / len(selecionados)
    🐛 **Bug**: A função `arredondar` deve retornar um valor decimal com duas casas decimais.

--- src/servicos/partidas_utils.py:13
    
    🐛 **Bug**: A função `media_por_jogador_id` deve retornar um valor decimal.

--- src/servicos/partidas_utils.py:14
    
    🐛 **Bug**: A função `precisa_reabastecer` deve retornar um valor booleano.

--- svc/produtos.py:1
    from collections import Counter
    🐛 **Bug**: A função `registrar_visita` deve receber um usuário e um conjunto de visitas. A função `contar_status` deve retornar um dicionário com o status de cada produto.

--- svc/produtos.py:11
    return Counter(x["status"] for x in produtos)
    🐛 **Bug**: A função `contar_status` deve retornar um dicionário com o status de cada produto.

--- app/readings_repo.py:1
    def primeiro_de(readings, valor):
    🐛 **Bug**: O método `primeiro_de` deve retornar o primeiro registro da lista que matche o valor fornecido. O método `cabecalho_paginacao` deve retornar um objeto com as informações de paginção.

--- app/readings_repo.py:4
    
    🐛 **Bug**: O método `media_por_device_id` deve retornar a média dos valores de um dispositivo específico. O método `cabecalho_paginacao` deve retornar um objeto com as informações de paginção.

--- app/readings_repo.py:10
    
    🐛 **Bug**: O método `media_por_device_id` deve retornar a média dos valores de um dispositivo específico. O método `cabecalho_paginacao` deve retornar um objeto com as informações de paginção.

--- lib/pedidos.py:1
    from collections import Counter
    🐛 **Bug**: Função `arredondar` deve retornar um Decimal com duas casas decimais.

--- lib/pedidos.py:2
    from decimal import ROUND_HALF_UP, Decimal
    🐛 **Bug**: Função `mesclar` deve retornar um dicionário com os dados de pedidos.

--- lib/pedidos.py:3
    
    🐛 **Bug**: Função `contar_status` deve retornar um dicionário com o status de cada pedido.

--- svc/alunos.py:1
    def cabecalho_paginacao(total_registros, limite):
    🐛 **Bug**: Função `cabecalho_paginacao` deve retornar um dicionário com as informações de cabecalho.

--- svc/alunos.py:2
    return {
    🐛 **Bug**: Função `medias_moveis` deve retornar uma lista de médias de movimentos.

--- svc/alunos.py:3
    "X-Total": total_registros,
    🐛 **Bug**: Função `primeiro_de` deve retornar o primeiro aluno da turma especificada.

--- backend/consultas_utils.py:2
    selecionados = [x["duracao"] for x in consultas if x["medico_id"] == valor]
    🐛 **Bug**: Selecionar apenas os medicos com o mesmo ID.

--- backend/consultas_utils.py:3
    if not selecionados:
    🐛 **Bug**: Verificar se a lista está vazia antes de calcular a média.

--- backend/consultas_utils.py:4
    return None
    🐛 **Bug**: Revisão da função para garantir que o estoque não seja menor que o mínimo.

--- backend/alunos_service_2.py:1
    from collections import Counter
    🐛 **Bug**: Função `arredondar` usa `Decimal` para arredondar valores e `quantize` para formatar o resultado com duas casas decimais.

--- backend/alunos_service_2.py:2
    from decimal import ROUND_HALF_UP, Decimal
    🐛 **Bug**: Função `contar_status` usa `Counter` para contar o número de alunos em cada status.

--- svc/viagens.py:2
    for i in ids:
    🐛 **Bug**: Remove itens da lista enquanto itera sobre ela pula elementos: [-1, -2] vira [-2]. Use uma nova lista: [x for x in ids if x >= 0].

--- svc/viagens.py:3
    if i <= 0:
    🐛 **Bug**: `discard(i)` remove o elemento se ele existir na lista.

[60 chamadas, 44306 tokens de entrada, 22183 de saída, 14016.8 s no modelo]