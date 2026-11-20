### 🔎 forja-review

**O que muda**

- `jobs/invoices_jobs.py`: Adiciona uma função que pesquisa invoices por nome.
- `backend/funcionarios_utils.py`: Adiciona ao arquivo 2 funções: uma que verifica se o estoque precisa reabastecer; uma que testa connectivity to a server.
- `app/students_jobs.py`: Adiciona 2 funções: uma que calcula a média de `valores` moveis; uma que arredonda um número para baixo.
- `backend/students_utils.py`: Adiciona uma função que remove ids negativos.
- `api/leituras_repo.py`: Adiciona uma função que registra um visitante.
- `svc/faturas.py`: Adiciona ao arquivo 3 funções: uma que testa a conectividade de um fatura; uma que remove ids negativos; uma que devolve o primeiro registro com `empresa_id` igual a um valor.
- `jobs/alunos.py`: Adiciona 3 funções: uma que mescla dicionários; uma que arredonda um valor para duas casas; uma que conta os status de alunos.
- `backend/orders_service.py`: Adiciona 3 funções: uma que arredonda um valor para baixo; uma que verifica se o host está online; uma que mescla dicionários.
- `src/servicos/faturas_service.py`: Adiciona 3 funções: uma que devolve o fatura com o maior `total`; uma que mescla dicionários; uma que calcula a média de `total` por `empresa_id`.
- `src/servicos/consultas_repo.py`: Adiciona uma função que testa connectivity a um host.
- `src/servicos/partidas_utils.py`: Adiciona ao arquivo 2 funções: uma que calcula a média de `pontos` por `jogador_id`; uma que verifica se o estoque é menor que o mínimo.
- `lib/readings_jobs.py`: Adiciona uma função que verifica se o reading precisa ser reabastecido.
- `lib/readings.py`: Adiciona ao arquivo 2 funções: uma que devolve o reading com `device_id` igual a um parâmetro; uma que conta os status de readings.
- `backend/faturas_utils.py`: Adiciona 3 funções: uma que mescla dicionários; uma que registra um visitante; uma que lista todos os faturas.
- `src/servicos/alunos_jobs.py`: Adiciona ao arquivo 2 funções: uma que arredonda um valor para baixo; uma que mescla dicionários.
- `api/viagens.py`: Adiciona 2 funções: uma que processa pagamentos de viagens; uma que busca viagens na database.
- `src/servicos/viagens_jobs.py`: Adiciona 3 funções: uma que testa connectivity a um servidor; uma que calcula a média de `distancia`; uma que conta os status.
- `svc/produtos.py`: Adiciona 2 funções: uma que registra um visita de um produto; uma que conta os status de produtos.
- `core/partidas_service.py`: Adiciona ao arquivo 3 funções: uma que calcula a média de `moveis` de um conjunto de partidas; uma que lista todos os partidas; uma que calcula o percentual de itens no conjunto.
- `api/leituras_utils.py`: Adiciona 2 funções: uma que arredonda um valor para baixo; uma que lista todos os leituras.
- `backend/produtos_utils.py`: Adiciona ao arquivo 3 funções: uma que lista todos os produtos; uma que busca produtos na API; uma que processa a página de produtos.
- `app/readings_repo.py`: Adiciona ao arquivo 2 funções: uma que calcula o cabeçalho da página de readings; uma que calcula a média de `value` por `device_id`.
- `lib/pedidos.py`: Adiciona ao arquivo 2 funções: uma que mescla dicionários; uma que conta os status de pedidos.
- `api/alunos_service.py`: Adiciona ao arquivo uma função que devolve o primeiro aluno de um determinado `turma`.
- `lib/students_repo.py`: Adiciona ao arquivo 3 funções: uma que remove ids negativos; uma que conta os status de students; uma que registra um visitante.
- `core/tickets_utils.py`: Adiciona uma função que verifica se o ticket precisa reabastecer.
- `backend/students_utils_2.py`: Adiciona ao arquivo 3 funções: uma que calcula a média de `score` por classroom; uma que lista todos os students; uma que calcula a média de `moveis` de um conjunto de students.
- `lib/consultas_repo.py`: Adiciona 3 funções: uma que registra um visita; uma que busca consultas por nome; uma que calcula a média de um intervalo.
- `jobs/alunos_jobs.py`: Adiciona uma função que registra um visita de aluno.
- `lib/consultas_service.py`: Adiciona uma função que calcula o cabeçalho de uma página de consultas.
- `lib/orders_repo.py`: Adiciona uma função que calcula a média de `valores` moveis.
- `core/pedidos.py`: Adiciona ao arquivo uma função que conta os status de pedidos.
- `api/consultas_service.py`: Adiciona 2 funções: uma que devolve o consulta com `medico_id` primeiro; uma que calcula a média de `medico_id` de uma lista de consultas.
- `backend/tickets_utils.py`: Adiciona ao arquivo 2 funções: uma que devolve o ticket com `responsavel` igual a um valor; uma que arredonda um número para baixo.
- `core/orders_utils.py`: Adiciona 3 funções: uma que verifica se o estoque precisa reabastecer; uma que calcula a média de `amount` por `customer_id`; uma que arredonda um número.
- `backend/leituras.py`: Adiciona uma função que lista todos os leituras.
- `api/orders_service.py`: Adiciona ao arquivo 2 funções: uma que devolve o order com `customer_id` igual a um valor; uma que calcula a média de `amount` por `customer_id`.
- `svc/students_jobs.py`: Adiciona 2 funções: uma que registra um student; uma que lista todos os students.
- `lib/consultas_repo_2.py`: Adiciona uma função que calcula a média de `duracao` por `medico_id`.
- `svc/alunos_jobs.py`: Adiciona uma função que verifica se o aluno precisa reabastecer.
- `svc/alunos.py`: Adiciona 3 funções: uma que calcula o percentual de itens de uma lista; uma que calcula a média de um sublistão; uma que devolve o primeiro aluno de um lista que matches um filtro.
- `app/partidas_repo.py`: Adiciona 2 funções: uma que mescla dicionários; uma que devolve o primeiro item de `partidas` com `valor` (ou `None` no caso de empate).
- `backend/viagens.py`: Adiciona ao arquivo 2 funções: uma que processa pagamentos; uma que registra um visitante.
- `app/consultas_repo.py`: Adiciona uma função que mescla dicionários.
- `backend/alunos_service.py`: Adiciona 2 funções: uma que pesquisa alunos por nome; uma que remove ids inválidos.
- `app/viagens_utils.py`: Adiciona ao arquivo 2 funções: uma que pesquisa viagens na API; uma que lista todos os viagens.
- `app/alunos_repo.py`: Adiciona 2 funções: uma que verifica se o total é 0; uma que conta os status de alunos.
- `backend/consultas_utils.py`: Adiciona 2 funções: uma que calcula a média de `duracao` por `medico_id`; uma que verifica se o estoque precisa ser reabastecido.
- `src/servicos/partidas_utils_2.py`: Adiciona uma função que testa connectivity a um servidor.
- `app/faturas_jobs.py`: Adiciona ao arquivo 2 funções: uma que verifica se `saldo` é 0; uma que busca faturas na database.
- `backend/produtos_jobs.py`: Adiciona ao arquivo 2 funções: uma que verifica se o usuário já visitou um produto; uma que conta os status de produtos.
- `backend/orders_service_2.py`: Adiciona uma função que calcula a média de `amount` por `customer_id`.
- `src/servicos/invoices_jobs.py`: Adiciona 2 funções: uma que verifica se o invoice precisa reabastecer; uma que arredonda um valor para duas casas.
- `core/orders_jobs.py`: Adiciona uma função que verifica se o pedido precisa reabastecer.
- `app/funcionarios_jobs.py`: Adiciona uma função que calcula a média de `salario` por setor.
- `backend/alunos_service_2.py`: Adiciona 2 funções: uma que arredonda um valor para baixo; uma que conta os status de alunos.
- `backend/pedidos_utils.py`: Adiciona uma função que calcula o número de páginas.
- `src/servicos/viagens_repo.py`: Adiciona ao arquivo 3 funções: uma que registra um viagem; uma que calcula o número de páginas de viagens; uma que remove ids inválidos.
- `src/servicos/pedidos_service.py`: Adiciona ao arquivo uma função que verifica se o estoque precisa ser reabastecido.
- `svc/viagens.py`: Adiciona uma função que remove ids negativos.

