# forja-review

**O fechamento do [Forja](../forja).** Um GitHub App que revisa pull requests em português: explica o que muda e aponta bugs nas linhas do diff. Ele chama o modelo pelo [forja-serve](../forja-serve) (ou qualquer endpoint OpenAI-compatível) e manda traces OpenTelemetry que o [forja-evals](../forja-evals) avalia como **eval online**.

> **Resultado:** o pipeline inteiro funciona: webhook → fila → modelo → comentários ancorados nas linhas → feedback → traces → eval online. **O modelo pequeno ainda não.** Com o Gemma 4 26B local como teto, a review acha **4/4 bugs** num PR reservado (7/8 no de ajuste). Com o Qwen2.5-Coder 0.5B (pelo forja-serve) e o 1.5B, acha **0/4**. Em vez de esconder isso, esse é o número que o pós-treino (forja-posttrain) precisa mover.

## Medindo antes de instalar: PRs com bugs plantados

Antes de pôr usuário real na frente, a pergunta é simples: **ele acha bug de verdade?** Para responder, há dois PRs de exemplo com bugs plantados e gabarito:

- [`examples/pr-bugs-plantados.diff`](examples/pr-bugs-plantados.diff) tem 8 bugs: SQL injection, arquivo e conexão sem fechar, 3 divisões por zero ou lista vazia, off-by-one e `//` que perde a última página. É o conjunto usado para **ajustar** o prompt.
- [`examples/pr-holdout.diff`](examples/pr-holdout.diff) tem 4 bugs: condição de TTL invertida, argumento padrão mutável, `requests.get` sem timeout e sem checar o status. É **reservado**: foi criado antes de ajustar o prompt e nunca usado para isso.

Um bug conta como achado quando há comentário no arquivo, a até 2 linhas, que **fala do problema** (palavra-chave do gabarito). Só a posição não basta, e foi a primeira lição:

> Na primeira medição, só por posição, o Qwen 1.5B "achou" 4/8. Lendo os comentários, nenhum apontava bug: eram changelog ("Adicionou a função `percentual`…"), e o da paginação recomendava o bug ao contrário. Com a checagem de conteúdo, caiu para 1/8.

| Modelo (CPU, Ryzen 5 5625U) | Prompt | Ajuste (8 bugs) | **Reservado (4 bugs)** | Formato quebrado | Tempo por PR |
| --- | --- | --- | --- | --- | --- |
| Qwen2.5-Coder 1.5B Q4_K_M (llama.cpp) | v0 | 1/8 | 0/4 | 1 de 5 chamadas | 30–40 s |
| Qwen2.5-Coder 1.5B Q4_K_M (llama.cpp) | v1 | 1/8 | 0/4 | 1 de 5 | 15–30 s |
| Qwen2.5-Coder 1.5B Q4_K_M + `json_mode` | v1 | 1/8 | 0/4 | 0 (gramática) | 15–30 s |
| Qwen2.5-Coder 0.5B fp32 (**forja-serve**) | v1 | 0/8¹ | 0/4 | 2 de 5, +1 cortada em 512 tokens | 1–2 min |
| Gemma 4 26B-A4B Q4_0 (llama.cpp), teto | v1 | **7/8** | **4/4** | 0² | 12–22 min |
| Qwen2.5-Coder 0.5B + SFT LoRA (forja-posttrain R1) | curto | 2/8 | 0/4 | 0 | ~40 s |
| Qwen2.5-Coder 0.5B + SFT + DPO (forja-posttrain R1) | curto | 3/8 | 0/4 | 0 | ~45 s |
| `ruff` (sem modelo, [`examples/linters.py`](examples/linters.py)) | — | 2/8 | 2/4 | — | 0,1 s |

¹ O checker de palavras-chave marcou 1/8, mas o comentário diz que `media` "retorna 0.0 se a lista está vazia", e ela levanta `ZeroDivisionError`. Contado como 0.
² Na primeira tentativa, uma chamada do Gemma foi cortada: ele gastou os 4096 tokens raciocinando antes do JSON. Com 8192, achou a condição invertida do TTL, o bug mais sutil. Agora isso aparece no trace como `resposta_cortada`, não como `json_invalido`.

O que os números dizem:

