# Fluxogramas — arquitetura e experimentos

Diagramas da arquitetura do **RAG Test Engine** e das diferenças entre os perfis de experimento (`--profile`).

---

## 1. Visão geral do pipeline

```mermaid
flowchart TB
    subgraph entry [Entrada]
        CLI["main.py / scripts/run_all_profiles.py"]
        SRC["SOURCE_DIR<br/>(ex.: repositorios/pyjwt/jwt)"]
    end

    subgraph profile [Perfil opcional]
        RP["apply_run_profile()<br/>sem-rag | rag-limitado | rag-completo | com-cache"]
    end

    subgraph orch [OrchestratorAgent.run]
        ING["1. Ingestão<br/>AST + CallGraph + DependencyGraph"]
        IDX["2. Indexação<br/>Embeddings → Qdrant"]
        GEN["3. Geração por símbolo<br/>RAG + LLM + Cache"]
        VAL["4. Validação da suíte<br/>pytest em tests/"]
        SUM["5. Artefatos<br/>run_summary.json + suite_metrics"]
    end

    subgraph store [Persistência]
        RUNS["runs/&lt;slug&gt;/&lt;profile&gt;/&lt;timestamp&gt;/"]
        TESTS["tests/ — arquivos aprovados"]
        ART["artifacts/ — symbols, grafos, métricas"]
        LOGS["logs/ — pipeline.log, api_calls/"]
    end

    CLI --> RP
    SRC --> orch
    RP --> orch
    ING --> IDX
    IDX --> GEN
    GEN --> VAL
    VAL --> SUM
    SUM --> RUNS
    RUNS --> TESTS
    RUNS --> ART
    RUNS --> LOGS
```

**Ponto de entrada:** `main.py` instancia `OrchestratorAgent` e chama `.run(source_dir)`.

**Saída:** `OrchestrationResult` + workspace em `runs/`.

---

## 2. Fase de ingestão e indexação

```mermaid
flowchart LR
    subgraph ingest [Ingestão — sempre executa]
        SCAN["scan_python_files()"]
        PARSE["parse_repository_graphs()"]
        FILTER["filter_symbols()"]
        SAVE["save_ingest_artifacts()"]
    end

    subgraph index [Indexação — depende do perfil]
        CHECK{"RAG_MODE<br/>== none?"}
        SKIP["Pula Qdrant"]
        EMB["index_symbols()<br/>OpenAI / Local embedding"]
        QDRANT[("Qdrant<br/>coleção symbols")]
    end

    SCAN --> PARSE --> FILTER --> SAVE
    SAVE --> CHECK
    CHECK -->|sim sem-rag| SKIP
    CHECK -->|não| EMB --> QDRANT
```

| Artefato | Conteúdo |
|---|---|
| `symbols.json` | Todos os símbolos extraídos |
| `call_graph.json` | Quem chama quem |
| `dependency_graph.json` | Dependências estruturais |
| `ingest_selection.json` | Símbolos incluídos/ignorados |

---

## 3. Loop por símbolo (núcleo do experimento)

Cada função/método elegível passa pelo fluxo abaixo. **O perfil altera principalmente os blocos RAG e Cache.**

```mermaid
flowchart TB
    SYM["ExtractedSymbol"]
    CTX["FunctionContext.from_symbol()"]

    RAG_GATE{"RAG_MODE<br/>!= none?"}
    ENRICH["Retriever.enrich()<br/>busca híbrida + grafos"]
    STATIC["Contexto estático apenas<br/>(código, imports, exceções, branches)"]

    CACHE_GATE{"Cache hit?<br/>GENERATION_CACHE_ENABLED"}
    CACHE_HIT["Reutiliza teste + RunResult<br/>sem chamar LLM"]
    LLM_GEN["TestGeneratorAgent.generate()<br/>system + user prompt"]

    PYTEST["TestRunner — pytest"]
    PASS1{"Passou?"}
    REPAIR["RepairAgent<br/>até MAX_REPAIRS"]
    COV{"MAX_COVERAGE_ROUNDS > 0<br/>e abaixo do threshold?"}
    COV_REGEN["Regenera com lacunas de cobertura"]
    SAVE["save_approved_test()<br/>→ tests/test_*.py"]

    SYM --> CTX --> RAG_GATE
    RAG_GATE -->|sim| ENRICH --> CACHE_GATE
    RAG_GATE -->|não| STATIC --> CACHE_GATE
    CACHE_GATE -->|hit| CACHE_HIT --> COV
    CACHE_GATE -->|miss| LLM_GEN --> PYTEST --> PASS1
    PASS1 -->|não| REPAIR --> COV
    PASS1 -->|sim| COV
    COV -->|sim| COV_REGEN --> SAVE
    COV -->|não / ok| SAVE
```

---

## 4. Enriquecimento RAG (quando ativo)