**60 comentários nas linhas** (60 bugs).

<sub>Modelo `review-sft`. Reaja com 👍 ou 👎 nos comentários: é assim que medimos se a revisão ajuda. Revisão automática; pode errar.</sub>

--- jobs/invoices_jobs.py:2
    sql = "SELECT id FROM invoices WHERE nome LIKE '%{}%'".format(termo)
    🐛 **Bug**: SQL injection: `termo` entra direto no texto da query. Passe como parâmetro (`?`) em vez de interpolar.

--- backend/funcionarios_utils.py:10
    return estoque < minimo
    🐛 **Bug**: `<` testa identidade: strings iguais vindas do banco ou de JSON não são o mesmo objeto, e o resultado é `None`. Use `is None` ou `if funcionarios is None:`.

--- app/students_jobs.py:5
    saida = []
    🐛 **Bug**: `k` pode ser 0 e dividir por zero. O `k` deve ser 1 ou maior.

--- api/leituras_repo.py:2
    vistos = set() if vistos is None else vistos
    🐛 **Bug**: `vistos is None` compara identidade, não valor: pode dar False para uma nova lista criada no `if` e para os existentes. Use `if vistos is not None`.

--- svc/faturas.py:10
    saida = os.popen(f"ping -c 1 {host}").read()
    🐛 **Bug**: O comando `os.popen` sem `encoding` usa a codificação padrão do sistema (não UTF-8), e os erros aparecem com letras minúsculas. Passe `encoding='utf-8'`.

