# Documentação

Índice da documentação do **RAG Test Engine**.

## Comece aqui

| Documento | Conteúdo |
|---|---|
| [../README.md](../README.md) | Instalação, uso rápido, visão geral |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Arquitetura, fases do pipeline, diagramas |
| [CONFIGURATION.md](CONFIGURATION.md) | Variáveis de ambiente (`.env`) |
| [API.md](API.md) | `main()`, agentes e uso programático |
| [MODULES.md](MODULES.md) | Referência de módulos por pacote |

## Fluxo resumido

```
python main.py mockes
       │
       ▼
OrchestratorAgent.run("mockes")
       │
       ├── ingest  → artifacts/symbols.json, call_graph.json, …
       ├── index   → Qdrant (com cache se REINDEX_SYMBOLS=false)
       ├── gen     → TestGeneratorAgent + RAG
       ├── run     → TestRunner (pytest)
       ├── repair  → RepairAgent (até 2x)
       ├── coverage → CoverageAnalyzer (opcional)
       └── save    → runs/mockes/<timestamp>/tests/
```

## Estrutura de saída

```
runs/<fonte>/<timestamp>/
├── tests/              # testes aprovados
├── logs/pipeline.log   # log da execução
└── artifacts/          # parser, grafos, resumo, tokens
```

## Links úteis

- [OpenAI API Pricing](https://openai.com/api/pricing/)
- [Qdrant Docs](https://qdrant.tech/documentation/)
- Dashboard Qdrant local: http://localhost:6333/dashboard
