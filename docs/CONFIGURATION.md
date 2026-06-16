# Configuração

Todas as variáveis são carregadas de `.env` na raiz do projeto via `config/settings.py` (Pydantic Settings).

## Exemplo `.env`

```env
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-5-nano
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
QDRANT_URL=http://localhost:6333
AI_MODE=openai
REINDEX_SYMBOLS=false
RAG_MODE=full
GENERATION_CACHE_ENABLED=true
RUNS_DIR=runs
LOG_LEVEL=INFO
LOG_API_CALLS=true
```

## OpenAI

| Variável | Obrigatória | Padrão | Descrição |
|---|---|---|---|
| `OPENAI_API_KEY` | Sim | — | Chave da API OpenAI |
| `OPENAI_MODEL` | Não | `gpt-5-nano` | Modelo de chat para geração e reparo |
| `OPENAI_EMBEDDING_MODEL` | Não | `text-embedding-3-small` | Modelo de embeddings |
| `AI_MODE` | Não | `openai` | `openai` = API real; `offline` = mock/local |

### Modelos de raciocínio (gpt-5*)

Modelos `gpt-5-nano`, `gpt-5-mini`, etc. **não aceitam** `temperature` customizada. O cliente `OpenAILLM` omite esse parâmetro automaticamente.

## Qdrant

| Variável | Padrão | Descrição |
|---|---|---|
| `QDRANT_URL` | `http://localhost:6333` | URL do servidor. Use `:memory:` para testes efêmeros |
| `QDRANT_API_KEY` | `None` | Necessário apenas para Qdrant Cloud |
| `QDRANT_COLLECTION_SYMBOLS` | `symbols` | Coleção de código de produção |
| `QDRANT_COLLECTION_TESTS` | `tests` | Coleção de testes existentes |
| `EMBEDDING_DIMENSIONS` | `1536` | Dimensão dos vetores (deve corresponder ao modelo) |
| `REINDEX_SYMBOLS` | `false` | `true` = reindexa tudo; `false` = só símbolos novos/alterados |

### Cache de embeddings

Com `REINDEX_SYMBOLS=false`:

- Símbolos com mesmo `content_hash` no Qdrant são ignorados na indexação.
- O retriever reutiliza vetores cacheados durante o RAG.
- Reindexe (`REINDEX_SYMBOLS=true`) ao trocar modelo de embedding ou dimensões.

## Execução e logs

| Variável | Padrão | Descrição |
|---|---|---|
| `RUNS_DIR` | `runs` | Raiz dos workspaces (`runs/<fonte>/<timestamp>/`) |
| `LOG_DIR` | `logs` | Fallback se logging não receber caminho explícito |
| `LOG_LEVEL` | `INFO` | `DEBUG`, `INFO`, `WARNING`, `ERROR` |
| `LOG_API_CALLS` | `true` | Grava metadados e tokens de cada chamada em `logs/api_calls/` |
| `LOG_API_CALL_BODIES` | `false` | Persiste prompts/respostas integrais (**desativado por padrão**; valores sensíveis são mascarados) |
| `LOG_API_CALL_METADATA` | `true` | Inclui tamanhos e contexto operacional nos logs de API |

## Segurança

| Variável | Padrão | Descrição |
|---|---|---|
| `SOURCE_DIR_STRICT` | `false` | `true` bloqueia `source_dir` arriscado (raiz do engine ou volume alto de `.py`) |
| `SOURCE_DIR_ALLOW_RISKY` | `false` | Permite continuar em CI/scripts sem flag `--allow-risky-source` |
| `SOURCE_DIR_PY_WARN_THRESHOLD` | `200` | Limite de arquivos Python incluídos antes de aviso/bloqueio |

### O que nunca é indexado

- Arquivos `.env` e `.env.*`
- Chaves (`*.pem`, `*.key`, `id_rsa`, etc.)
- Diretórios sensíveis (`secrets/`, `.ssh/`, `.aws/`, etc.)

### Logs e mascaramento

Por padrão, **prompts completos não são gravados** (`LOG_API_CALL_BODIES=false`). Quando ativado, padrões como `sk-…`, Bearer tokens e atribuições `API_KEY`/`TOKEN`/`SECRET`/`PASSWORD` são mascarados **somente na persistência** — o código-fonte em memória enviado ao modelo não é alterado.

### Rotação de chaves

Se uma chave de API, token ou senha foi exposta em log, issue, commit ou chat:

