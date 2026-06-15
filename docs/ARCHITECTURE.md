# Arquitetura

## Visão geral

O **RAG Test Engine** é um pipeline em fases orquestrado pelo `OrchestratorAgent`. Cada fase é independente e comunica-se via modelos Pydantic (`ExtractedSymbol`, `FunctionContext`, `GeneratedTest`).

## Entrypoint

```
main.py  →  OrchestratorAgent.run()  →  OrchestrationResult
```

A `main.py` não contém lógica de pipeline — apenas:

1. Faz parse de `SOURCE_DIR` via `argparse` (padrão: `"."`; use `--help` para ajuda)
2. Instancia `OrchestratorAgent`
3. Chama `orchestrator.run(source_dir)`
4. Retorna `OrchestrationResult`

Detalhes dos argumentos: [CLI.md](CLI.md)

```python
# main.py (simplificado)
def main(
    source_dir: str = ".",
    *,
    profile: str | None = None,
) -> OrchestrationResult:
    if profile:
        with apply_run_profile(profile):
            return OrchestratorAgent().run(source_dir)
    return OrchestratorAgent().run(source_dir)
```

```mermaid
flowchart TB
    subgraph ingest [Ingestão]
        Scanner --> Parser
        Parser --> Symbols[ExtractedSymbol]
        Parser --> CG[CallGraph]
        Parser --> DG[DependencyGraph]
    end

    subgraph index [Indexação]
        Symbols --> Embed[OpenAI Embedding]
        Embed --> Qdrant[(Qdrant)]
    end

    subgraph gen [Geração por símbolo]
        Symbols --> Ctx[FunctionContext]
        Ctx --> Retriever
        Qdrant --> Retriever
        CG --> Retriever
        DG --> Retriever
        Retriever --> EnrichedCtx[FunctionContext + RAG]
        EnrichedCtx --> Generator[TestGeneratorAgent]
        Prompts[prompts/] --> Generator
        Generator --> LLM[OpenAI Chat]
        LLM --> Parser[parsers/llm/response]
        Parser --> Test[GeneratedTest]
    end

    subgraph exec [Validação]
        Test --> Runner[TestRunner / pytest]
        Runner -->|falhou| Repair[RepairAgent]
        Repair --> LLM
        Runner -->|passou| Coverage[CoverageAnalyzer]
        Coverage -->|baixa| Generator
        Runner -->|ok| Save[runs/.../tests/]
    end

    ingest --> index
    index --> gen
    gen --> exec
```

## Fases do pipeline

### 1. Ingestão

**Entrada:** caminho do diretório fonte (`SOURCE_DIR`)

**Módulos:** `parsers/source/scanner.py`, `parsers/source/parser.py`, `parsers/source/extract.py`

1. `RepositoryScanner` varre `*.py`, ignorando `.git`, `__pycache__`, `venv`, etc.
2. Cada arquivo é parseado em AST (`ast_utils.py`).
3. `SymbolExtractor` produz `ExtractedSymbol` (função, método ou classe).
4. Coletores AST extraem imports, branches, exceções e dependências.
5. `CallGraphBuilder` e `DependencyGraphBuilder` constroem grafos estruturais.

**Saída:** lista de símbolos + grafos, persistidos em `artifacts/`.

### 2. Indexação

**Módulo:** `retrieval/retriever.py`, `retrieval/embeddings.py`

> **Nota:** pulada quando `RAG_MODE=none` (perfil `sem-rag` ou `.env`).

1. Para cada símbolo, monta documento textual (`embedding_builder.py`).
2. Gera embedding via `OpenAIEmbedding` (ou `LocalEmbedding` em modo offline).
3. Faz upsert no Qdrant (`QdrantStore`) na coleção `symbols`.
4. Com `REINDEX_SYMBOLS=false`, símbolos inalterados são pulados (hash de conteúdo).

**IDs estáveis:** UUID-5 derivado do `qualified_name` — reindexação não duplica pontos.

### 3. Enriquecimento RAG

**Módulos:** `retrieval/retriever.py`, `retrieval/hybrid.py`, `prompts/rag.py`

> **Nota:** pulado quando `RAG_MODE=none`. Com `RAG_MODE=limited` (perfil `rag-limitado`),
> o orçamento de snippets e top-k é reduzido via `config/run_profiles.py`.

Para cada símbolo alvo:

1. Obtém vetor de consulta (cache do Qdrant ou nova chamada de embedding).
2. Busca ANN na coleção `symbols` (pool de `RETRIEVER_RERANK_POOL_SIZE` candidatos).
3. Coleta vizinhos do call graph (callers/callees) e dependency graph.
4. Reordena com score híbrido:

```
score = 0.5 × similaridade_vetorial
      + 0.3 × dependency_score
      + 0.2 × call_graph_score
```

5. Busca testes similares na coleção `tests` (se existir).
6. `prompts/rag.py` deduplica, trunca e aplica orçamento global ao bloco RAG no prompt.
7. Preenche `FunctionContext.retrieval_context`.

### 4. Geração de testes

**Módulos:** `agents/test_generator.py`, `prompts/loader.py`, `parsers/llm/response.py`

