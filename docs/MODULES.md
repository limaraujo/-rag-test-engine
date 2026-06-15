# Módulos

Referência por pacote.

## `agents/`

Agentes LLM e serviços do pipeline de geração/reparo.

| Arquivo | Descrição |
|---|---|
| `orchestrator.py` | `OrchestratorAgent` — pipeline completo |
| `test_generator.py` | `TestGeneratorAgent` — geração de testes via LLM |
| `repair.py` | `RepairAgent` — correção de testes falhos |
| `import_utils.py` | Normalização de imports (`mockes.exemplo`, etc.) |

### `agents/policies/`

| Arquivo | Descrição |
|---|---|
| `llm_budget.py` | Orçamento de chamadas LLM por símbolo e fingerprint de erros |

### `agents/services/`

| Arquivo | Descrição |
|---|---|
| `generation_service.py` | Geração com cache persistente e salvamento de testes aprovados |
| `repair_cycle.py` | Loop iterativo de reparo via LLM |
| `coverage_cycle.py` | Loop de regeneração orientado por cobertura |
| `pipeline_logging.py` | Logging estruturado, `log_ingest_selection()`, payloads de resumo |

## `prompts/`

Templates e montagem de prompts enviados ao LLM.

| Arquivo / pasta | Descrição |
|---|---|
| `loader.py` | Carrega templates de texto e aplica limites de configuração |
| `rag.py` | Orçamento, deduplicação e seções RAG no prompt do usuário |
| `rag_headers.yaml` | Cabeçalhos das seções RAG |
| `templates/generator_system.txt` | System prompt do gerador de testes |
| `templates/repair_system.txt` | System prompt do agente de reparo |

## `parsers/`

Parsing de código-fonte e de respostas do LLM.

### `parsers/llm/`

| Arquivo | Descrição |
|---|---|
| `response.py` | Normaliza, valida e estrutura a saída do LLM (`GeneratedTest`) |

### `parsers/source/`

Análise estática de repositórios Python (antigo `ingest/`).

| Arquivo | Descrição |
|---|---|
| `scanner.py` | `RepositoryScanner` — varredura de `*.py` |
| `path_filters.py` | Exclusões centralizadas; `scan_python_files()`, `python_file_skip_reason()` |
| `symbol_filter.py` | Filtro de elegibilidade; `filter_symbols()`, `symbol_skip_reason()` |
| `parser.py` | `parse_repository_graphs()` — ponto de entrada do ingest |
| `extract.py` | `SymbolExtractor` — extração via AST; dicas para `@dataclass` |
| `ast_utils.py` | Parse de arquivo em AST (UTF-8 com/sem BOM) |
| `text_utils.py` | `read_source_text()`, `strip_utf8_bom()` |
| `call_graph.py` | `CallGraph`, `CallGraphBuilder` |
| `dependency_graph.py` | `DependencyGraph`, `DependencyGraphBuilder` |
| `import_resolver.py` | `module_name_from_path()` — caminho → módulo Python |
| `collectors/branches.py` | Contagem de branches por símbolo |
| `collectors/dependency_collector.py` | Dependências chamadas |
| `collectors/exceptions.py` | Exceções lançadas/capturadas |
| `collectors/imports.py` | Imports do arquivo |
| `heuristics/edge_cases.py` | Casos de borda heurísticos |
| `models/ExtractedSymbol.py` | Modelo do símbolo extraído |

## `cache/`

| Arquivo | Descrição |
|---|---|
| `generation_cache.py` | Cache JSON persistente de gerações aprovadas |

## `config/`

| Arquivo | Descrição |
|---|---|
| `settings.py` | Configuração Pydantic + `.env` |
| `run_profiles.py` | Perfis CLI (`--profile`): RAG + cache de geração |
| `run_workspace.py` | `RunWorkspace`, `source_slug()`, `save_ingest_artifacts()`, `save_ingest_selection()` |
| `logging_setup.py` | Logging console + arquivo |
| `source_guard.py` | Validação de `source_dir` arriscado |
| `security_paths.py` | Padrões de caminhos sensíveis e auditoria de segredos |

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
| `coverage_analyzer.py` | `CoverageAnalyzer` — pytest-cov; métricas escopadas por símbolo alvo |
| `coverage_format.py` | Formatação de intervalos de linhas (missing ranges) |
| `pytest_support.py` | Montagem de PYTHONPATH e parsing de saída do pytest |

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
| `usage_tracker.py` | `UsageTracker` — acumula tokens; `reconciliation` inclui `entrada + saída` |
| `call_logger.py` | Log persistente de chamadas LLM/embedding |
| `pricing.py` | Estimativa de custo por token |
| `sanitize.py` | Mascaramento de segredos em logs |
| `token_usage.py` | Parsing de usage da API OpenAI |

## `schemas/`

| Arquivo | Descrição |
|---|---|
| `context.py` | `FunctionContext` — entrada do gerador |
| `retrieval_context.py` | `RetrievalContext`, `RetrievalMetrics` |
| `outputs.py` | `GeneratedTest` — saída do gerador |
| `pipeline.py` | `PipelineStats`, `OrchestrationResult` |
| `prompt_utils.py` | Reexport de compatibilidade → `prompts.rag` |

## `scripts/`

| Arquivo | Descrição |
|---|---|
| `ingest_only.py` | Ingestão estática (parser + grafos + `ingest_selection.json`) |
| `run_all_profiles.py` | Executa os 4 perfis (`sem-rag` … `com-cache`) em sequência |

## `repositorios/`

Pasta opcional na raiz do engine para clones de projetos externos (ex.: `repositorios/code_katas/`). Aponte o pipeline para o subdiretório com código Python:

```bash
python scripts/ingest_only.py repositorios/code_katas/src
python main.py repositorios/code_katas/src --profile sem-rag
```

O slug em `runs/` será `repositorios_code_katas_src`.

## `main.py`

Entrypoint CLI fino. Não contém lógica de pipeline.

```python
def main(
    source_dir: str = ".",
    *,
    allow_risky_source: bool = False,
    profile: str | None = None,
) -> OrchestrationResult:
    ...
```

| Argumento CLI | Padrão | Descrição |
|---|---|---|
| `SOURCE_DIR` | `.` | Diretório Python a analisar |
| `--profile` | — | `sem-rag`, `rag-limitado`, `rag-completo`, `com-cache` |
| `--allow-risky-source` | `false` | Ignora avisos de `source_dir` arriscado |

```bash
python main.py mockes --profile rag-completo
python main.py --help
```

Ver [CLI.md](CLI.md).

| Responsabilidade | Onde fica |
|---|---|
| Parse de argumentos (`argparse`) | `main.py` |
| Perfis de teste | `config/run_profiles.py` |
| Pipeline completo | `agents/orchestrator.py` |
| Templates LLM | `prompts/templates/` |
| Parsing de resposta LLM | `parsers/llm/response.py` |
| Análise estática (AST) | `parsers/source/` |
| Configuração | `config/settings.py` |
| Workspace + artefatos | `config/run_workspace.py` |

## `tests/`

Testes unitários do engine. Usam Qdrant em memória (`:memory:`) e embedder fake (`tests/conftest.py`).

## `mockes/`

Código de exemplo (`exemplo.py`) para validar o pipeline:

```bash
python main.py mockes
python main.py mockes --profile sem-rag
```
