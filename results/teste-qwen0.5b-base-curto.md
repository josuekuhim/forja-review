### 🔎 forja-review

**O que muda**

- `jobs/invoices_jobs.py`: Adicionado um novo método para pesquisar invoices no banco de dados.
- `app/students_jobs.py`: Adicionado a função `medias_moveis` para calcular a média de uma janela de tamanho `k` de um array de valores.
- `backend/students_utils.py`: Adicionado um novo método `remover_invalidos` na classe `students_utils.py` para remover IDs negativos.
- `api/leituras_repo.py`: Adicionado um novo método para registrar uma visita em um usuário.
- `svc/faturas.py`: O arquivo `svc/faturas.py` foi modificado para incluir a função `responde` que envia uma solicitação de ping para um host específico e verifica se o número de retornos é 1.
- `jobs/alunos.py`: Adicionado um novo método `arredondar` para o arquivo `jobs/alunos.py`.
- `backend/orders_service.py`: Adicionado a função `arredondar` para arredondar valores de ponto flutuante para duas casas decimais.
- `src/servicos/consultas_repo.py`: Adicionado um novo método `responde` na classe `Consultas_repo.py` para verificar se um host está respondendo ao ping.
- `lib/readings_jobs.py`: Adicionado um novo método `precisa_reabastecer` à função `ler_readings_jobs.py`.
- `lib/readings.py`: O arquivo `lib/readings.py` foi modificado para incluir novas funções e métodos. Algumas alterações incluem a adição de novas funções para arredondar valores, obter o primeiro registro de um dispositivo específico, contar o status de cada registro, e adicionar uma nova função para contar os registros por status.
- `backend/faturas_utils.py`: Adicionado a função `mesclar` para combinar dados de um padrão e um dicionário extra.
- `src/servicos/alunos_jobs.py`: O arquivo `src/servicos/alunos_jobs.py` foi modificado para incluir novas funções e métodos. Essas mudanças incluem a adição de novas funções para contar o status de alunos e arredondar valores, além de adicionar novas funções para mesclar dados de padrao e extra.
- `api/viagens.py`: Adicionado a função `processar_pagamentos` para processar pagamentos de viagens.
- `svc/produtos.py`: Adicionado novas funções para registrar visitas e contar status de produtos.
- `core/partidas_service.py`: O arquivo `core/partidas_service.py` foi modificado para incluir novas funções e métodos para medias moveis e todos as partidas da base de dados.
- `api/leituras_utils.py`: Adicionado a função `arredondar` para arredondar valores de ponto flutuante para duas casas decimais.
- `backend/produtos_utils.py`: O arquivo `backend/produtos_utils.py` foi modificado para incluir funções para contar o status de produtos, listar todos os produtos, pesquisar produtos e processar pagamentos.
- `lib/pedidos.py`: O arquivo `lib/pedidos.py` foi modificado para incluir a função `arredondar` que arredonda valores de ponto flutuante para duas casas decimais.
- `api/alunos_service.py`: Alguns problemas encontrados na linha 3 do arquivo `api/alunos_service.py`:
- `core/tickets_utils.py`: Adicionado uma nova função `precisa_reabastecer` no arquivo `core/tickets_utils.py`. Esta função verifica se o estoque é maior que o mínimo permitido.
- `lib/consultas_repo.py`: Adicionado novas funções para registrar visitas e pesquisar consultas no banco de dados.
- `jobs/alunos_jobs.py`: Adicionado um novo método `registrar_visita` na função `alunos_jobs.py` para verificar se um usuário já está na lista de visitas.
- `lib/consultas_service.py`: Adicionado um novo método `cabecalho_paginacao` na classe `consultas_service.py`.
- `lib/orders_repo.py`: Adicionado um novo método `medias_moveis` na classe `OrdersRepo` que calcula a média de cada janela de tamanho `k` na lista de valores fornecida.
- `core/pedidos.py`: Alguns problemas encontrados no arquivo `core/pedidos.py` após a modificação.
- `api/consultas_service.py`: Adicionado o método `primeiro_de` para obter a primeira consulta de um médico específico.
- `backend/tickets_utils.py`: O arquivo `backend/tickets_utils.py` foi modificado para incluir novas funções e métodos que ajudam na análise de status de tickets e a busca de tickets por um responsável específico.
- `core/orders_utils.py`: Adicionado a função `media_por_customer_id` para calcular a média de valores por cliente.
- `backend/leituras.py`: Adicionado um novo método `todos_leituras` na classe `backend/leituras.py` para obter todas as leituras da base de dados.
- `api/orders_service.py`: O arquivo `api/orders_service.py` foi modificado para incluir a função `arredondar` que arredonda um valor para duas casas decimais.
- `svc/students_jobs.py`: Adicionado um novo método `registrar_student` para registrar um novo estudante.
- `lib/consultas_repo_2.py`: Adicionado uma nova função `media_por_medico_id` na função `consultas_repo_2.py` que calcula a média da duração de consultas por médico ID.
- `svc/alunos_jobs.py`: Adicionado um novo método `precisa_reabastecer` na função `alunos_jobs.py`.
- `svc/alunos.py`: Adicionado novas funções para calcular cabecalho de páginação e médias de movimentos, além de uma nova função para encontrar o primeiro aluno de uma turma específica.
- `app/partidas_repo.py`: Adicionado a função `mesclar` para combinar dois dicionários de parâmetros.
- `app/consultas_repo.py`: Adicionado um método para mesclar dois dicionários.
- `backend/alunos_service.py`: Adicionado a função `pesquisar_alunos` para buscar alunos pelo nome.
- `app/viagens_utils.py`: O arquivo `app/viagens_utils.py` foi modificado para incluir novas funções e métodos para buscar e listar viagens.
- `src/servicos/partidas_utils_2.py`: Adicionado um novo método `responde` na classe `partidas_utils_2.py` para verificar se uma host está respondendo ao ping.
- `backend/orders_service_2.py`: Adicionado um novo método para calcular a média de valores por cliente.
- `src/servicos/invoices_jobs.py`: Adicionado a função `precisa_reabastecer` para verificar se o estoque é menor que o mínimo.
- `core/orders_jobs.py`: Adicionado um novo método `precisa_reabastecer` à função `orders_jobs.py`.
- `backend/alunos_service_2.py`: Adicionado a função `arredondar` para arredondar valores de ponto flutuante para duas casas decimais.
- `backend/pedidos_utils.py`: Adicionado cabeçalho de páginação para o arquivo `pedidos_utils.py`.
- `svc/viagens.py`: Adicionado um novo método `remover_invalidos` na função `viagens.py` para remover IDs inválidos do conjunto de IDs.