```mermaid
flowchart TB
    TARGET["Símbolo alvo"]
    GATE{"should_apply_rag()?<br/>símbolo trivial isolado"}

    EMB_Q["Embedding da consulta"]
    VEC["Busca ANN no Qdrant<br/>pool → rerank híbrido"]
    CG["Call graph<br/>callers + callees"]
    DG["Dependency graph"]
    TESTS["Busca testes similares<br/>coleção tests"]

    SCORE["Score híbrido<br/>0.5 vetor + 0.3 dep + 0.2 call + boost módulo"]
    FILTER["filter_hybrid_candidates()<br/>score mínimo p/ só-vetoriais"]
    PROMPT["build_rag_prompt_sections()<br/>dedup + truncamento + orçamento"]

    TARGET --> GATE
    GATE -->|pula| OUT_STATIC["Sem bloco RAG"]
    GATE -->|aplica| EMB_Q --> VEC
    GATE -->|aplica| CG
    GATE -->|aplica| DG
    VEC --> SCORE --> FILTER
    CG --> PROMPT
    DG --> PROMPT
    FILTER --> PROMPT
    TESTS --> PROMPT
    PROMPT --> OUT["FunctionContext + RetrievalContext"]
```

---

## 5. Perfis de experimento — comparação

Os perfis são presets em `config/run_profiles.py`. Cada um isola uma variável para comparação justa.

```mermaid
flowchart LR
    subgraph baseline [Baseline]
        SR["sem-rag<br/>❌ RAG ❌ Cache"]
    end

    subgraph rag [Escala de RAG]
        RL["rag-limitado<br/>✅ RAG reduzido ❌ Cache"]
        RC["rag-completo<br/>✅ RAG full ❌ Cache"]
    end

    subgraph cache [Cache]
        CC["com-cache<br/>✅ RAG full ✅ Cache<br/>1ª passagem — popula cache"]
        CCR["com-cache-rerun<br/>✅ RAG full ✅ Cache<br/>2ª passagem — mede hits"]
    end

    SR --> RL --> RC --> CC --> CCR
```

### Tabela comparativa

| Perfil | `RAG_MODE` | Indexação Qdrant | Contexto no prompt | Cache de geração | Objetivo do experimento |
|---|---|---|---|---|---|
| **sem-rag** | `none` | ❌ Pulada | Só análise estática (AST, exceções, branches) | ❌ | **Baseline** — quanto o LLM resolve sem contexto externo |
| **rag-limitado** | `limited` | ✅ | RAG com orçamento reduzido (600 chars total, 1 snippet) | ❌ | **Custo/benefício** — RAG mínimo ainda ajuda? |
| **rag-completo** | `full` | ✅ | RAG completo (2500 chars, top-3 related, grafos) | ❌ | **Máximo RAG** — teto de qualidade sem cache |
| **com-cache** | `full` | ✅ | Igual rag-completo | ✅ (popula) | **Cache frio→quente** — 1ª execução grava entradas no cache |
| **com-cache-rerun** | `full` | ✅ | Igual rag-completo | ✅ (reutiliza) | **Medir hits** — 2ª execução; compara tokens/tempo vs com-cache |

### Overrides do `rag-limitado`

| Variável | Padrão (`rag-completo`) | `rag-limitado` |
|---|---|---|
| `PROMPT_MAX_RAG_TOTAL_CHARS` | 2500 | **600** |
| `PROMPT_MAX_RAG_SNIPPET_CHARS` | 300 | **150** |
| `RETRIEVER_TOP_K_FUNCTIONS` | 3 | **1** |
| `RETRIEVER_TOP_K_TESTS` | 2 | **1** |
| `RETRIEVER_RERANK_POOL_SIZE` | 10 | **5** |

### O que muda no prompt do LLM

```mermaid
flowchart TB
    subgraph semrag [sem-rag]
        S1["## Função alvo"]
        S2["## Código-fonte"]
        S3["## Imports / Exceções / Branches"]
        S4["❌ Sem seções RAG"]
    end

    subgraph raglim [rag-limitado]
        R1["Mesmo contexto estático"]
        R2["+ 1 snippet related (≤150 chars)"]
        R3["+ callees/callers/deps se couberem<br/>orçamento total ≤ 600 chars"]
    end

    subgraph ragfull [rag-completo / com-cache]
        F1["Mesmo contexto estático"]
        F2["+ até 3 related (híbrido)"]
        F3["+ callees, callers, deps"]
        F4["+ até 2 testes similares"]
        F5["orçamento ≤ 2500 chars"]
    end

    semrag --> raglim --> ragfull
```

### O que muda no cache (`com-cache` vs demais)

