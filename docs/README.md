# Documentação

Índice da documentação do **RAG Test Engine**.

## Comece aqui

| Documento | Conteúdo |
|---|---|
| [../README.md](../README.md) | Instalação, uso rápido, visão geral |
| [CLI.md](CLI.md) | Argumentos de linha de comando e perfis (`--profile`) |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Arquitetura, fases do pipeline, diagramas |
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
       ├── parsers/source  → artifacts/symbols.json, call_graph.json, …
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
uv run python scripts/run_all_profiles.py mockes   # os 4 em sequência
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
scripts/       # utilitários CLI (run_all_profiles.py)
```

## Estrutura de saída

```
runs/<repo>/[<run_group>/]<profile>/[<timestamp>/]
├── tests/              # testes aprovados
├── logs/
│   ├── pipeline.log    # log da execução (perfil + repo)
│   └── api_calls/      # tokens por chamada (_index.jsonl)
└── artifacts/
    ├── run_summary.json   # token_usage.reconciliation + api_calls_log_match
    └── ...
```

Lote dos 4 perfis: `runs/mockes/<run_group>/sem-rag/`, `.../rag-limitado/`, etc.

## Links úteis

- [OpenAI API Pricing](https://openai.com/api/pricing/)
- [Qdrant Docs](https://qdrant.tech/documentation/)
- Dashboard Qdrant local: http://localhost:6333/dashboard