- **O pipeline não é o gargalo.** O mesmo prompt, a mesma ancoragem e o mesmo parser, com um modelo capaz, acham 11 de 12 bugs com zero comentários extras, e cada comentário traz a correção (`with open(...)`, `?` na query, `descontos=None`, `raise_for_status()`). Os resultados completos estão em [`results/`](results).
- **O modelo pequeno não acha bug: descreve a mudança.** O prompt v1 (checklist, exemplo resolvido, proibição explícita de descrever) e o filtro de comentário descritivo tiraram o changelog. Sobrou o problema real: o 1.5B e o 0.5B inventam defeitos ("deve retornar com duas casas decimais") ou dizem o contrário do certo. `json_mode` resolve o formato, não o raciocínio.
- **O custo do teto é o tempo.** O Gemma raciocina de 1.500 a 4.500 tokens por arquivo a ~7 tok/s: 12 a 22 min por PR em CPU. Funciona para um repositório pessoal com poucos PRs; para uso real, precisa de GPU ou de um modelo pequeno que acerte.
- **A ponte para o resto do Forja:** esses dois PRs viram casos de `deteccao_bug` no forja-evals, e os comentários do Gemma viram pares de preferência para o DPO do forja-posttrain (escolhida: Gemma; rejeitada: o 0.5B). O teto local vira professor do modelo pequeno.

### Depois do pós-treino: modelo + linter

