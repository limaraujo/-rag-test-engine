# API dos agentes

Referência programática dos componentes principais.

## CLI: `main.py`

**Sintaxe:**

```bash
uv run python main.py [SOURCE_DIR] [--profile PERFIL]
uv run python main.py --help
```

| Argumento | Padrão | Descrição |
|---|---|---|
| `SOURCE_DIR` | `.` | Diretório Python a analisar |
| `--profile` | — | `sem-rag`, `rag-limitado`, `rag-completo`, `com-cache` |
| `--allow-risky-source` | `false` | Ignora avisos de `source_dir` arriscado |

Demais opções (modelo, Qdrant, `LOG_API_CALLS`, RAG, cache) vêm do `.env` ou do perfil — ver [CLI.md](CLI.md) e [CONFIGURATION.md](CONFIGURATION.md).

## Entrypoint: `main()`

**Arquivo:** `main.py`

Ponto de entrada da CLI. Delega ao orquestrador e retorna o resultado.

```python
from main import main

result = main("mockes")                          # defaults do .env
result = main("mockes", profile="rag-completo")  # perfil de teste
result = main()                                  # diretório atual (".")

assert result.stats.ok >= 0
print(result.workspace.tests_dir)
```

**Com perfil programático:**

```python
from config.run_profiles import apply_run_profile
from agents.orchestrator import OrchestratorAgent

with apply_run_profile("sem-rag"):
    result = OrchestratorAgent().run("mockes")
```

Equivalente direto (sem perfil):

```python
from agents.orchestrator import OrchestratorAgent

orchestrator = OrchestratorAgent()
result = orchestrator.run("mockes")
```

---

## OrchestratorAgent

**Arquivo:** `agents/orchestrator.py`

Orquestra o pipeline completo.

```python
from agents.orchestrator import OrchestratorAgent

agent = OrchestratorAgent(
    retriever=None,       # Retriever() por padrão
    generator=None,       # TestGeneratorAgent() por padrão
    runner=None,          # TestRunner() por padrão
    repair_agent=None,    # RepairAgent() por padrão
    max_repairs=2,
)

result = agent.run("mockes")
```

### Retorno: `OrchestrationResult`

```python
result.workspace.root          # Path: runs/mockes/20260609_...
result.workspace.tests_dir     # Path: .../tests
result.workspace.artifacts_dir # Path: .../artifacts
result.stats.ok                # testes salvos
result.stats.failed            # testes descartados
result.stats.skipped           # erros de geração
result.stats.repaired          # salvos após reparo
result.stats.coverage_boosted  # salvos após boost de cobertura
result.generation_cache        # GenerationCacheStats (hits, misses, …)
result.indexed                 # símbolos indexados no Qdrant
result.cache_hits              # símbolos reutilizados do cache de embeddings
result.token_summary           # str com uso de tokens (ou None)
```

`run_summary.json` inclui `stats.run_profile`, `stats.rag_mode` e `stats.generation_cache_enabled`.

---

## RunProfile

**Arquivo:** `config/run_profiles.py`

```python
from config.run_profiles import apply_run_profile, PROFILES, describe_profiles

print(describe_profiles())

with apply_run_profile("rag-limitado"):
    # settings.RAG_MODE == "limited" durante o bloco
    ...
```

| Perfil | `rag_mode` | `generation_cache_enabled` |
|---|---|---|
| `sem-rag` | `none` | `False` |
| `rag-limitado` | `limited` | `False` |
| `rag-completo` | `full` | `False` |
| `com-cache` | `full` | `True` |

---

## TestGeneratorAgent

**Arquivo:** `agents/test_generator.py`

Gera um arquivo pytest a partir de `FunctionContext`. Usa `prompts/loader.py` para o system prompt.

```python
from agents.test_generator import TestGeneratorAgent
from schemas.context import FunctionContext

agent = TestGeneratorAgent()
ctx = FunctionContext.from_symbol(symbol, project_root=ROOT)
test = agent.generate(ctx)

print(test.full_code)    # código completo com imports
print(test.imports)      # linhas de import extraídas
print(test.coverage_hints)
```

