### 🔎 forja-review

**O que muda**

- `jobs/invoices_jobs.py`: Adiciona uma função que pesquisa invoices por nome.
- `backend/funcionarios_utils.py`: Adiciona ao arquivo 2 funções: uma que verifica se o estoque precisa ser reabastecido; uma que testa connectivity to a server.
- `app/students_jobs.py`: Adiciona 2 funções: uma que calcula a média de `valores` moveis; uma que arredonda um número para baixo.
- `backend/students_utils.py`: Adiciona uma função que remove ids negativos.
- `api/leituras_repo.py`: Adiciona uma função que registra um visitante.
- `svc/faturas.py`: Adiciona ao arquivo 3 funções: uma que testa a conectividade de um fatura; uma que remove ids negativos; uma que devolve o primeiro registro com `empresa_id` igual a um valor.
- `jobs/alunos.py`: Adiciona 3 funções: uma que mescla dicionários; uma que arredonda um valor para duas casas; uma que conta os status de alunos.
- `backend/orders_service.py`: Adiciona 3 funções: uma que arredonda um valor para baixo; uma que testa connectivity a um servidor; uma que mescla dicionários.
- `src/servicos/faturas_service.py`: Adiciona 3 funções: uma que devolve o fatura com o maior `total`; uma que mescla dicionários; uma que calcula a média de `total` por `empresa_id`.
- `src/servicos/consultas_repo.py`: Adiciona uma função que testa connectivity a um servidor.
- `src/servicos/partidas_utils.py`: Adiciona ao arquivo 2 funções: uma que calcula a média de `pontos` por `jogador_id`; uma que verifica se o estoque é menor que o mínimo.
- `lib/readings_jobs.py`: Adiciona uma função que verifica se o reading precisa ser reabastecido.
- `lib/readings.py`: Adiciona ao arquivo 2 funções: uma que devolve o reading com `device_id` igual a um parâmetro; uma que conta os status de readings.
- `backend/faturas_utils.py`: Adiciona 3 funções: uma que mescla dicionários; uma que registra um visitante; uma que lista todos faturas.
- `src/servicos/alunos_jobs.py`: Adiciona ao arquivo 2 funções: uma que arredonda um valor para baixo; uma que mescla dicionários.
- `api/viagens.py`: Adiciona 2 funções: uma que processa pagamentos de viagens; uma que busca viagens na database.
- `src/servicos/viagens_jobs.py`: Adiciona 3 funções: uma que testa connectivity a um servidor; uma que calcula a média de `distancia` por motorista ID; uma que conta os status de viagens.
- `svc/produtos.py`: Adiciona 2 funções: uma que registra um visita de um produto; uma que conta os status de produtos.
- `core/partidas_service.py`: Adiciona ao arquivo 3 funções: uma que calcula a média de `moveis` de um conjunto de partidas; uma que lista todos os partidas de uma página; uma que calcula o tamanho total de um conjunto de partidas.
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
- `core/pedidos.py`: Adiciona ao arquivo 2 funções: uma que devolve o pedido com o cliente id menor; uma que conta os status de pedidos.
- `api/consultas_service.py`: Adiciona 2 funções: uma que devolve o consulta com `medico_id` primeiro; uma que calcula a média de `medico_id` de uma lista de consultas.
- `backend/tickets_utils.py`: Adiciona ao arquivo 3 funções: uma que devolve o ticket com `responsavel` igual a um valor; uma que calcula o percentual de itens entre o total; uma que arredonda um número para baixo.
- `core/orders_utils.py`: Adiciona 3 funções: uma que verifica se o estoque precisa reabastecer; uma que calcula a média de `amount` por `customer_id`; uma que arredonda um número.
- `backend/leituras.py`: Adiciona uma função que lista todos os leituras.
- `api/orders_service.py`: Adiciona ao arquivo 2 funções: uma que devolve o order com `customer_id` igual a um valor; uma que calcula a média de `amount` por `customer_id`.
- `svc/students_jobs.py`: Adiciona 2 funções: uma que registra um student; uma que lista todos os students.
- `lib/consultas_repo_2.py`: Adiciona uma função que calcula a média de `duracao` por `medico_id`.
- `svc/alunos_jobs.py`: Adiciona uma função que verifica se o aluno precisa reabastecer.
- `svc/alunos.py`: Adiciona 3 funções: uma que calcula o cabeçalho da página de alunos; uma que calcula a média de um número de colunas; uma que devolve o primeiro aluno de um lista por `valor`.
- `app/partidas_repo.py`: Adiciona 2 funções: uma que mescla dicionários; uma que devolve o primeiro item de `partidas` com `valor` (ou `None` no caso de empate).
- `backend/viagens.py`: Adiciona ao arquivo 2 funções: uma que processa pagamentos; uma que registra um visitante.
- `app/consultas_repo.py`: Adiciona uma função que mescla dicionários.
- `backend/alunos_service.py`: Adiciona 2 funções: uma que pesquisa alunos por nome; uma que remove ids inválidos.
- `app/viagens_utils.py`: Adiciona ao arquivo 2 funções: uma que busca viagens na API; uma que lista todos os viagens.
- `app/alunos_repo.py`: Adiciona 2 funções: uma que verifica se o total é 0; uma que conta os status de alunos.
- `backend/consultas_utils.py`: Adiciona 2 funções: uma que calcula a média de `duracao` por `medico_id`; uma que verifica se o estoque precisa ser reabastecido.
- `src/servicos/partidas_utils_2.py`: Adiciona uma função que testa connectivity a um servidor.
- `app/faturas_jobs.py`: Adiciona ao arquivo 2 funções: uma que verifica se o `total` é 0; uma que lista faturas por nome.
- `backend/produtos_jobs.py`: Adiciona ao arquivo 3 funções: uma que verifica se o usuário já visitou; uma que registra um visita; uma que conta os status de produtos.
- `backend/orders_service_2.py`: Adiciona uma função que calcula a média de `amount` por `customer_id`.
- `src/servicos/invoices_jobs.py`: Adiciona 2 funções: uma que verifica se o invoice precisa reabastecer; uma que arredonda um valor para duas casas.
- `core/orders_jobs.py`: Adiciona uma função que verifica se o pedido precisa reabastecer.
- `app/funcionarios_jobs.py`: Adiciona uma função que calcula a média de `salario` por setor.
- `backend/alunos_service_2.py`: Adiciona 2 funções: uma que arredonda um valor para duas casas; uma que conta os status de alunos.
- `backend/pedidos_utils.py`: Adiciona uma função que calcula o número de páginas.
- `src/servicos/viagens_repo.py`: Adiciona ao arquivo 3 funções: uma que registra um viagem; uma que calcula o número de páginas de viagens; uma que remove ids inválidos.
- `src/servicos/pedidos_service.py`: Adiciona ao arquivo uma função que verifica se o estoque precisa ser reabastecido.
- `svc/viagens.py`: Adiciona uma função que remove ids inválidos.

