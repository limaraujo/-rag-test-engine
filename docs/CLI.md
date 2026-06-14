# CLI

Referência dos argumentos de linha de comando do entrypoint `main.py`.

## Sintaxe

```bash
uv run python main.py [SOURCE_DIR]
```

| Argumento | Obrigatório | Padrão | Descrição |
|---|---|---|---|
| `SOURCE_DIR` | Não | `.` | Diretório raiz com código Python a analisar. Caminho relativo ou absoluto. |

Não há flags adicionais na CLI — modelo, Qdrant, logs de API e demais opções vêm do `.env` ([CONFIGURATION.md](CONFIGURATION.md)).

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
| `LOG_API_CALLS` | `true` | Grava prompts e respostas em `logs/api_calls/` |
| `RUNS_DIR` | `runs` | Pasta raiz dos workspaces |
| `REINDEX_SYMBOLS` | `false` | `false` = reutiliza embeddings no Qdrant |

Lista completa: [CONFIGURATION.md](CONFIGURATION.md).

## Uso programático

Equivalente à CLI, sem parse de argumentos:

```python
from main import main

result = main("mockes")
print(result.workspace.root)
print(result.workspace.logs_dir / "api_calls")
```

Ver também: [API.md](API.md).

## Scripts em `mockes/`

| Script | Comando | Log de API |
|---|---|---|
| Pipeline (testes + RAG) | `LOG_API_CALLS=true uv run python main.py mockes` | `runs/mockes/<timestamp>/logs/api_calls/` |
| Embeddings só deste arquivo | `LOG_API_CALLS=true uv run python mockes/embedding_demo.py mockes/exemplo.py` | `logs/mockes/embedding_demo/<timestamp>/api_calls/` |
| Parser AST (sem API) | `uv run python mockes/exemplo.py` | — |

Confirme no `.env`:

```env
LOG_API_CALLS=true
AI_MODE=openai
```

Para desligar: `LOG_API_CALLS=false`.

## Códigos de saída

A CLI não define códigos de saída customizados — exceções não tratadas propagam como erro Python (`exit code != 0`). Inspecione `result.stats` ou `artifacts/run_summary.json` para o resultado do pipeline.
