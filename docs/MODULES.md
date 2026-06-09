# Módulos

Referência por pacote.

## `agents/`

| Arquivo | Descrição |
|---|---|
| `orchestrator.py` | `OrchestratorAgent` — pipeline completo |
| `test_generator.py` | `TestGeneratorAgent` — geração de testes via LLM |
| `repair.py` | `RepairAgent` — correção de testes falhos |
| `import_utils.py` | Normalização de imports (`mockes.exemplo`, etc.) |

## `config/`

| Arquivo | Descrição |
|---|---|
| `settings.py` | Configuração Pydantic + `.env` |
| `run_workspace.py` | `RunWorkspace`, persistência de artefatos |
| `logging_setup.py` | Logging console + arquivo |

## `ingest/`

| Arquivo | Descrição |
|---|---|
| `scanner.py` | `RepositoryScanner` — varredura de `*.py` |
| `parser.py` | `parse_repository_graphs()` — ponto de entrada do ingest |
| `extract.py` | `SymbolExtractor` — extração via AST |
| `ast_utils.py` | Parse de arquivo em AST |
| `call_graph.py` | `CallGraph`, `CallGraphBuilder` |
| `dependency_graph.py` | `DependencyGraph`, `DependencyGraphBuilder` |
| `import_resolver.py` | `module_name_from_path()` — caminho → módulo Python |
| `collectors/branches.py` | Contagem de branches por símbolo |
| `collectors/dependency_collector.py` | Dependências chamadas |
| `collectors/exceptions.py` | Exceções lançadas/capturadas |
| `collectors/imports.py` | Imports do arquivo |
| `heuristics/edge_cases.py` | Casos de borda heurísticos |
| `models/ExtractedSymbol.py` | Modelo do símbolo extraído |

## `retrieval/`

| Arquivo | Descrição |
|---|---|
| `retriever.py` | `Retriever` — indexação + enrich RAG |
| `qdrant_client.py` | `QdrantStore` — cliente Qdrant |
| `embeddings.py` | `embed_symbol()`, `embed_symbols()` |
| `embedding_builder.py` | `to_embedding_doc()`, `content_hash()` |
| `hybrid.py` | `HybridCandidate`, `rerank_candidates()`, score híbrido |

## `execution/`

| Arquivo | Descrição |
|---|---|
| `runner.py` | `TestRunner`, `RunResult` |
| `coverage_analyzer.py` | `CoverageAnalyzer` — cobertura orientada |
| `coverage.py` | Utilitários legados de cobertura |

## `llm/`

| Arquivo | Descrição |
|---|---|
| `factory.py` | `get_llm()`, `get_embedder()` |
| `base.py` | `BaseLLM`, `BaseEmbedding` |
| `openai_llm.py` | `OpenAILLM` — chat completions OpenAI |
| `openai_embedding.py` | `OpenAIEmbedding` |
| `local_embedding.py` | Embeddings determinísticos (offline) |
| `mock_llm.py` | LLM mock (offline) |
| `models.py` | `LLMRequest`, `LLMResponse`, `TokenUsage` |
| `usage_tracker.py` | `UsageTracker` — acumula tokens |
| `gemini.py` | Legado Gemini (não usado pelo factory) |
| `gemini_embedding.py` | Legado Gemini embeddings |

## `schemas/`

| Arquivo | Descrição |
|---|---|
| `context.py` | `FunctionContext` — entrada do gerador |
| `retrieval_context.py` | `RetrievalContext`, `RetrievalMetrics` |
| `outputs.py` | `GeneratedTest` — saída do gerador |
| `pipeline.py` | `PipelineStats`, `OrchestrationResult` |

## `main.py`

Entrypoint CLI fino. Não contém lógica de pipeline.

```python
def main(source_dir: str = ".") -> OrchestrationResult:
    orchestrator = OrchestratorAgent()
    return orchestrator.run(source_dir)
```

| Responsabilidade | Onde fica |
|---|---|
| Parse de `sys.argv` | `main.py` |
| Pipeline completo | `agents/orchestrator.py` |
| Configuração | `config/settings.py` |
| Workspace + artefatos | `config/run_workspace.py` |

## `tests/`

Testes unitários do engine. Usam Qdrant em memória (`:memory:`) e embedder fake (`tests/conftest.py`).

## `mockes/`

Código de exemplo (`exemplo.py`) para validar o pipeline:

```bash
python main.py mockes
```
