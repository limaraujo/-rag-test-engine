# CLI

Referência dos argumentos de linha de comando do entrypoint `main.py`.

## Sintaxe

```bash
uv run python main.py [SOURCE_DIR]
```

| Argumento | Obrigatório | Padrão | Descrição |
|---|---|---|---|
| `SOURCE_DIR` | Não | `.` | Diretório raiz com código Python a analisar. Caminho relativo ou absoluto. |
| `--allow-risky-source` | Não | `false` | Continua com `source_dir` arriscado (raiz do engine ou muitos `.py`). Obrigatório quando `SOURCE_DIR_STRICT=true`. |
| `--profile` | Não | — | Perfil de teste (RAG + cache). Ver tabela abaixo. |

Demais opções (modelo, Qdrant, logs de API, modo estrito) vêm do `.env` ([CONFIGURATION.md](CONFIGURATION.md)).

## Perfis de teste (`--profile`)

Quatro presets para comparar comportamento do pipeline:

| Perfil | RAG | Cache de geração | Uso |
|---|---|---|---|
| `sem-rag` | Desligado | Desligado | Baseline sem contexto RAG nem reutilização de testes |
| `rag-limitado` | Limitado (orçamento reduzido) | Desligado | RAG enxuto: menos snippets e top-k menor |
| `rag-completo` | Completo (defaults do `.env`) | Desligado | RAG com orçamento padrão, sempre regenera via LLM |
| `com-cache` | Completo | Ligado | Igual ao completo, mas reutiliza testes aprovados do cache |

```bash
# Sem RAG
uv run python main.py mockes --profile sem-rag

# RAG limitado
uv run python main.py mockes --profile rag-limitado

# RAG completo (sem cache)
uv run python main.py mockes --profile rag-completo

# RAG completo + cache persistente
uv run python main.py mockes --profile com-cache

# Rodar os 4 perfis em sequência
uv run python scripts/run_all_profiles.py mockes
```

O perfil ativo aparece em `logs/pipeline.log` e em `artifacts/run_summary.json` (`profile`, `source_slug`, `stats.run_profile`).

### Layout de pastas (`runs/`)

| Cenário | Caminho |
|---|---|
| Execução normal | `runs/<repo>/<timestamp>/` |
| Com `--profile` | `runs/<repo>/<profile>/<timestamp>/` |
| Lote dos 4 perfis (`scripts/run_all_profiles.py`) | `runs/<repo>/<run_group>/<profile>/` |

Exemplo do lote:

```
runs/mockes/20260615_143022/
├── sem-rag/logs/pipeline.log
├── rag-limitado/logs/pipeline.log
├── rag-completo/logs/pipeline.log
└── com-cache/logs/pipeline.log
```

Cada pasta de perfil contém `logs/`, `tests/` e `artifacts/` (incluindo `run_summary.json` com `token_usage` e conferência `api_calls_log_match`).

Alternativa via `.env` (sem `--profile`):

```env
RAG_MODE=none          # none | limited | full
GENERATION_CACHE_ENABLED=false
```

## Ajuda integrada

```bash
uv run python main.py --help
```

## Exemplos

```bash
# Analisa o diretório de trabalho atual
uv run python main.py

# Analisa a pasta de exemplos do repositório
uv run python main.py mockes

# Caminho absoluto (Windows)
uv run python main.py "C:\projetos\meu-app\src"

# Caminho relativo
uv run python main.py ./src
```

## O que acontece na execução

1. Cria um workspace em `runs/<nome_fonte>/<timestamp>/`
2. Varre recursivamente `SOURCE_DIR` por arquivos `.py`
3. Executa o pipeline completo (ingestão → indexação → geração → pytest → reparo → cobertura)
4. Grava testes aprovados, logs e artefatos no workspace

O `<nome_fonte>` deriva do nome da pasta em `SOURCE_DIR` (ex.: `mockes` → `runs/mockes/...`).

## Saída gerada

```
runs/<fonte>/<timestamp>/
├── tests/                      # testes pytest que passaram
├── logs/
│   ├── pipeline.log            # log textual da execução
│   └── api_calls/              # se LOG_API_CALLS=true (padrão)
│       ├── _index.jsonl        # índice resumido (tokens por chamada)
│       └── 0001_....json       # entrada/saída de cada chamada LLM/embedding
└── artifacts/
    ├── symbols.json
    ├── call_graph.json
    ├── dependency_graph.json
    ├── run_meta.json
    └── run_summary.json        # stats, token_usage, api_calls_dir
```

## Variáveis de ambiente relevantes

Estas **não** são argumentos CLI, mas afetam o comportamento da execução:

| Variável | Padrão | Efeito |
|---|---|---|
| `AI_MODE` | `openai` | `openai` = API real; `offline` = LLM/embeddings locais |
| `RAG_MODE` | `full` | `none` / `limited` / `full` — sobrescrito por `--profile` |
| `GENERATION_CACHE_ENABLED` | `true` | Cache persistente de testes aprovados |
| `LOG_API_CALLS` | `true` | Grava metadados de chamadas em `logs/api_calls/` |
| `RUNS_DIR` | `runs` | Pasta raiz dos workspaces |
| `REINDEX_SYMBOLS` | `false` | `false` = reutiliza embeddings no Qdrant |

Lista completa: [CONFIGURATION.md](CONFIGURATION.md).

## Uso programático

Equivalente à CLI, sem parse de argumentos:

```python
from main import main

result = main("mockes")
result = main("mockes", profile="com-cache")

print(result.workspace.root)
print(result.generation_cache.hits)
```

Com `apply_run_profile` diretamente:

```python
from config.run_profiles import apply_run_profile
from agents.orchestrator import OrchestratorAgent

with apply_run_profile("sem-rag"):
    result = OrchestratorAgent().run("mockes")
```

Ver também: [API.md](API.md).

## Scripts utilitários

| Script | Comando | Descrição |
|---|---|---|
| Comparar 4 perfis | `uv run python scripts/run_all_profiles.py mockes` | Roda `sem-rag` → `com-cache` em sequência |
| Parser AST (sem API) | `uv run python mockes/exemplo.py` | Só `parsers/source`, sem LLM |

## Scripts em `mockes/`

| Script | Comando | Log de API |
|---|---|---|
| Pipeline (testes + RAG) | `LOG_API_CALLS=true uv run python main.py mockes` | `runs/mockes/<timestamp>/logs/api_calls/` |
| Parser AST (sem API) | `uv run python mockes/exemplo.py` | — |

Confirme no `.env`:

```env
LOG_API_CALLS=true
AI_MODE=openai
```

Para desligar: `LOG_API_CALLS=false`.

## Códigos de saída

A CLI não define códigos de saída customizados — exceções não tratadas propagam como erro Python (`exit code != 0`). Inspecione `result.stats` ou `artifacts/run_summary.json` para o resultado do pipeline.
