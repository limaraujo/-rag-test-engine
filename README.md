# RAG Test Engine

Motor de geração automática de testes **pytest** com **RAG** (Retrieval-Augmented Generation).

O pipeline analisa código Python via AST, indexa símbolos no **Qdrant**, enriquece o contexto com busca híbrida (vetores + grafos), gera testes com **OpenAI**, executa **pytest**, corrige falhas com LLM e opcionalmente regenera por cobertura.

## Requisitos

- Python **3.12+**
- [uv](https://github.com/astral-sh/uv) (recomendado) ou `pip`
- **Qdrant** local (Docker) para indexação persistente
- Chave **OpenAI** (`OPENAI_API_KEY`)

## Instalação

```bash
git clone <repo-url>
cd -rag-test-engine
cp .env.example .env   # edite com sua OPENAI_API_KEY
uv sync                # ou: pip install -r requirements.txt
```

### Qdrant local

```bash
docker run -p 6333:6333 qdrant/qdrant
```

Dashboard: http://localhost:6333/dashboard

## Uso rápido

A `main.py` é apenas o **entrypoint CLI** — ela instancia o `OrchestratorAgent` e delega todo o pipeline a ele.

```bash
# Ajuda dos argumentos
uv run python main.py --help

# Pipeline completo no diretório atual
uv run python main.py

# Testar a pasta de exemplos
uv run python main.py mockes
```

Referência completa dos argumentos: [docs/CLI.md](docs/CLI.md)

Equivalente em Python:

```python
from main import main

result = main("mockes")
print(result.workspace.root)
```

Cada execução cria um workspace isolado:

```
runs/<fonte>/<timestamp>/
├── tests/          # testes gerados que passaram
├── logs/
│   ├── pipeline.log
│   └── api_calls/  # prompts/respostas e tokens (LOG_API_CALLS=true)
└── artifacts/
    ├── symbols.json
    ├── call_graph.json
    ├── dependency_graph.json
    ├── run_meta.json
    └── run_summary.json
```

## Configuração

Copie `.env.example` para `.env`. Variáveis principais:

| Variável | Padrão | Descrição |
|---|---|---|
| `OPENAI_API_KEY` | — | Chave OpenAI (obrigatória) |
| `OPENAI_MODEL` | `gpt-5-nano` | Modelo de chat |
| `OPENAI_EMBEDDING_MODEL` | `text-embedding-3-small` | Modelo de embeddings |
| `AI_MODE` | `openai` | `openai` ou `offline` (sem API) |
| `QDRANT_URL` | `http://localhost:6333` | URL do Qdrant |
| `REINDEX_SYMBOLS` | `false` | `false` = cache incremental |
| `RUNS_DIR` | `runs` | Pasta raiz das execuções |
| `LOG_API_CALLS` | `true` | Grava entrada/saída de cada chamada LLM em `logs/api_calls/` |

Documentação completa: [docs/CONFIGURATION.md](docs/CONFIGURATION.md) · CLI: [docs/CLI.md](docs/CLI.md)

## Pipeline

```
Ingestão → Indexação → Geração → Execução → Reparo → Cobertura → Salvamento
```

1. **Ingestão** — varre `SOURCE_DIR`, extrai símbolos, call graph e dependency graph
2. **Indexação** — embeddings no Qdrant (com cache se `REINDEX_SYMBOLS=false`)
3. **Geração** — LLM gera pytest por símbolo, com contexto RAG
4. **Execução** — roda pytest em subprocesso
5. **Reparo** — até 2 tentativas de correção via LLM se falhar
6. **Cobertura** — regenera se cobertura < `COVERAGE_THRESHOLD`
7. **Salvamento** — grava em `runs/.../tests/`

Detalhes: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

## Uso programático

**Via entrypoint (recomendado):**

```python
from main import main

result = main("mockes")
```

**Via orquestrador diretamente:**

```python
from agents.orchestrator import OrchestratorAgent

orchestrator = OrchestratorAgent()
result = orchestrator.run("mockes")
```

**Retorno (`OrchestrationResult`):**

```python
print(result.workspace.root)   # runs/mockes/20260609_...
print(result.stats.ok)         # testes salvos
print(result.token_summary)    # uso de tokens (modo openai)
```

API completa: [docs/API.md](docs/API.md)

## Testes do projeto

```bash
# Suíte unitária
uv run pytest

# Testes gerados manualmente (legado)
uv run pytest generated_tests -v

# Testes de uma execução em runs/
uv run pytest runs/mockes -v
```

## Estrutura do projeto

```
main.py        # entrypoint CLI → OrchestratorAgent.run()
agents/        # OrchestratorAgent, TestGeneratorAgent, RepairAgent
config/        # settings, logging, run workspace
execution/     # TestRunner, CoverageAnalyzer
ingest/        # parser AST, grafos, ExtractedSymbol
llm/           # OpenAI, embeddings, usage tracker
retrieval/     # Qdrant, Retriever, busca híbrida
schemas/       # FunctionContext, GeneratedTest, OrchestrationResult
tests/         # testes unitários
mockes/        # código de exemplo para testar o pipeline
runs/          # saída de cada execução (gitignored)
docs/          # documentação técnica
```

Índice da documentação: [docs/README.md](docs/README.md) · Módulos: [docs/MODULES.md](docs/MODULES.md)

## Reduzir custos

Análise dos logs em `runs/.../logs/api_calls/_index.jsonl` mostra que **saída do LLM**
(`completion_tokens`) costuma ser 3–5× maior que a entrada. Prioridades:

1. **`MAX_COVERAGE_ROUNDS=0`** — elimina regenerações por cobertura (maior economia)
2. **`LLM_MAX_OUTPUT_TOKENS=2048`** — limita testes verbosos (já é o padrão)
3. **`INGEST_SKIP_FUNCTION_NAMES=main`** — ignora `main()` de scripts (já é o padrão)
4. **`INGEST_SKIP_FILE_GLOBS=*_demo.py`** — ignora arquivos demo (já é o padrão)
5. **`MAX_REPAIRS=1`** — menos tentativas de reparo (já é o padrão)
6. **`REINDEX_SYMBOLS=false`** + Qdrant persistente → evita re-embedar
7. Reduzir `RETRIEVER_TOP_K*` para prompts menores

Perfil completo: [docs/CONFIGURATION.md](docs/CONFIGURATION.md#perfil-econômico-sugerido)

## Licença

Ver repositório do projeto.