O parsing da resposta LLM fica em `parsers/llm/response.py` (`parse_response`).

---

## RepairAgent

**Arquivo:** `agents/repair.py`

Corrige teste que falhou no pytest.

```python
from agents.repair import RepairAgent

repair = RepairAgent()
fixed = repair.repair(
    ctx,              # FunctionContext original
    failing_test,     # GeneratedTest
    run_result,       # RunResult do pytest
    attempt=1,
)
```

---

## Retriever

**Arquivo:** `retrieval/retriever.py`

Indexação e enriquecimento RAG.

```python
from retrieval.retriever import Retriever

retriever = Retriever()

# Indexar símbolos no Qdrant
indexed, skipped = retriever.index_symbols(symbols)

# Enriquecer contexto com RAG híbrido
ctx = FunctionContext.from_symbol(symbol, project_root=ROOT)
enriched = retriever.enrich(
    ctx,
    symbol,
    call_graph=call_graph,
    dependency_graph=dependency_graph,
    symbols_by_name=symbols_by_name,
    project_root=source_dir,
)
```

---

## TestRunner

**Arquivo:** `execution/runner.py`

```python
from execution.runner import TestRunner

runner = TestRunner()
result = runner.run(test, pythonpath=[str(ROOT)], timeout=30)

result.passed        # bool
result.exit_code     # código do pytest
result.failure_summary  # trecho de erro para o LLM
result.num_passed
```

---

## CoverageAnalyzer

**Arquivo:** `execution/coverage_analyzer.py`

```python
from execution.coverage_analyzer import CoverageAnalyzer

analyzer = CoverageAnalyzer(
    test,
    target_file_path,
    target_function="Calculadora.divide",
    pythonpath=[str(ROOT)],
    threshold=80.0,
)
analyzer.run()
summary = analyzer.generate_summary()
gaps = analyzer.gaps_for_prompt()
```

---

## LLM Factory

**Arquivo:** `llm/factory.py`

```python
from llm.factory import get_llm, get_embedder

llm = get_llm()           # OpenAILLM ou MockLLM
embedder = get_embedder() # OpenAIEmbedding ou LocalEmbedding
```

### Uso de tokens

```python
from llm.usage_tracker import get_tracker, reset_tracker

reset_tracker()
# ... chamadas LLM/embeddings ...
print(get_tracker().format_summary())
```

Cada `LLMResponse` e `LLMEmbeddingResponse` expõe `.usage` (`TokenUsage`).

Com `LOG_API_CALLS=true` (padrão), cada chamada também é gravada em
`runs/.../logs/api_calls/` — ver [CLI.md](CLI.md).

---

## RunWorkspace

**Arquivo:** `config/run_workspace.py`

```python
from config.run_workspace import RunWorkspace, save_ingest_artifacts

workspace = RunWorkspace.create(Path("mockes"))
# workspace.root, .tests_dir, .logs_dir, .artifacts_dir

save_ingest_artifacts(workspace, symbols=..., call_graph=..., dependency_graph=...)
```

---

## FunctionContext

**Arquivo:** `schemas/context.py`

```python
from schemas.context import FunctionContext
from config.settings import ROOT

ctx = FunctionContext.from_symbol(symbol, project_root=ROOT)
prompt = ctx.to_prompt_block()  # texto para o LLM
```

Campos RAG (`related_functions`, `similar_tests`) são preenchidos pelo `Retriever` quando `RAG_MODE != "none"`.

Montagem do bloco RAG no prompt: `prompts/rag.py` (`build_rag_prompt_sections`).

---

## parse_response (LLM)

**Arquivo:** `parsers/llm/response.py`

```python
from parsers.llm.response import parse_response, normalize_code_response

test = parse_response(raw_llm_output, ctx)
```

---

## GeneratedTest

**Arquivo:** `schemas/outputs.py`

```python
from schemas.outputs import GeneratedTest

test.target_function  # "Calculadora.divide"
test.code             # arquivo completo
test.full_code        # alias de code
test.imports          # ["from mockes.exemplo import Calculadora", ...]
```