```mermaid
sequenceDiagram
    participant O as Orchestrator
    participant C as GenerationCache
    participant L as LLM

    Note over O,L: sem-rag / rag-limitado / rag-completo
    O->>C: lookup
    C-->>O: miss (cache desligado)
    O->>L: generate()
    L-->>O: teste

    Note over O,L: com-cache (1ª passagem)
    O->>C: lookup
    C-->>O: miss
    O->>L: generate()
    L-->>O: teste
    O->>C: store (após aprovação)

    Note over O,L: com-cache-rerun (2ª passagem)
    O->>C: lookup
    C-->>O: hit ✓
    Note right of O: Sem chamada LLM<br/>tokens ≈ 0
```

---

## 6. Protocolo de lote (`run_all_profiles.py`)

Compara os 5 perfis em sequência dentro do mesmo `run_group`.

```mermaid
flowchart TB
    START["run_all_profiles.py SOURCE_DIR"]
    CLEAR0["Limpa cache de geração"]
    GROUP["run_group = timestamp<br/>ex.: 20260615_015849"]

    SR["sem-rag"]
    RL["rag-limitado"]
    RC["rag-completo"]
    CC["com-cache"]
    CCR["com-cache-rerun"]

    C1["Limpa cache"]
    C2["Limpa cache"]
    C3["Limpa cache"]
    KEEP["Mantém cache<br/>(popula entradas)"]
    C4["Limpa cache ao final"]

    CMP["compare_run_metrics.py<br/>tabela comparativa"]

    START --> CLEAR0 --> GROUP
    GROUP --> SR --> C1 --> RL --> C2 --> RC --> C3 --> CC --> KEEP --> CCR --> C4 --> CMP
```

### Protocolo `fair` (padrão)

| Passo | Perfil | Cache após execução | Por quê |
|---|---|---|---|
| 1 | sem-rag | Limpa | RAG comparado sem resíduo |
| 2 | rag-limitado | Limpa | Idem |
| 3 | rag-completo | Limpa | Idem |
| 4 | com-cache | **Mantém** | Popula cache para a 2ª passagem |
| 5 | com-cache-rerun | Limpa | Mede hits; limpa para próximo lote |

### O que comparar nos resultados

| Comparação | Perfis | Métrica principal |
|---|---|---|
| **RAG ajuda?** | sem-rag vs rag-limitado vs rag-completo | `ok`, `repaired`, `failed`, tokens |
| **RAG limitado basta?** | rag-limitado vs rag-completo | Qualidade vs custo de tokens |
| **Cache economiza?** | com-cache vs com-cache-rerun | `generation_cache.hits`, tokens, tempo |
| **Suíte executável?** | Todos | `suite_metrics`, validação pytest final |

Layout de saída:

```
runs/<slug>/<run_group>/
├── sem-rag/
├── rag-limitado/
├── rag-completo/
├── com-cache/
└── com-cache-rerun/
```

---

## 7. Mapa de módulos

```mermaid
flowchart TB
    subgraph agents [agents/]
        ORCH["orchestrator.py"]
        GEN["test_generator.py"]
        REP["repair.py"]
        SVC["services/<br/>generation, repair, coverage"]
    end

    subgraph retrieval [retrieval/]
        RET["retriever.py"]
        HYB["hybrid.py"]
        POL["rag_policy.py"]
    end

    subgraph prompts [prompts/]
        TPL["templates/*.txt"]
        RAGP["rag.py"]
    end

    subgraph parsers [parsers/]
        SRC["source/ — AST, grafos"]
        LLMP["llm/response.py"]
    end

    subgraph infra [infra]
        LLM["llm/ — OpenAI, embeddings"]
        EXEC["execution/ — pytest, coverage"]
        CACHE["cache/generation_cache.py"]
        CFG["config/ — settings, run_profiles"]
    end

    ORCH --> RET
    ORCH --> GEN
    ORCH --> REP
    ORCH --> SVC
    GEN --> TPL
    GEN --> RAGP
    RET --> HYB
    RET --> POL
    GEN --> LLMP
    ORCH --> SRC
    SVC --> CACHE
    GEN --> LLM
    RET --> LLM
    SVC --> EXEC
    ORCH --> CFG
```

---

## Comandos rápidos

```bash
# Um perfil
uv run python main.py repositorios/pyjwt/jwt --profile rag-completo

# Lote completo (5 experimentos)
uv run python scripts/run_all_profiles.py repositorios/pyjwt/jwt

# Comparar métricas
uv run python scripts/compare_run_metrics.py runs/repositorios_pyjwt_jwt/<run_group>
```

## Referências

- [ARCHITECTURE.md](ARCHITECTURE.md) — descrição textual das fases
- [PROMPTS_AND_TECHNIQUES.md](PROMPTS_AND_TECHNIQUES.md) — prompts e técnicas RAG
- [RAG_TUNING.md](RAG_TUNING.md) — ajuste fino e protocolo de avaliação
- [CLI.md](CLI.md) — argumentos e layout de `runs/`
