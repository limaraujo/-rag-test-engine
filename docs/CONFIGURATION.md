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
| `RETRIEVER_TOP_K` | `10` | Resultados finais após reranking |
| `RETRIEVER_TOP_K_FUNCTIONS` | `10` | Funções relacionadas por consulta |
| `RETRIEVER_TOP_K_TESTS` | `10` | Testes similares por consulta |
| `RETRIEVER_RERANK_POOL_SIZE` | `30` | Candidatos vetoriais antes do rerank |
| `RETRIEVER_VECTOR_WEIGHT` | `0.5` | Peso da similaridade vetorial |
| `RETRIEVER_DEPENDENCY_WEIGHT` | `0.3` | Peso do dependency graph |
| `RETRIEVER_CALL_GRAPH_WEIGHT` | `0.2` | Peso do call graph |
| `RETRIEVER_SCORE_THRESHOLD` | `0.55` | Similaridade mínima (0–1) |

Os pesos híbridos devem somar **1.0**.

## Cobertura

| Variável | Padrão | Descrição |
|---|---|---|
| `COVERAGE_THRESHOLD` | `80.0` | Cobertura mínima de linhas (%) |
| `MAX_COVERAGE_ROUNDS` | `2` | Rodadas de regeneração por cobertura insuficiente |
| `MAX_REPAIRS` | `1` | Tentativas de reparo via LLM quando pytest falha |

## Ingestão (varredura de código)

| Variável | Padrão | Descrição |
|---|---|---|
| `INGEST_SKIP_DIRS` | *(vazio)* | Diretórios extras ignorados na varredura (vírgula). **Mesclado** com padrões fixos: `.git`, `__pycache__`, `.venv`, `venv`, `.pytest_cache`, `.mypy_cache`, `.ruff_cache`, `tests`, `test`, `runs`, `logs`, `generated_tests`, `dist`, `build` |
| `INGEST_SKIP_FILE_GLOBS` | *(vazio)* | Globs extras de arquivo ignorados (vírgula). **Mesclado** com padrões fixos: `test_*.py`, `*_test.py`, `conftest.py`, `*_demo.py` |

Os padrões fixos **não são removidos** ao definir essas variáveis — apenas acrescentam exclusões.

Código em `src/`, `app/`, `lib/` e pacotes do projeto permanece incluído; somente segmentos de caminho com nome exato de diretório ignorado são excluídos.

## Economia de tokens (LLM)

| Variável | Padrão | Descrição |
|---|---|---|
| `LLM_MAX_OUTPUT_TOKENS` | `2048` | Limite de tokens de saída do chat. Use vazio/`null` para sem limite |
| `INGEST_SKIP_FUNCTION_NAMES` | `main` | Funções de módulo ignoradas na geração (vírgula) |
| `PROMPT_MAX_RAG_SNIPPET_CHARS` | `600` | Tamanho máximo de cada trecho RAG no prompt |
| `REPAIR_ERROR_MAX_CHARS` | `1500` | Tamanho máximo do erro pytest no prompt de reparo |

Para desligar o loop de cobertura (economia de tokens):

```env
MAX_COVERAGE_ROUNDS=0
```

## Perfil econômico sugerido

```env
AI_MODE=openai
OPENAI_MODEL=gpt-5-nano
REINDEX_SYMBOLS=false
MAX_COVERAGE_ROUNDS=0
MAX_REPAIRS=1
LLM_MAX_OUTPUT_TOKENS=2048
INGEST_SKIP_FUNCTION_NAMES=main
INGEST_SKIP_DIRS=
INGEST_SKIP_FILE_GLOBS=
PROMPT_MAX_RAG_SNIPPET_CHARS=400
REPAIR_ERROR_MAX_CHARS=1200
RETRIEVER_TOP_K=3
RETRIEVER_TOP_K_FUNCTIONS=3
RETRIEVER_TOP_K_TESTS=2
RETRIEVER_RERANK_POOL_SIZE=10
```