1. `prompts/templates/generator_system.txt` fornece o system prompt (limites via `settings`).
2. `FunctionContext.to_prompt_block()` formata o user prompt com contexto estático + RAG.
3. `TestGeneratorAgent` envia system + user prompt ao LLM.
4. `parsers/llm/response.parse_response()` normaliza a saída: remove markdown, valida sintaxe.
5. `agents/import_utils.normalize_test_imports()` corrige caminhos de importação.

**Cache de geração:** se `GENERATION_CACHE_ENABLED=true` (perfil `com-cache` ou `.env`),
`agents/services/generation_service.py` consulta `cache/generation_cache.py` antes de chamar o LLM.

**Imports:** usa `module_name` relativo à raiz do projeto (ex.: `from mockes.exemplo import Calculadora`). O `import_utils.normalize_test_imports()` corrige imports incorretos gerados pelo LLM. O `PYTHONPATH` na execução aponta para a raiz do repositório (`config.settings.ROOT`).

### 5. Execução

**Módulo:** `execution/runner.py`

1. `TestRunner` escreve `GeneratedTest.full_code` em arquivo temporário.
2. Executa `pytest -v --noconftest` com `PYTHONPATH` na raiz do projeto.
3. Retorna `RunResult` (passed, stdout/stderr, contagens).

### 6. Reparo

**Módulos:** `agents/repair.py`, `prompts/templates/repair_system.txt`

Se `RunResult.passed == False`:

1. Monta prompt com contexto, código falho e saída do pytest.
2. `RepairAgent` pede correção ao LLM.
3. Reexecuta pytest (até `max_repairs`, padrão 2).

### 7. Cobertura

**Módulo:** `execution/coverage_analyzer.py`

Se o teste passou e `MAX_COVERAGE_ROUNDS > 0`:

1. `CoverageAnalyzer` mede cobertura da função alvo.
2. Se abaixo de `COVERAGE_THRESHOLD`, injeta lacunas em `FunctionContext`.
3. Regenera teste e revalida (com loop de reparo se necessário).

### 8. Persistência

**Módulo:** `config/run_workspace.py`

Cada execução cria `runs/<slug>/<timestamp>/`:

| Pasta/arquivo | Conteúdo |
|---|---|
| `tests/` | Arquivos `test_<symbol>.py` aprovados |
| `logs/pipeline.log` | Log com timestamp |
| `artifacts/symbols.json` | Símbolos extraídos |
| `artifacts/call_graph.json` | Grafo de chamadas |
| `artifacts/dependency_graph.json` | Grafo de dependências |
| `artifacts/run_meta.json` | Metadados iniciais |
| `artifacts/run_summary.json` | Stats + tokens + `run_profile` ao final |

## Perfis de execução

**Módulo:** `config/run_profiles.py`

Quatro presets CLI (`--profile`) aplicam overrides temporários em `settings` durante a execução:

| Perfil | `RAG_MODE` | Cache | Overrides extras |
|---|---|---|---|
| `sem-rag` | `none` | off | — |
| `rag-limitado` | `limited` | off | `PROMPT_MAX_RAG_TOTAL_CHARS=600`, `RETRIEVER_TOP_K_FUNCTIONS=1`, … |
| `rag-completo` | `full` | off | — |
| `com-cache` | `full` | on | — |

O perfil ativo é registrado em `pipeline.log` e em `run_summary.json` (`stats.run_profile`).

Ver [CLI.md](CLI.md#perfis-de-teste---profile).

## Modos de operação

### `AI_MODE=openai` (padrão)

- LLM: `OpenAILLM` (`gpt-5-nano` por padrão)
- Embeddings: `OpenAIEmbedding` (`text-embedding-3-small`)
- Rastreamento de tokens via `UsageTracker`

### `AI_MODE=offline`

- LLM: `MockLLM` (testes mínimos determinísticos)
- Embeddings: `LocalEmbedding` (vetores hash, sem API)
- Útil para validar pipeline sem custo

## Modelos de dados principais

| Modelo | Arquivo | Papel |
|---|---|---|
| `ExtractedSymbol` | `parsers/source/models/ExtractedSymbol.py` | Símbolo extraído do AST |
| `FunctionContext` | `schemas/context.py` | Entrada do gerador (código + RAG) |
| `RetrievalContext` | `schemas/retrieval_context.py` | Contexto RAG híbrido |
| `GeneratedTest` | `schemas/outputs.py` | Arquivo pytest estruturado |
| `RunResult` | `execution/runner.py` | Resultado do pytest |
| `PipelineStats` | `schemas/pipeline.py` | Contadores da execução |
| `OrchestrationResult` | `schemas/pipeline.py` | Resultado final do orchestrator |

## Extensibilidade

| Ponto | Como estender |
|---|---|
| LLM | Implementar `BaseLLM`, registrar em `llm/factory.py` |
| Embeddings | Implementar `BaseEmbedding`, registrar em `llm/factory.py` |
| Coletores AST | Novos collectors em `parsers/source/collectors/` |
| Score híbrido | Pesos em `RETRIEVER_*_WEIGHT` no `.env` |
| Pipeline | Injetar dependências em `OrchestratorAgent(...)` |
| Prompts LLM | Editar `prompts/templates/*.txt` |
| Orçamento RAG | `prompts/rag.py` + variáveis `PROMPT_MAX_RAG_*` |
| Parsing LLM | `parsers/llm/response.py` |
