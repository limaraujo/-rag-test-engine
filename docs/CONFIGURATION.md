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
RETRIEVER_TOP_K=3
RETRIEVER_TOP_K_FUNCTIONS=3
RETRIEVER_TOP_K_TESTS=2
RETRIEVER_RERANK_POOL_SIZE=10
```