1. **Revogue** a credencial no painel do provedor (OpenAI, Qdrant Cloud, etc.).
2. **Gere** uma nova chave e atualize apenas o `.env` local (nunca commite).
3. **Verifique** o histórico git com `git log -p -- .env` (o arquivo deve estar no `.gitignore`).
4. Em caso de vazamento em repositório público, considere `git filter-repo` ou suporte do provedor e force-push apenas após alinhar a equipe.

Não reutilize credenciais que já circularam em texto claro.

## Retriever (RAG)

| Variável | Padrão | Descrição |
|---|---|---|
| `RETRIEVER_TOP_K` | `3` | Resultados finais após reranking |
| `RETRIEVER_TOP_K_FUNCTIONS` | `3` | Funções relacionadas por consulta |
| `RETRIEVER_TOP_K_TESTS` | `2` | Testes similares por consulta |
| `RETRIEVER_RERANK_POOL_SIZE` | `10` | Candidatos vetoriais antes do rerank |
| `RETRIEVER_VECTOR_WEIGHT` | `0.5` | Peso da similaridade vetorial |
| `RETRIEVER_DEPENDENCY_WEIGHT` | `0.3` | Peso do dependency graph |
| `RETRIEVER_CALL_GRAPH_WEIGHT` | `0.2` | Peso do call graph |
| `RETRIEVER_SCORE_THRESHOLD` | `0.55` | Similaridade mínima (0–1) para símbolos |
| `RETRIEVER_TEST_SCORE_THRESHOLD` | `0.45` | Similaridade mínima para testes similares |
| `RAG_SKIP_ISOLATED_SYMBOLS` | `true` | Pula RAG em símbolos triviais isolados |
| `RAG_MIN_HYBRID_SCORE` | `0.35` | Filtra candidatos só-vetoriais fracos |
| `RAG_SAME_MODULE_BOOST` | `0.15` | Bônus no rerank para mesmo diretório |

Os pesos híbridos devem somar **1.0**.

## RAG, cache e perfis de execução

| Variável | Padrão | Descrição |
|---|---|---|
| `RAG_MODE` | `full` | `none` = sem enriquecimento RAG; `limited` = orçamento reduzido; `full` = defaults |
| `GENERATION_CACHE_ENABLED` | `true` | Reutiliza testes aprovados do cache antes de chamar o LLM |
| `GENERATION_CACHE_DIR` | *(vazio)* | Diretório do cache (padrão: `.cache/generation/`) |
| `PROMPT_MAX_RAG_TOTAL_CHARS` | `2500` | Orçamento global do corpo dos snippets RAG |
| `PROMPT_MAX_RAG_SNIPPET_CHARS` | `300` | Tamanho máximo de cada snippet RAG |

### Perfis CLI (`--profile`)

Definidos em `config/run_profiles.py`. Sobrescrevem `RAG_MODE` e `GENERATION_CACHE_ENABLED` **apenas durante a execução** (settings restaurados ao final).

| Perfil | `RAG_MODE` | Cache | Overrides |
|---|---|---|---|
| `sem-rag` | `none` | off | — |
| `rag-limitado` | `limited` | off | `PROMPT_MAX_RAG_TOTAL_CHARS=600`, `PROMPT_MAX_RAG_SNIPPET_CHARS=150`, `RETRIEVER_TOP_K_FUNCTIONS=1`, `RETRIEVER_TOP_K_TESTS=1`, `RETRIEVER_RERANK_POOL_SIZE=5` |
| `rag-completo` | `full` | off | — |
| `com-cache` | `full` | on | — |

```bash
uv run python main.py mockes --profile rag-limitado
uv run python scripts/run_all_profiles.py mockes
uv run python scripts/clear_cache.py
```

