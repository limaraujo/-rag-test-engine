# Métricas — `20260615_000809`

Base: `runs\repositorios_code_katas_src\20260615_000809`

## Resumo por perfil

| Perfil | Salvos | Falharam | Válidos % | 1ª gen % | Aprovação % | Cov. linhas | Cov. branches | Tokens | Chamadas LLM | Reparos | s/símbolo | Produtiv. | Testes valid. |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `sem-rag` | 49 | 9 | 86.2% | 75.9% | 100.0% | 98.1% | 97.1% | 223,508 | 64 | 5 | 22.18s | 0.77 | 198 |
| `rag-limitado` | 47 | 11 | 86.2% | 79.3% | 100.0% | 99.1% | 98.8% | 227,066 | 62 | 1 | 23.91s | 0.76 | 196 |
| `rag-completo` | 47 | 11 | 86.2% | 79.3% | 100.0% | 99.0% | 98.5% | 216,233 | 62 | 1 | 21.68s | 0.76 | 179 |
| `com-cache` | 47 | 11 | 86.2% | 77.6% | 100.0% | 98.7% | 98.0% | 242,259 | 63 | 2 | 25.48s | 0.75 | 190 |

## Símbolos que falharam em todos os perfis

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

- `Trie.traversal`

## Matriz de falhas por símbolo

| Símbolo | sem-rag | rag-limitado | rag-completo | com-cache |
| --- | --- | --- | --- | --- |
| `Autocomplete.__init__` | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) |
| `Autocomplete._autocomplete` | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) |
| `Autocomplete.autocomplete` | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) |
| `Trie.__init__` | FALHA (tests_failed) | FALHA (tests_failed) | FALHA (tests_failed) | FALHA (tests_failed) |
| `Trie._traversal` | OK | OK | FALHA (tests_failed) | FALHA (tests_failed) |
| `Trie.remove` | OK | FALHA (tests_failed) | OK | OK |
| `Trie.traversal` | OK | FALHA (tests_failed) | FALHA (tests_failed) | FALHA (tests_failed) |
| `calculate_distance` | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) |
| `create_graph` | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) |
| `flight_path` | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) |
| `get_json` | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) |
| `lat_long_dict` | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) |