**40 comentários nas linhas** (40 bugs).

<sub>Modelo `qwen-base`. Reaja com 👍 ou 👎 nos comentários: é assim que medimos se a revisão ajuda. Revisão automática; pode errar.</sub>

--- app/students_jobs.py:12
    def arredondar(valor):
    🐛 **Bug**: A função `medias_moveis` deve ser chamada com uma lista de valores e um número `k` que represente o tamanho da janela.

--- svc/faturas.py:12
    
    🐛 **Bug**: A função `responde` deve verificar se o número de retornos é 1 antes de retornar a mensagem '1 received'.

--- jobs/alunos.py:12
    return Decimal(str(valor)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    🐛 **Bug**: O método `arredondar` deve receber um valor como parâmetro e retornar um valor decimal com duas casas decimais.

--- backend/orders_service.py:12
    
    🐛 **Bug**: A função `arredondar` deve retornar um valor decimal, não uma string.

--- lib/readings.py:12
    
    🐛 **Bug**: A função `arredondar` foi adicionada para garantir que os valores são arredondados para duas casas decimais.

--- lib/readings.py:13
    def contar_status(readings):
    🐛 **Bug**: A função `primeiro_de` foi adicionada para obter o primeiro registro de um dispositivo específico.

--- lib/readings.py:14
    return Counter(x["status"] for x in readings)
    🐛 **Bug**: A função `contar_status` foi adicionada para contar o status de cada registro.

--- backend/faturas_utils.py:12
    novo = usuario not in vistos
    🐛 **Bug**: A função `mesclar` deve receber dois argumentos: um dicionário `padrao` e um dicionário `extra`. Além disso, deve verificar se `extra` não é `None` antes de adicionar seus valores aos dados baseados no padrão.

--- src/servicos/alunos_jobs.py:12
    
    🐛 **Bug**: A função `arredondar` foi adicionada para garantir que os valores arredondados sejam com duas casas decimais.

--- src/servicos/alunos_jobs.py:13
    def mesclar(padrao, extra):
    🐛 **Bug**: A função `mesclar` foi adicionada para mesclar dados de padrao e extra.

--- src/servicos/alunos_jobs.py:14
    saida = dict(padrao)
    🐛 **Bug**: A função `contar_status` foi adicionada para contar o status de alunos.

--- core/partidas_service.py:12
    saida = []
    🐛 **Bug**: A função `medias_moveis` foi adicionada para calcular a média de cada k-ésimo janela de valores da lista de valores.

--- core/partidas_service.py:13
    for i in range(len(valores) - k + 2):
    🐛 **Bug**: A função `todos_partidas` foi adicionada para obter todas as partidas da base de dados.

--- core/partidas_service.py:14
    janela = valores[i:i + k]
    🐛 **Bug**: A função `cabecalho_paginacao` foi adicionada para criar um cabeçalho para a página de resultados.

--- api/leituras_utils.py:12
    resp = requests.get(base_url, params={"page": pagina}, timeout=10)
    🐛 **Bug**: A função `arredondar` deve ser chamada com um valor de ponto flutuante.

--- backend/produtos_utils.py:12
    def todos_produtos(base_url):
    🐛 **Bug**: A função `contar_status` foi adicionada para contar o status de produtos.

--- backend/produtos_utils.py:13
    pagina, itens = 1, []
    🐛 **Bug**: A função `todos_produtos` foi adicionada para listar todos os produtos.

--- backend/produtos_utils.py:14
    while True:
    🐛 **Bug**: A função `pesquisar_produtos` foi adicionada para pesquisar produtos.

--- lib/pedidos.py:12
    return saida
    🐛 **Bug**: A função `arredondar` deve ser chamada antes de ser usada.

--- lib/pedidos.py:13
    
    🐛 **Bug**: A função `arredondar` deve ser chamada antes de ser usada.

--- lib/pedidos.py:14
    
    🐛 **Bug**: A função `arredondar` deve ser chamada antes de ser usada.

--- api/alunos_service.py:3
    
    🐛 **Bug**: A função `contar_status` está incorreta. A função deve retornar um objeto `Counter` com as contagens de status dos alunos.

--- lib/consultas_repo.py:12
    def medias_moveis(valores, k):
    🐛 **Bug**: A função `registrar_visita` não retorna o valor `novo` corretamente.

--- lib/consultas_repo.py:13
    saida = []
    🐛 **Bug**: A função `pesquisar_consultas` não retorna a lista de consultas corretamente.

--- lib/consultas_repo.py:14
    for i in range(len(valores) - k + 2):
    🐛 **Bug**: A função `medias_moveis` não retorna a lista de médias corretamente.

--- backend/tickets_utils.py:12
    
    🐛 **Bug**: A função `primeiro_de` foi adicionada para encontrar o primeiro ticket de um determinado responsável.

--- backend/tickets_utils.py:13
    
    🐛 **Bug**: A função `cabecalho_paginacao` foi adicionada para criar um cabeçalho de página com informações sobre o total de registros e a quantidade de páginas.

--- backend/tickets_utils.py:14
    def cabecalho_paginacao(total_registros, limite):
    🐛 **Bug**: A função `arredondar` foi adicionada para arredondar valores de acordo com a precisão decimal.

--- core/orders_utils.py:10
    if not selecionados:
    🐛 **Bug**: A função `media_por_customer_id` está retornando `None` quando o valor não for encontrado.

--- backend/leituras.py:12
    pagina += 1
    🐛 **Bug**: O método `todos_leituras` deve ser chamado com a URL base da API e deve retornar uma lista de leituras.

--- api/orders_service.py:3
    
    🐛 **Bug**: A função `arredondar` deve ser chamada antes de ser usada em qualquer parte do código.

--- api/orders_service.py:7
    
    🐛 **Bug**: A função `arredondar` deve ser chamada antes de ser usada em qualquer parte do código.

--- api/orders_service.py:10
    
    🐛 **Bug**: A função `arredondar` deve ser chamada antes de ser usada em qualquer parte do código.

--- svc/students_jobs.py:12
    return _contador["total"]
    🐛 **Bug**: O método `registrar_student` está sem chamar a função `_lock` para garantir que o contador seja atualizado corretamente.

--- svc/alunos.py:12
    saida.append(sum(janela) / k)
    🐛 **Bug**: A função `cabecalho_paginacao` deve retornar uma lista com os valores de `X-Total` e `X-Paginas`.

--- svc/alunos.py:13
    return saida
    🐛 **Bug**: A função `medias_moveis` deve retornar uma lista com os valores de `sum(janela) / k`.

--- svc/alunos.py:14
    
    🐛 **Bug**: A função `primeiro_de` deve retornar o primeiro aluno da turma que tem o valor especificado.

--- app/viagens_utils.py:12
    
    🐛 **Bug**: A função `primeiro_de` foi adicionada para garantir que o motorista_id seja encontrado antes de retornar o primeiro registro da lista.

--- app/viagens_utils.py:17
    resp.raise_for_status()
    🐛 **Bug**: A função `pesquisar_viagens` foi adicionada para garantir que a consulta seja feita com base na URL fornecida.

--- app/viagens_utils.py:22
    pagina += 1
    🐛 **Bug**: A função `todos_viagens` foi adicionada para garantir que a consulta seja feita com base na URL fornecida.

[60 chamadas, 16286 tokens de entrada, 10312 de saída, 5064.2 s no modelo]