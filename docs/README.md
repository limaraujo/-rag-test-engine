# Documentação

Índice da documentação do **RAG Test Engine**.

## Comece aqui

| Documento | Conteúdo |
|---|---|
| [../README.md](../README.md) | Instalação, uso rápido, visão geral |
| [REPOSITORY_TESTING.md](REPOSITORY_TESTING.md) | Clonar repo externo e testar nos 4 perfis |
| [CLI.md](CLI.md) | Argumentos de linha de comando e perfis (`--profile`) |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Arquitetura, fases do pipeline, diagramas |
| [RAG_TUNING.md](RAG_TUNING.md) | Ajuste do RAG, gating, protocolo de avaliação |
| [CONFIGURATION.md](CONFIGURATION.md) | Variáveis de ambiente (`.env`) |
| [API.md](API.md) | `main()`, agentes e uso programático |
| [MODULES.md](MODULES.md) | Referência de módulos por pacote |

## Fluxo resumido

```
python main.py mockes --profile rag-completo
       │
       ▼
main() → apply_run_profile (opcional) → OrchestratorAgent.run()
       │
       ├── parsers/source  → artifacts/symbols.json, ingest_selection.json, …
       ├── index           → Qdrant (pulado se RAG_MODE=none)
       ├── enrich          → Retriever (pulado se RAG_MODE=none)
       ├── gen             → TestGeneratorAgent + prompts/
       ├── cache           → GenerationCache (se habilitado)
       ├── run             → TestRunner (pytest)
       ├── repair          → RepairAgent (até MAX_REPAIRS)
       ├── coverage        → CoverageAnalyzer (se MAX_COVERAGE_ROUNDS > 0)
       └── save            → runs/mockes/<timestamp>/tests/
```

## Perfis de teste

Quatro presets para comparar RAG e cache — ver [CLI.md](CLI.md#perfis-de-teste---profile):

| Perfil | RAG | Cache |
|---|---|---|
| `sem-rag` | Desligado | Desligado |
| `rag-limitado` | Orçamento reduzido | Desligado |
| `rag-completo` | Completo | Desligado |
| `com-cache` | Completo | Ligado |

```bash
uv run python main.py mockes --profile sem-rag
uv run python scripts/ingest_only.py mockes          # só parser (sem LLM)
uv run python scripts/run_all_profiles.py mockes   # os 4 em sequência; limpa cache após cada perfil
uv run python scripts/clear_cache.py               # limpar cache manualmente
```

## Estrutura do repositório

```
agents/        # orquestrador, gerador, reparo
prompts/       # templates LLM + montagem RAG
parsers/       # resposta LLM (llm/) + código-fonte AST (source/)
cache/         # cache persistente de gerações
config/        # settings, run_profiles, workspace
retrieval/     # Qdrant, busca híbrida
execution/     # pytest, cobertura
llm/           # OpenAI, embeddings, telemetria
schemas/       # modelos Pydantic
scripts/       # ingest_only.py, run_all_profiles.py, clear_cache.py
repositorios/  # clones opcionais (ex.: code_katas)
```

## Estrutura de saída

```
runs/<slug>/[<run_group>/]<profile>/[<timestamp>/]
├── tests/              # testes aprovados
├── logs/
│   ├── pipeline.log    # execução + [arquivo +/-] [símbolo +/-] na ingestão
│   └── api_calls/      # tokens por chamada (_index.jsonl)
└── artifacts/
    ├── ingest_selection.json  # arquivos/símbolos incluídos e ignorados
    ├── run_summary.json       # token_usage.reconciliation + api_calls_log_match
    └── ...
```

`<slug>` = caminho relativo de `SOURCE_DIR` (ex.: `repositorios/code_katas/src` → `repositorios_code_katas_src`).

Lote dos 4 perfis: `runs/mockes/<run_group>/sem-rag/`, `.../rag-limitado/`, etc.

## Links úteis

- [OpenAI API Pricing](https://openai.com/api/pricing/)
- [Qdrant Docs](https://qdrant.tech/documentation/)
- Dashboard Qdrant local: http://localhost:6333/dashboard
