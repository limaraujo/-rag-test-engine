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

```bash
# Pipeline completo no diretório atual
uv run python main.py

# Testar a pasta de exemplos
uv run python main.py mockes
```

Cada execução cria um workspace isolado:

```
runs/<fonte>/<timestamp>/
├── tests/          # testes gerados que passaram
├── logs/
│   └── pipeline.log
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

Documentação completa: [docs/CONFIGURATION.md](docs/CONFIGURATION.md)

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

```python
from agents.orchestrator import OrchestratorAgent

result = OrchestratorAgent().run("mockes")

print(result.workspace.root)   # runs/mockes/20260609_...
print(result.stats.ok)         # testes salvos
print(result.token_summary)    # uso de tokens
```

API dos agentes: [docs/API.md](docs/API.md)

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
agents/        # OrchestratorAgent, TestGeneratorAgent, RepairAgent
config/        # settings, logging, run workspace
execution/     # TestRunner, CoverageAnalyzer
ingest/        # parser AST, grafos, ExtractedSymbol
llm/           # OpenAI, embeddings, usage tracker
retrieval/     # Qdrant, Retriever, busca híbrida
schemas/       # FunctionContext, GeneratedTest, PipelineStats
main.py        # entrypoint CLI
tests/         # testes unitários
mockes/        # código de exemplo para testar o pipeline
```

Módulos: [docs/MODULES.md](docs/MODULES.md)

## Reduzir custos

- `REINDEX_SYMBOLS=false` + Qdrant persistente → evita re-embedar
- `MAX_COVERAGE_ROUNDS=0` no `.env` → desliga loop de cobertura
- `OPENAI_MODEL=gpt-5-nano` (já é o padrão)
- Reduzir `RETRIEVER_TOP_K*` para prompts menores

## Licença

Ver repositório do projeto.