Ver [CLI.md](CLI.md#perfis-de-teste---profile).

### `scripts/run_all_profiles.py`

| Argumento | Padrão | Descrição |
|---|---|---|
| `SOURCE_DIR` | `mockes` | Diretório Python a analisar |
| `--allow-risky-source` | `false` | Repassa para cada `main()` |
| `--protocol` | `fair` | `fair`: RAG sem cache cruzado + 2ª passagem `com-cache-rerun`. `legacy`: limpa cache após cada perfil |

### Cache de geração e limpeza

O cache persistente armazena testes **já aprovados** (hash do código-fonte + contexto RAG) para o perfil `com-cache` e quando `GENERATION_CACHE_ENABLED=true` no `.env`.

| Ação | Comando |
|---|---|
| Limpar após um run isolado | `python scripts/clear_cache.py` |
| Protocolo justo (lote) | `python scripts/run_all_profiles.py [SOURCE_DIR]` — popula cache em `com-cache`, mede em `com-cache-rerun` |
| Comportamento antigo | `--protocol legacy` |
| Ver caminho sem apagar | `python scripts/clear_cache.py --dry-run` |

**Importante:** limpar `.cache/generation/` **não** apaga vetores no Qdrant. Para reindexar embeddings do zero, use `REINDEX_SYMBOLS=true` ou limpe a coleção no servidor Qdrant.

### Comportamento por `RAG_MODE`

| Modo | Indexação Qdrant | Enriquecimento RAG | Prompt do usuário |
|---|---|---|---|
| `none` | Pulada | Pulado | Só contexto estático do símbolo |
| `limited` | Ativa | Ativa | RAG com orçamento reduzido |
| `full` | Ativa | Ativa | RAG com defaults do `.env` |

## Cobertura e reparo

| Variável | Padrão | Descrição |
|---|---|---|
| `COVERAGE_THRESHOLD` | `80.0` | Cobertura mínima de linhas (%) |
| `MAX_COVERAGE_ROUNDS` | `0` | Rodadas de regeneração por cobertura (`0` = desligado) |
| `MAX_REPAIRS` | `1` | Tentativas de reparo via LLM quando pytest falha |
| `MAX_LLM_CALLS_PER_SYMBOL` | `2` | Limite global de chamadas LLM por símbolo |

## Ingestão (varredura de código)

| Variável | Padrão | Descrição |
|---|---|---|
| `INGEST_SKIP_DIRS` | *(vazio)* | Diretórios extras ignorados na varredura (vírgula). **Mesclado** com padrões fixos: `.git`, `__pycache__`, `.venv`, `venv`, `.pytest_cache`, `.mypy_cache`, `.ruff_cache`, `tests`, `test`, `runs`, `logs`, `generated_tests`, `dist`, `build` |
| `INGEST_SKIP_FILE_GLOBS` | *(vazio)* | Globs extras de arquivo ignorados (vírgula). **Mesclado** com padrões fixos: `test_*.py`, `*_test.py`, `conftest.py`, `*_demo.py` |
| `INGEST_SKIP_FUNCTION_NAMES` | `main` | Funções de módulo ignoradas na geração (vírgula) |

Os padrões fixos **não são removidos** ao definir essas variáveis — apenas acrescentam exclusões.

Código em `src/`, `app/`, `lib/` e pacotes do projeto permanece incluído; somente segmentos de caminho com nome exato de diretório ignorado são excluídos.

**Auditoria:** cada execução grava `artifacts/ingest_selection.json` (lista completa com motivos) e espelha no `logs/pipeline.log` linhas `[arquivo +]`, `[arquivo -]`, `[símbolo +]`, `[símbolo -]`. Ver [CLI.md](CLI.md#exclusões-na-ingestão-arquivos).

## Economia de tokens (LLM)

| Variável | Padrão | Descrição |
|---|---|---|
| `LLM_MAX_OUTPUT_TOKENS` | *(vazio)* | Limite de tokens de saída do chat. Vazio = sem limite na API |
| `REPAIR_ERROR_MAX_CHARS` | `900` | Tamanho máximo do erro pytest no prompt de reparo |
| `GENERATION_MAX_TEST_FUNCTIONS` | `4` | Máximo de funções `test_*` por arquivo gerado |
| `GENERATION_MAX_LINES` | `80` | Máximo de linhas no arquivo de teste gerado |

Para desligar o loop de cobertura (economia de tokens):

```env
MAX_COVERAGE_ROUNDS=0
```

## Perfil econômico sugerido

```env
AI_MODE=openai
OPENAI_MODEL=gpt-5-nano
REINDEX_SYMBOLS=false
RAG_MODE=limited
GENERATION_CACHE_ENABLED=true
MAX_COVERAGE_ROUNDS=0
MAX_REPAIRS=1
MAX_LLM_CALLS_PER_SYMBOL=2
INGEST_SKIP_FUNCTION_NAMES=main
PROMPT_MAX_RAG_TOTAL_CHARS=600
PROMPT_MAX_RAG_SNIPPET_CHARS=150
REPAIR_ERROR_MAX_CHARS=900
RETRIEVER_TOP_K_FUNCTIONS=1
RETRIEVER_TOP_K_TESTS=1
RETRIEVER_RERANK_POOL_SIZE=5
```

Ou use o preset pronto: `uv run python main.py mockes --profile rag-limitado`