**45 comentários nas linhas** (45 bugs).

<sub>Modelo `review-dpo`. Reaja com 👍 ou 👎 nos comentários: é assim que medimos se a revisão ajuda. Revisão automática; pode errar.</sub>

--- backend/funcionarios_utils.py:10
    return estoque < minimo
    🐛 **Bug**: `estoque < minimo` compara identidade, não valor: uma lista vazia é sempre menor que qualquer número. Use `if not estoque:`.

--- app/students_jobs.py:5
    saida = []
    🐛 **Bug**: `k` pode ser 0 e ser ignorado em cada iteração: a média de um número sequencial é `NaN` (Not a Number). Se `k` pode ser 0, trate antes ou use `valores[-k:]`.

--- app/students_jobs.py:13
    return Decimal(str(valor)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    🐛 **Bug**: O `round` default é `ROUND_HALF_UP`, então comum o número se arredonda para baixo. Use `ROUND_HALF_DOWN`.

--- svc/faturas.py:10
    saida = os.popen(f"ping -c 1 {host}").read()
    🐛 **Bug**: `os.popen` sem nome usa o shell padrão (comando padrão de shell no Linux), e num servidor sem `shell=True` some comlaguma coisa. Passe `shell=False`.

--- svc/faturas.py:19
    return next((x for x in faturas if x["empresa_id"] == valor), None)
    🐛 **Bug**: `None` no `next` de `faturas` quando itere vazio: uma vez que o iterador se da, o elemento seguinte nunca é avaliado. Itere `list(faturas)` ou monte um novo lista.

--- jobs/alunos.py:12
    return Decimal(str(valor)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    🐛 **Bug**: `Decimal("0.01")` converte para zero e trunca: com 2 casas, "0,10" vale 0, não 1. Use `Decimal("0.10")`.

--- jobs/alunos.py:16
    return Counter(x["status"] for x in alunos)
    🐛 **Bug**: O nome diz "alunos", mas o filtro usa `x["status"]` e devolve vazio para o campo que não tem. Troque para `x["status"] is not None`.

--- backend/orders_service.py:10
    saida = os.popen(f"ping -c 1 {host}").read()
    🐛 **Bug**: `os.popen` sem nome de arquivo cria uma nova janela: um processo com `ping` numa porta fica parado; use `subprocess.check_output`.

--- src/servicos/partidas_utils.py:16
    return estoque > minimo
    🐛 **Bug**: `estoque` pode ser 0 e a média é `None` quando o conjunto é vazio. Teste `if not estoque:` antes de dividir.

--- lib/readings.py:10
    return next((x for x in readings if x["device_id"] == valor), None)
    🐛 **Bug**: `next` de uma sequência vazia levanta `StopIteration`. Se `readings` pode vir vazia, trate antes ou use `itertools.find_first_true`.

--- lib/readings.py:14
    return Counter(x["status"] for x in readings)
    🐛 **Bug**: `Counter` de tuplas de um lista de tuples levanta `RuntimeWarning: dictionary value changed size during iteration`. Itere sobre `list(readings)` ou monte um novo dicionário.

--- src/servicos/alunos_jobs.py:10
    return Decimal(str(valor)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    🐛 **Bug**: `Decimal("0.01")` sempre arredonda para baixo, então os valores que já estão abaixo disso aparecem como acima. Use `Decimal("0.01").quantize(Decimal("1"), rounding=ROUND_HALF_UP)`.

--- src/servicos/alunos_jobs.py:14
    saida = dict(padrao)
    🐛 **Bug**: `extra` pode ser `None` e o dicionário vira vazio: `{}` quando chega como `None` no Python 3.6. Use `if extra is None: extra = {}`.

--- api/viagens.py:2
    for x in viagens:
    🐛 **Bug**: `except Exception as e:` captura tudo, inclusive `KeyboardInterrupt` e erros de programação, e devolve `None` como se o operário der erro. Capture `(OSError, Exception)` só.

--- api/viagens.py:10
    sql = "SELECT id FROM viagens WHERE nome LIKE ?"
    🐛 **Bug**: `conn.execute` sem tipo de cursor: lista de resultados indeterminada. Use `cursor.fetchall()` ou `cursor.bind_param` e tire o tipo de cursor depois.

--- src/servicos/viagens_jobs.py:11
    selecionados = [x["distancia"] for x in viagens if x["motorista_id"] == valor]
    🐛 **Bug**: `valor` entra num comando com `sudo`: pule aspas e teste como if `valor is None`: `if viagens and viagens[0]["motorista_id"] == valor:`.

--- svc/produtos.py:5
    novo = usuario not in vistos
    🐛 **Bug**: `not in` testa identidade: para o elemento a primeira vez, o índice é `None`, e o teste verifica `vistos is None` (e é `False` para qualquer valor), e o resultado é `True`. Use `if usuario not in vistos:`.

--- svc/produtos.py:11
    return Counter(x["status"] for x in produtos)
    🐛 **Bug**: `Counter` de tuplas de 2 itens levanta `RuntimeWarning: dictionary value changed size during iteration`. Itere sobre `list(x)`, monte um novo dicionário e vá. (`produtos` numa lista de iters é avaliado uma vez: 100 itens, 100 contagem.)

--- core/partidas_service.py:12
    saida = []
    🐛 **Bug**: `k` pode ser 0 e ser ignorado em some: tuplas vazias entre `for` e `if` se verem como verdadeiros. Use `if v is not None and k in v`.

--- core/partidas_service.py:20
    pagina, itens = 1, []
    🐛 **Bug**: A condição está invertida: itere uma lista e devolva o último elemento, então travie o `for` sem checar o que vem depois. Use `for x in lista:`.

--- backend/produtos_utils.py:13
    pagina, itens = 1, []
    🐛 **Bug**: `while True` sem `break` fica em loop indefinido: cada página completa duas vezes. Passe `break` no fim.

--- backend/produtos_utils.py:24
    sql = "SELECT id FROM produtos WHERE nome LIKE '%{}%'".format(termo)
    🐛 **Bug**: SQL injection: `termo` entra direto no texto da query. Passe como parâmetro (`?`) em vez de interpolar.

--- app/readings_repo.py:13
    selecionados = [x["value"] for x in readings if x["device_id"] == valor]
    🐛 **Bug**: `valor` entra num filtro: devolve itens que não estão no `readings` (o que não existe) e prende o banco de dados. Passe uma lista de valores para `filter` (e evite aí o `or None`): `[x["device_id"] == valor for x in readings]`.

--- lib/pedidos.py:10
    saida = dict(padrao)
    🐛 **Bug**: `padrao` é avaliado uma vez: todas as chaves de `extra` são o mesmo e o que se apaga também apaga para todas. Use `dict.fromkeys(extra.keys(), padrao)`.

--- lib/pedidos.py:16
    return Counter(x["status"] for x in pedidos)
    🐛 **Bug**: `Counter` de uma sequência vazia levanta `ZeroDivisionError`. Se `pedidos` pode vir vazia, trate antes ou use `Counter(pedidos["status"])`.

--- lib/students_repo.py:16
    return Counter(x["status"] for x in students)
    🐛 **Bug**: `Counter` de `students` vira vazio com cada `id` (duplo `id` no HTML ou no Python): uma id vira o outro e some os counts. Passe a tupla como segundo argumento: `Counter(*students)`.

--- lib/students_repo.py:20
    novo = usuario not in vistos
    🐛 **Bug**: `novo` é avaliado uma vez, depois dos ids já foram descartados, então True some os ids vindos de `vistos` e False some os de `students`. Troque para `novo = not usuario in vistos`.

--- lib/consultas_repo.py:8
    sql = "SELECT id FROM consultas WHERE nome LIKE '%{}%'".format(termo)
    🐛 **Bug**: `%` formata a string antes de chegar no driver, então os valores entram crus no SQL (injeção e erro com aspas). Passe a tupla como segundo argumento: `conn.execute("SELECT * FROM ...", (termo,))`.

--- core/pedidos.py:5
    return next((x for x in pedidos if x["cliente_id"] == valor), None)
    🐛 **Bug**: `None` no `next` vira `None` sempre: o pedido com o menor `cliente_id` vem depois de todos os outros. Retorne um valor padrão (o primeiro item default) se não houver itens.

--- core/pedidos.py:9
    return Counter(x["status"] for x in pedidos)
    🐛 **Bug**: `Counter` de tuplas vira um dicionário com valores unicos: dos mesmos `cliente_id` aparecem 2. Passe a chave `x["cliente_id"]`.

--- api/consultas_service.py:2
    return next((x for x in consultas if x["medico_id"] == valor), None)
    🐛 **Bug**: `next` de uma lista vazia levanta `StopIteration`. Se `consultas` pode vir vazia, trate antes ou use `if not consultas:`.

--- api/consultas_service.py:6
    saida = []
    🐛 **Bug**: `k` pode ser maior que o número de itens: em que caso `valores[i + k]` é `valores[i] + k - 1` e o elemento seguinte não existe, e `sum(janela)` levanta `IndexError`. Use `valores[i:i + k] if i + k <= len(valores) else []`.

--- backend/tickets_utils.py:11
    return next((x for x in tickets if x["responsavel"] == valor), None)
    🐛 **Bug**: `next` de uma lista vazia levanta `StopIteration`. Se `tickets` pode vir vazia, trate antes ou use `itertools.filterfalse`.

--- backend/tickets_utils.py:15
    return {
    🐛 **Bug**: `math.ceil` trunca: com resto, o último página parcial some. Arredonde para cima: `math.ceil(total_registros / limite) - 1`.

--- api/orders_service.py:9
    return next((x for x in orders if x["customer_id"] == valor), None)
    🐛 **Bug**: `next` de uma sequência vazia levanta `StopIteration`. Se `orders` pode vir vazia, trate antes ou use `itertools.filterfalse`.

--- api/orders_service.py:13
    selecionados = [x["amount"] for x in orders if x["customer_id"] == valor]
    🐛 **Bug**: `len(selecionados)` pode ser 0 e a média é `None` quando o conjunto é vazio. Teste `if not selecionados:` antes de dividir.

--- backend/viagens.py:9
    for x in viagens:
    🐛 **Bug**: `except Exception as e:` captura tudo, inclusive `KeyboardInterrupt` e erros de programação, e devolve `None` como se o usuário clicou no `X`. Capture `(OSError, Exception)` só: erros de programação.

--- backend/alunos_service.py:2
    sql = "SELECT id FROM alunos WHERE nome LIKE '%{}%'".format(termo)
    🐛 **Bug**: `%{}%` usa a sintaxe de formatação (que permite qualquer tipo de injeção) e espaço no nome permite injeção de comando. Passe a lista de argumentos como segundo argumento: `conn.execute("SELECT * FROM alunos WHERE nome LIKE %s", (termo,))`.

--- backend/consultas_utils.py:2
    selecionados = [x["duracao"] for x in consultas if x["medico_id"] == valor]
    🐛 **Bug**: `valor` entra num filtro: os resultados não são ordenados e corrompencem. Passe uma tupla como segundo argumento: `consultas.filter(medico_id=valor)`.

--- backend/consultas_utils.py:9
    return estoque > minimo
    🐛 **Bug**: `estoque` pode ser 0 e a função verifica a condição: maior que o minimo. Retorne `False` só para o caso padrão (estoque zero) e calcule numa lista: `[estoque > minimo for estoque in estoque]`.

--- backend/produtos_jobs.py:9
    novo = usuario not in vistos
    🐛 **Bug**: `not in` verifica identidade: não verifica o valor, e o usuário pode vir multipleplas vezes com o mesmo `id`. Use `if usuario not in vistos`: conjunto mutável, não permite duplicidade.

--- backend/produtos_jobs.py:15
    return Counter(x["status"] for x in produtos)
    🐛 **Bug**: `Counter` de tuplas levanta `RuntimeWarning: dictionary too large` com `n` itens: %s`.

--- src/servicos/invoices_jobs.py:5
    return estoque < minimo
    🐛 **Bug**: `< minimo` é `None` no primeiro chamada: quando o invoice ainda não vem no corpo, `estoque` pode ser `None` e a condição levanta `TypeError`. Use `if estoque is None or estoque < minimo:`.

--- src/servicos/viagens_repo.py:13
    _lock.acquire()
    🐛 **Bug**: `acquire()` de `_lock` numa thread só é avaliado uma vez: todas as outras chamadas de `_lock` trava numa mesma thread. Passe `blocking=False` como segundo argumento.

--- src/servicos/viagens_repo.py:26
    for i in ids:
    🐛 **Bug**: `ids.discard(i)` está sempre verificando o elemento atual e levanta `ValueError: list index out of range` quando o item é removido: uma id inválida é o último e o índice seguinte é sempre `None`. Monte uma nova lista: `[i for i in ids if i > 0]`.

[60 chamadas, 16286 tokens de entrada, 5372 de saída, 7624.2 s no modelo]