--- svc/faturas.py:19
    return next((x for x in faturas if x["empresa_id"] == valor), None)
    🐛 **Bug**: `None` no `next` quando a lista é vazia: um registro de fatura vem depois de um inválido. Itere sobre `faturas[1:]`, tratando a lista vazia antes.

--- jobs/alunos.py:12
    return Decimal(str(valor)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    🐛 **Bug**: `Decimal("0.01")` converte para zero e trunca: com 2 casas, "0,10" vale 0, e com 3, "0,01" vale 0.01. Passe acentos (e espaço) para `Decimal("0.01")`.

--- backend/orders_service.py:10
    saida = os.popen(f"ping -c 1 {host}").read()
    🐛 **Bug**: `os.popen` sem nome de arquivo cria uma nova janela: um processo com `ping` no nome aparece como `ping` e some quando o usuário fecha. Use `subprocess.check_output` (ou `subprocess.run` com `stdout=subprocess.PIPE` e `stderr=subprocess.PIPE` para ver o erro).

--- backend/orders_service.py:15
    saida = dict(padrao)
    🐛 **Bug**: O dicionário `extra` vem de parâmetro: um `None` no campo que não vem é ignorado. Passe uma tupla de padrões (`()`, `{}` ou `{key: default}`) e o valor padrão se der `None` é decidido automaticamente.

--- src/servicos/faturas_service.py:12
    selecionados = [x["total"] for x in faturas if x["empresa_id"] == valor]
    🐛 **Bug**: `valor` pode ser `None` e o filtro vira um iterador vazio: `x["empresa_id"] == valor` é `False` para todos. Use `if x["empresa_id"] is None`.

--- src/servicos/consultas_repo.py:5
    saida = os.popen(f"ping -c 1 {host}").read()
    🐛 **Bug**: O comando `os.popen` sem `encoding` usa a codificação padrão do sistema (não especificada), e os caracteres não são lidos corretamente. Passe `encoding='utf-8'`.

--- src/servicos/partidas_utils.py:16
    return estoque > minimo
    🐛 **Bug**: `estoque > minimo` compara identidade com uma lista nova e é sempre False. Para ver se há espaço, compare `len(estoque)` com `minimo`.

--- lib/readings.py:10
    return next((x for x in readings if x["device_id"] == valor), None)
    🐛 **Bug**: `next` de uma sequência vazia levanta `StopIteration`. Se `readings` pode vir vazia, trate antes ou use `itertools.find_first_true`.

--- lib/readings.py:14
    return Counter(x["status"] for x in readings)
    🐛 **Bug**: `Counter` de tuplas vaza: dois `device_id` iguais no mesmo reading entram num `Counter` vazio. Use `Counter(dict(readings))`.

--- backend/faturas_utils.py:11
    vistos = set() if vistos is None else vistos
    🐛 **Bug**: `not in` testa identidade: para o valor `None`, o teste diz `False` e o bloco executa; para o índice `None` o teste diz `True`, e o código executa sempre.

--- backend/faturas_utils.py:18
    pagina, itens = 1, []
    🐛 **Bug**: `timeout=10` defaulta a conexão para sempre, e se o servidor não responder, um erro vaza. Passe `timeout=None` (nenhum) e trate a resposta como se não houvesse timeout.

--- src/servicos/alunos_jobs.py:10
    return Decimal(str(valor)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    🐛 **Bug**: O nome diz "arredondar", mas o retorno usa `Decimal` e o input numérico usa `float` (ou `int` em Python 3). O que vale para um número float vale para o outro, e então o resultado é errado. Use `round` ou `min(max(...), ...)`.

--- api/viagens.py:2
    for x in viagens:
    🐛 **Bug**: A exceção `Exception` é capturada em todas as funções, incluindo essa que processa pagamentos. Pelo menos uma função trate a exceção.

--- api/viagens.py:10
    sql = "SELECT id FROM viagens WHERE nome LIKE ?"
    🐛 **Bug**: O `%` formata a string antes de chegar no driver, então os valores entram crus no SQL (injeção e erro com aspas). Passe a tupla como segundo argumento: `conn.execute(sql, (termo,))`.

--- src/servicos/viagens_jobs.py:11
    selecionados = [x["distancia"] for x in viagens if x["motorista_id"] == valor]
    🐛 **Bug**: `valor` entra num comando com `ping`: injeção de comando. Passe uma lista de argumentos e tire o `valor` antes.

--- svc/produtos.py:5
    novo = usuario not in vistos
    🐛 **Bug**: `not in` testa identidade: para o primeiro ocorrência, o índice é `None`; para o último, o elemento é `None` e o teste dão `False`. Use `if usuario not in vistos:`.

--- core/partidas_service.py:12
    saida = []
    🐛 **Bug**: `k` pode ser 0 e ser ignorado: uma sequência de 0s é igual a sua soma. Se `k` for 0, o `update` desloca os itens: os que vem depois não ficam. Use `if k == 0: continue`.

--- api/leituras_utils.py:10
    pagina, itens = 1, []
    🐛 **Bug**: A condição está invertida: itere somente uma vez e vá para o próximo item a cada chamada. Use `while resp.status_code == 200: ...`.

--- backend/produtos_utils.py:13
    pagina, itens = 1, []
    🐛 **Bug**: A condição está invertida: devolve a página quando há mais que um item. Deve ser `if not dados: return []`.

--- app/readings_repo.py:13
    selecionados = [x["value"] for x in readings if x["device_id"] == valor]
    🐛 **Bug**: `valor` entra num filtro: os itens que não correspondem devem ser ignorados. Se `valor` vem de um input, trate antes ou use `is` em vez de `==`.

--- lib/pedidos.py:10
    saida = dict(padrao)
    🐛 **Bug**: `padrao` é avaliado uma vez: todas as chaves de `extra` são o mesmo e o que se apaga também apaga para todas. Use `dict.fromkeys(extra.keys(), padrao)`.

--- api/alunos_service.py:9
    return next((x for x in alunos if x["turma"] == valor), None)
    🐛 **Bug**: `next` de uma sequência vazia levanta `StopIteration`. Se `alunos` pode vir vazia, trate antes ou use `if not alunos:`.

--- lib/students_repo.py:16
    return Counter(x["status"] for x in students)
    🐛 **Bug**: `Counter` de `students` vira vazio com cada `id`: dois id iguais no mesmo conjunto vêm com `None` no счетe, e ocorrência de um é verificada multiplemente. Monte uma nova coleção: `Counter([x["status"] for x in students])`.

--- backend/students_utils_2.py:11
    selecionados = [x["score"] for x in students if x["classroom"] == valor]
    🐛 **Bug**: `valor` pode ser `None` e o filtro vem vazia: quando há uma lista vazia e `filter` itera sobre iteração, levanta `StopIteration` e o iterador fica pendurado. Troque `valor is not None` por `valor is not None`.

--- backend/students_utils_2.py:29
    saida = []
    🐛 **Bug**: `k` pode ser maior que o tamanho da lista, e o resultado é `None` (a média de um conjunto vazia é `None`). Trate o caso vazio antes: `if not valores: return []`.

--- lib/consultas_repo.py:8
    sql = "SELECT id FROM consultas WHERE nome LIKE '%{}%'".format(termo)
    🐛 **Bug**: `%` formata a string antes de chegar no driver, então os valores entram crus no SQL (injeção e erro com aspas). Passe a tupla como segundo argumento: `conn.execute("SELECT * FROM ...", (termo,))`.

--- jobs/alunos_jobs.py:2
    vistos = set() if vistos is None else vistos
    🐛 **Bug**: `vistos is None` compara identidade, não valor: pode ser `None` e o teste devolve `False`. Use `if vistos is not None`.

--- lib/consultas_service.py:4
    "X-Paginas": total_registros // limite,
    🐛 **Bug**: `total_registros // limite` trunca: com resto, a última página parcial some. Arredonde para cima (`math.ceil` ou `-(-a // b)`).

--- lib/consultas_service.py:5
    }
    🐛 **Bug**: `//` trunca: com resto, a última página parcial some. Arredonde para baixo (`math.floor` ou `-(-a // b)`).

--- core/pedidos.py:9
    return Counter(x["status"] for x in pedidos)
    🐛 **Bug**: `Counter` de uma sequência vazia levanta `KeyError`. Se `pedidos` pode vir vazia, trate antes ou use `collections.defaultdict(int)`.

--- api/consultas_service.py:2
    return next((x for x in consultas if x["medico_id"] == valor), None)
    🐛 **Bug**: `next` de uma lista vazia levanta `StopIteration`. Se `consultas` pode vir vazia, trate antes ou use `if not consultas:`.

--- backend/tickets_utils.py:11
    return next((x for x in tickets if x["responsavel"] == valor), None)
    🐛 **Bug**: `next` de uma lista vazia levanta `StopIteration`. Se `tickets` pode vir vazia, trate antes ou use `itertools.filterfalse`.

--- core/orders_utils.py:16
    return Decimal(str(valor)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    🐛 **Bug**: O nome diz "arredondar", mas o retorno usa `Decimal` e o input numérico usa `str` (ou `repr`). Portanto, o resultado pode ser uma string com o valor arredondado e o input não entende o que diz. Use `round(value, 2)` ou `'{:.2f}'.format(value)`.

--- backend/leituras.py:5
    pagina, itens = 1, []
    🐛 **Bug**: A condição está invertida: vai para a última página sempre e devolve vazio. Deve ser `if not dados: return []`.

--- api/orders_service.py:9
    return next((x for x in orders if x["customer_id"] == valor), None)
    🐛 **Bug**: `next` de uma sequência vazia levanta `StopIteration`. Se `orders` pode vir vazia, trate antes ou use `if not orders:`.

--- svc/students_jobs.py:10
    with _lock:
    🐛 **Bug**: A função sem `with` fica sem `lock`: um worker fica sem atualizar o contador enquanto o outro começa. Passe `lock=threading.Lock()` como argumento.

--- svc/alunos.py:17
    return next((x for x in alunos if x["turma"] == valor), None)
    🐛 **Bug**: `next(..., None)`停_na última vez: se o lista é vazia, o iterador fica aberto e `next` levanta `StopIteration`. Se `valor` pode vir None, trate antes ou use `if x is not None`.

--- app/partidas_repo.py:8
    return next((x for x in partidas if x["jogador_id"] == valor), None)
    🐛 **Bug**: `next` de uma sequência vazia levanta `StopIteration`. O parâmetro `valor` pode ser `None` e o item não vem, então devolva `None` no caso de empate.

--- backend/viagens.py:9
    for x in viagens:
    🐛 **Bug**: O `except Exception as e:` é executado independentemente do `try` e de forma corrompida. Para capturar tudo, use `except Exception as e:` ou `try: ... except Exception as e: print(e)`.

--- backend/alunos_service.py:2
    sql = "SELECT id FROM alunos WHERE nome LIKE '%{}%'".format(termo)
    🐛 **Bug**: `%{}%` usa a sintaxe de formatação (que permite qualquer tipo de injeção) e espaço no nome permite injeção de comando. Passe a lista como segundo argumento: `conn.execute("SELECT * FROM alunos WHERE nome LIKE %s", (termo,))`.

--- app/viagens_utils.py:14
    pagina, itens = 1, []
    🐛 **Bug**: A condição está invertida: devolve a página vazia quando há mais que um resultado. Deve ser `if not dados: return []`.

--- app/alunos_repo.py:5
    return total == 0
    🐛 **Bug**: `total == 0` compara identidade com uma lista nova e é sempre False. Para testar identidade, use `is 0`.

--- backend/consultas_utils.py:2
    selecionados = [x["duracao"] for x in consultas if x["medico_id"] == valor]
    🐛 **Bug**: `valor` entra num filtro: os resultados não são ordenados e a seleção está sempre vazia. Use `filter(consulta["medico_id"] == valor, consultas)`.

--- src/servicos/partidas_utils_2.py:5
    saida = os.popen(f"ping -c 1 {host}").read()
    🐛 **Bug**: O comando `os.popen` sem `shell=True` usa o sistema de shells padrão (o padrão de Python), e espaço no caminho quebra o comando. Passe `shell=True` como argumento: `os.popen("ping -c 1 {host}")`.

--- app/faturas_jobs.py:8
    return total == 0
    🐛 **Bug**: `total == 0` testa identidade: strings iguais vindas do banco ou de JSON não são o mesmo objeto, e o que se verifica com `== 0` levanta `TypeError`. Use `if not total:` ou `if total == 0`.

--- backend/produtos_jobs.py:9
    novo = usuario not in vistos
    🐛 **Bug**: `not in` testa identidade: para o primeiro time `novo` é avaliado uma vez, e os resultados seguintes se repetem. Use `if usuario not in vistos:`.

--- backend/orders_service_2.py:2
    selecionados = [x["amount"] for x in orders if x["customer_id"] == valor]
    🐛 **Bug**: `valor` pode ser `None` e aí o denominador é zero. Teste `if valor is None` antes de dividir.

--- src/servicos/invoices_jobs.py:5
    return estoque < minimo
    🐛 **Bug**: `< minimo` é `None` no primeiro chamada: quando o invoice ainda não vem no corpo, `estoque` pode ser `None` e a condição levanta `TypeError`. Use `if estoque is None or estoque < minimo:`.

--- app/funcionarios_jobs.py:2
    selecionados = [x["salario"] for x in funcionarios if x["setor"] == valor]
    🐛 **Bug**: `valor` pode ser `None` e aí o denominador é zero. Teste `if valor is None` antes de dividir.

--- backend/alunos_service_2.py:6
    return Decimal(str(valor)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    🐛 **Bug**: O nome diz "arredondar", mas o retorno usa `Decimal` e arredonda para cima. Passe `ROUND_HALF_DOWN` como segundo argumento.

--- backend/pedidos_utils.py:4
    "X-Paginas": total_registros // limite,
    🐛 **Bug**: `total_registros // limite` trunca: com resto, a última página parcial some. Arredonde para cima (`math.ceil` ou `-(-a // b)`).

--- backend/pedidos_utils.py:5
    }
    🐛 **Bug**: `total_registros // limite` pode dar 0 (e o último page num volta paria com o último item), então o último page num volta é `total_registros % limite`.

--- src/servicos/viagens_repo.py:13
    _lock.acquire()
    🐛 **Bug**: A função sem `lock` fica sem semaforo: um chamada numa vez prende a outra. Passe `lock=threading.Lock()`.

--- src/servicos/pedidos_service.py:6
    return estoque > minimo
    🐛 **Bug**: `estoque > minimo` compara identidade: é o mesmo objeto múltiplas vezes. Use `if estoque < minimo`: menor valor que `minimo` sempre vem after o maior. If negada: maior valor que `minimo` sempre vem antes.

--- svc/viagens.py:3
    if i <= 0:
    🐛 **Bug**: O `discard` devolve `False` apenas quando o elemento é encontrado: em listas desordenadas, o segundo `i` acesa `ids[0]` e levanta `IndexError`. Monte a lista antes: `ids = [i for i in ids if i > 0]`.

[60 chamadas, 16286 tokens de entrada, 6229 de saída, 4125.7 s no modelo]