O [forja-posttrain](../forja-posttrain#r1-revisor-de-pr-em-cpu-sft-lora-no-05b) treinou o 0.5B com um LoRA em CPU e mediu num PR de 60 arquivos gerado de templates nunca vistos no treino (53 bugs):

| Revisor | Bugs achados | Comentários extras |
| --- | --- | --- |
| Qwen 0.5B base (prompt curto) | 1/53 | 39 |
| Qwen 0.5B + SFT | 15/53 | 44 |
| ruff (regras de bug/segurança) | 25/53 | 4 |
| Qwen 0.5B + SFT + DPO | 11/53 | 34 |
| **ruff + SFT** | **32/53** | 48 |
| ruff + DPO | 28/53 | 38 |

O linter pega as classes de padrão (SQL montado com string, `shell=True`, default mutável, `requests` sem timeout) quase sem ruído. O modelo acha o que o linter não vê: condição invertida, divisão por lista vazia, paginação. A arquitetura que esses números sugerem é **linter primeiro, modelo para o semântico**, e o que falta é precisão no modelo. O DPO on-policy tentou isso e só deixou o modelo mais calado: menos extras, mas também menos bugs semânticos achados (detalhes no [forja-posttrain](../forja-posttrain#dpo-on-policy)). O próximo passo é dado real, não outro método.

[`examples/linters.py`](examples/linters.py) roda ruff ou bandit sobre o mesmo diff, no mesmo formato do `--json-out`, para a mesma régua do `recall.py` valer para os dois.

### O ciclo fechado: eval online

Os traces desses testes passaram pelo `forja-evals online` com o Gemma como juiz: 12 chamadas sorteadas, nota média 1,43 para o 1.5B e 1,00 para o 0.5B. Dos 14 comentários dos modelos pequenos, o juiz marcou **um** como útil, que é exatamente o único acerto real pelo gabarito. Ver [`forja-evals/baselines/online-forja-review-local`](../forja-evals/baselines/online-forja-review-local).

## O que tem dentro

| Peça | Arquivo | Garantia testada |
| --- | --- | --- |
| Webhook com assinatura HMAC-SHA256, triagem (rascunho, bot, ações) | `app.py` | assinatura errada → 401; o mesmo commit nunca enfileira duas vezes |
| Fila durável em SQLite (idempotente por `repo, pr, sha`, retry com backoff, recuperação após crash) | `store.py` | modelo fora do ar → volta para a fila e desiste após 3 tentativas; `rodando` órfão volta no restart |
| GitHub App: JWT RS256 → token de instalação (com cache) | `github.py` | claims do JWT verificadas com a chave pública; o token é pedido uma vez só |
| Parser de diff (patch da API e `git diff`) com a linha nova de cada linha | `diff.py` | numeração, renomeado, binário, removido, "No newline" |
| Prompt por arquivo, com pedaços de hunks inteiros quando não cabe | `prompt.py` | nada perdido e numeração preservada ao cortar |
| Ancoragem: JSON tolerante, comentário em linha fora do diff descartado, duplicata, excesso, **comentário descritivo** | `parse.py` | cada descarte vira um `problema` no trace, em vez de erro |
| Review publicada com comentários inline e fallback para o corpo se o GitHub recusar (422) | `worker.py` | commit antigo (chegou push novo) → ignorado; 422 → tudo no corpo |
| Feedback: 👍/👎 por comentário (reação não gera webhook; o `feedback` busca) | `worker.py` | reação de bot não conta; sem mudança não re-emite |
| Traces OpenTelemetry (JSONL e, opcionalmente, OTLP) | `telemetry.py` | o feedback aponta para o trace da review |

37 testes, sem rede: GitHub e modelo falsos via `httpx.MockTransport`.

## Como funciona

```text
GitHub ──webhook──▶ POST /webhook ──▶ valida HMAC ──▶ fila (SQLite, único por commit) ──▶ 202
                                                           │
                         worker (mesmo processo) ◀─────────┘
                           1. token de instalação (JWT → /access_tokens, em cache)
                           2. PR ainda está nesse commit? senão, ignora
                           3. /pulls/{n}/files → patch de cada arquivo
                           4. por arquivo: prompt com nº de linha → modelo (forja-serve) → JSON
                           5. ancora (descarta o que não está no diff) → POST /reviews (inline)
                           6. span forja.review.llm por chamada → traces/spans.jsonl
cron: forja-review feedback ──▶ lê 👍/👎 → span forja.review.feedback
forja-evals online ──▶ amostra dos spans → juiz por comentário → juiz × humanos
```

Decisões:

- **A review nunca roda dentro do request.** O GitHub espera no máximo 10 s pelo webhook e reentrega em erro; a review de um PR leva de dezenas de segundos a minutos num modelo em CPU. O endpoint só valida e enfileira.
- **SQLite em vez de Redis.** O volume são alguns PRs por hora. SQLite em WAL tem as garantias que importam (idempotência, persistência, `UPDATE … RETURNING` atômico para pegar o job) sem mais um serviço para operar.
- **Um arquivo por chamada.** Contexto pequeno, ancoragem simples (o modelo só vê números de linha daquele arquivo) e falha isolada: um JSON quebrado perde um arquivo, não a review.
- **Comentar só em linha que está no diff.** A API recusa a review inteira (422) se uma linha não estiver num hunk. A ancoragem descarta antes; se o diff mudar entre a leitura e a publicação, o fallback publica tudo no corpo.
- **Privacidade.** Por padrão, o diff e a resposta vão para o trace, porque o eval online precisa deles. Em repositório privado, `FORJA_REVIEW_CAPTURAR_CONTEUDO=0` guarda só o resultado estruturado.

## Uso

```bash
uv sync
uv run pytest

# Revisar um diff local (sem GitHub), contra o forja-serve ou o llama.cpp
uv run forja-review local main...HEAD --repo-dir ../algum-repo
uv run forja-review local --diff examples/pr-holdout.diff --base-url http://127.0.0.1:8001/v1 --json-out r.json
uv run python examples/recall.py examples/gabarito-holdout.json r.json

# Modelo pós-treinado: prompt curto (o mesmo do treino) e vários arquivos em paralelo
FORJA_REVIEW_CONCORRENCIA=8 uv run forja-review local --diff examples/pr-holdout.diff --model review-sft --prompt curto --json-out r.json

# Linha de base sem modelo, na mesma régua
uv run python examples/linters.py examples/pr-holdout.diff --ferramenta ruff --json-out ruff.json

# Como GitHub App (veja github-app.yml e .env.example)
uv run forja-review serve --port 8080      # webhook + worker
uv run forja-review feedback               # num cron: coleta 👍/👎
uv run forja-review stats                  # X PRs revisados, Y% dos comentários úteis
```

Para instalar: crie o App com as permissões do [`github-app.yml`](github-app.yml) (Pull requests: read & write, Contents: read), aponte o webhook para `/webhook` (um túnel como `cloudflared` serve para rodar em casa), salve a chave `.pem` fora do repositório e preencha o `.env`.

## Limitações (honestas)

- **Ainda não tem usuários reais.** O App está pronto para instalar, mas os números acima vêm de PRs com bugs plantados, não de tráfego. O "X PRs revisados, Y% úteis" do plano só existe depois de instalar em repositórios de verdade; o `stats` e o `forja-evals online` já medem isso.
- **12 bugs plantados não são um benchmark.** Servem para separar "acha" de "não acha" (0/4 contra 4/4), não para medir diferenças finas. O checker de palavras-chave é leniente (houve um falso positivo, contado à mão); a régua de verdade é o juiz do eval online, calibrado contra 👍/👎.
- **Uma review por commit.** Push novo gera uma review nova; não há resumo incremental nem resolução de comentários antigos.
- **Contexto só do diff.** O modelo não vê o resto do arquivo nem o repositório: um bug que depende de código fora do hunk passa.
- **Um processo.** Webhook e worker no mesmo processo; para escalar, o worker vira um processo separado lendo a mesma fila (o `claim` já é atômico).
- **O teto é lento.** O modelo que funciona (Gemma 26B) leva minutos por arquivo em CPU.
