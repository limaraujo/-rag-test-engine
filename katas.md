# Métricas — `20260615_015634`

Base: `runs/repositorios_code_katas_src/20260615_015634`

## Benchmark de cache (com-cache → com-cache-rerun)

| Métrica | 1ª passagem (fria) | 2ª passagem (quente) |
| --- | --- | --- |
| Tokens | 237,656 | 197,487 |
| Chamadas LLM | 64 | 52 |
| Cache hits | 0 | 12 |
| LLM evitadas | — | 12 |
| Redução de tokens | — | **16.9%** |

## Resumo por perfil (RAG)

| Perfil | Salvos | Falharam | Válidos % | 1ª gen % | Aprovação % | Cov. linhas | Tokens | Cache hits | LLM calls |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `sem-rag` | 47 | 11 | 86.2% | 75.9% | 100.0% | 99.2% | 226,209 | 0 | 64 |
| `rag-limitado` | 47 | 11 | 86.2% | 77.6% | 100.0% | 98.8% | 235,793 | 0 | 63 |
| `rag-completo` | 48 | 9 | 86.2% | 74.1% | 100.0% | 99.8% | 223,044 | 0 | 64 |
| `com-cache` | 47 | 11 | 86.2% | 75.9% | 100.0% | 96.9% | 237,656 | 0 | 64 |

## 2ª passagem de cache (`com-cache-rerun`)

- Símbolos salvos: 47
- Tokens: 197,487
- Cache hits: 12
- LLM evitadas: 12

## Símbolos que falharam em todos os perfis RAG

- `Autocomplete.__init__`
- `Autocomplete._autocomplete`
- `Autocomplete.autocomplete`
- `Trie.__init__`
- `calculate_distance`
- `create_graph`
- `flight_path`
- `get_json`
- `lat_long_dict`

## Salvos só em sem-rag

_Nenhum._

## Matriz de falhas por símbolo (perfis RAG)

| Símbolo | sem-rag | rag-limitado | rag-completo | com-cache |
| --- | --- | --- | --- | --- |
| `Autocomplete.__init__` | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) |
| `Autocomplete._autocomplete` | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) |
| `Autocomplete.autocomplete` | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) |
| `DoubleLink.balanced` | OK | OK | FALHA (tests_failed) | OK |
| `Graph.del_edge` | OK | OK | OK | FALHA (tests_failed) |
| `Trie.__init__` | FALHA (tests_failed) | FALHA (tests_failed) | FALHA (tests_failed) | FALHA (tests_failed) |
| `Trie._traversal` | OK | OK | OK | FALHA (tests_failed) |
| `Trie.remove` | FALHA (tests_failed) | FALHA (tests_failed) | OK | OK |
| `Trie.traversal` | FALHA (tests_failed) | OK | OK | OK |
| `calculate_distance` | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) |
| `create_graph` | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) | FALHA (error:expected '(' (<unknown>, line 36)) | FALHA (repair_skipped:pytest_collection_error) |
| `flight_path` | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) |
| `get_json` | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) |
| `lat_long_dict` | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) |
| `watch_pyramid_from_above` | OK | FALHA (tests_failed) | OK | OK |

