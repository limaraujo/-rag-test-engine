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

# Comparar modos: sem RAG, RAG limitado, RAG completo, com cache
uv run python main.py mockes --profile sem-rag
uv run python main.py mockes --profile rag-limitado
uv run python main.py mockes --profile rag-completo
uv run python main.py mockes --profile com-cache

# Rodar lote comparativo (protocolo justo: RAG + com-cache-rerun)
uv run python scripts/run_all_profiles.py mockes
```

Referência completa dos argumentos e perfis: [docs/CLI.md](docs/CLI.md)

Equivalente em Python:

```python
from main import main

result = main("mockes")
print(result.workspace.root)
```

Cada execução cria um workspace isolado. O nome da pasta em `runs/` (`<slug>`) segue o **caminho relativo** de `SOURCE_DIR` (ex.: `repositorios/code_katas/src` → `repositorios_code_katas_src`).

```
runs/<slug>/[<run_group>/]<profile>/[<timestamp>/]
├── tests/          # testes gerados que passaram
├── logs/
│   ├── pipeline.log       # inclui [arquivo +/-] e [símbolo +/-] na ingestão
│   └── api_calls/         # metadados e tokens (LOG_API_CALLS=true)
└── artifacts/
    ├── ingest_selection.json  # arquivos/símbolos incluídos e ignorados
    ├── run_summary.json       # token_usage + api_calls_log_match
    └── ...
```

Ingestão isolada (sem LLM): `uv run python scripts/ingest_only.py [SOURCE_DIR]`

Lote dos 4 perfis: `runs/mockes/20260615_143022/sem-rag/`, `.../rag-limitado/`, etc. O script limpa `.cache/generation/` após cada perfil por padrão.

Repositório externo (ex. [code-katas](https://github.com/rwisecar/code-katas)): [docs/REPOSITORY_TESTING.md](docs/REPOSITORY_TESTING.md)

## Configuração

Copie `.env.example` para `.env`. Variáveis principais:

| Variável | Padrão | Descrição |
|---|---|---|
| `OPENAI_API_KEY` | — | Chave OpenAI (obrigatória) |
| `OPENAI_MODEL` | `gpt-5-nano` | Modelo de chat |
| `OPENAI_EMBEDDING_MODEL` | `text-embedding-3-small` | Modelo de embeddings |
| `AI_MODE` | `openai` | `openai` ou `offline` (sem API) |
| `QDRANT_URL` | `http://localhost:6333` | URL do Qdrant |
| `REINDEX_SYMBOLS` | `false` | `false` = cache incremental de embeddings |
| `RAG_MODE` | `full` | `none` / `limited` / `full` — ver perfis abaixo |
| `GENERATION_CACHE_ENABLED` | `true` | Reutiliza testes aprovados antes de chamar o LLM |
| `RUNS_DIR` | `runs` | Pasta raiz das execuções |
| `LOG_API_CALLS` | `true` | Grava metadados de cada chamada LLM em `logs/api_calls/` |
| `LOG_API_CALL_BODIES` | `false` | Prompts/respostas integrais (desativado por padrão por segurança) |

**Segurança:** nunca aponte `SOURCE_DIR` para a raiz deste repositório em produção. Arquivos `.env`, chaves e diretórios `secrets/` são ignorados na varredura. Se uma chave foi exposta, rotacione-a no provedor — ver [docs/CONFIGURATION.md](docs/CONFIGURATION.md#rotação-de-chaves).

Documentação completa: [docs/CONFIGURATION.md](docs/CONFIGURATION.md) · CLI e perfis: [docs/CLI.md](docs/CLI.md) · Repositório externo: [docs/REPOSITORY_TESTING.md](docs/REPOSITORY_TESTING.md)

## Perfis de teste

Quatro presets via `--profile` para comparar RAG e cache sem editar o `.env`:

| Perfil | RAG | Cache | Quando usar |
|---|---|---|---|
| `sem-rag` | Desligado | Desligado | Baseline mínimo (sem Qdrant no prompt) |
| `rag-limitado` | Orçamento reduzido | Desligado | RAG enxuto para economizar tokens |
| `rag-completo` | Defaults do `.env` | Desligado | RAG completo, sempre gera via LLM |
| `com-cache` | Defaults do `.env` | Ligado | Reutiliza testes já aprovados |

```bash
uv run python main.py mockes --profile rag-completo
uv run python scripts/run_all_profiles.py mockes
uv run python scripts/clear_cache.py   # após run isolado
```

Detalhes: [docs/CLI.md](docs/CLI.md#perfis-de-teste---profile)

## Pipeline

```
Ingestão → Indexação → Geração → Execução → Reparo → Cobertura → Salvamento
```

1. **Ingestão** — `parsers/source/` varre `SOURCE_DIR`, extrai símbolos e grafos; grava `ingest_selection.json` e log de seleção
2. **Indexação** — embeddings no Qdrant (pulada se `RAG_MODE=none`)
3. **Enriquecimento** — busca híbrida RAG (pulada se `RAG_MODE=none`)
4. **Geração** — LLM gera pytest (`prompts/` + `parsers/llm/`)
5. **Execução** — roda pytest em subprocesso
6. **Reparo** — até `MAX_REPAIRS` tentativas de correção via LLM
7. **Cobertura** — regenera se cobertura < `COVERAGE_THRESHOLD` (`MAX_COVERAGE_ROUNDS > 0`)
8. **Salvamento** — grava em `runs/.../tests/` e opcionalmente no cache persistente

Detalhes: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

## Uso programático

**Via entrypoint (recomendado):**

```python
from main import main

result = main("mockes", profile="rag-completo")
```

**Via orquestrador com perfil:**

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

# Testes de uma execução em runs/
uv run pytest runs/mockes -v
```

## Estrutura do projeto

```
main.py        # entrypoint CLI → OrchestratorAgent.run()
agents/        # OrchestratorAgent, TestGeneratorAgent, RepairAgent
prompts/       # templates LLM e montagem RAG
parsers/       # parsing de respostas LLM e código-fonte (AST/grafos)
cache/         # cache persistente de gerações aprovadas
config/        # settings, run_profiles, logging, run workspace
scripts/       # ingest_only.py, run_all_profiles.py, clear_cache.py
execution/     # TestRunner, CoverageAnalyzer
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

1. **`MAX_COVERAGE_ROUNDS=0`** — elimina regenerações por cobertura (já é o padrão)
2. **`--profile rag-limitado`** ou `RAG_MODE=limited` — RAG com orçamento reduzido
3. **`--profile sem-rag`** — desliga indexação e enriquecimento RAG
4. **`INGEST_SKIP_FUNCTION_NAMES=main`** — ignora `main()` de scripts (já é o padrão)
5. **`MAX_REPAIRS=1`** — menos tentativas de reparo (já é o padrão)
6. **`REINDEX_SYMBOLS=false`** + Qdrant persistente → evita re-embedar
7. **`GENERATION_CACHE_ENABLED=true`** ou `--profile com-cache` → reutiliza testes aprovados

Perfil completo: [docs/CONFIGURATION.md](docs/CONFIGURATION.md#perfil-econômico-sugerido)

## Licença

Ver repositório do projeto.
