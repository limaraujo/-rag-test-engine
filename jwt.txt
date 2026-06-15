# Métricas — `20260615_015849`

Base: `runs/repositorios_pyjwt_jwt/20260615_015849`

## Benchmark de cache (com-cache → com-cache-rerun)

| Métrica | 1ª passagem (fria) | 2ª passagem (quente) |
| --- | --- | --- |
| Tokens | 868,566 | 859,228 |
| Chamadas LLM | 157 | 154 |
| Cache hits | 0 | 0 |
| LLM evitadas | — | 0 |
| Redução de tokens | — | **1.1%** |

## Resumo por perfil (RAG)

| Perfil | Salvos | Falharam | Válidos % | 1ª gen % | Aprovação % | Cov. linhas | Tokens | Cache hits | LLM calls |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `sem-rag` | 82 | 44 | 71.4% | 52.4% | 100.0% | 86.5% | 777,117 | 0 | 153 |
| `rag-limitado` | 95 | 31 | 80.2% | 60.3% | 100.0% | 85.6% | 845,642 | 0 | 153 |
| `rag-completo` | 96 | 29 | 81.0% | 54.0% | 100.0% | 84.4% | 864,062 | 0 | 159 |
| `com-cache` | 92 | 34 | 77.8% | 56.3% | 100.0% | 84.5% | 868,566 | 0 | 157 |

## 2ª passagem de cache (`com-cache-rerun`)

- Símbolos salvos: 92
- Tokens: 859,228
- Cache hits: 0
- LLM evitadas: 0

## Símbolos que falharam em todos os perfis RAG

- `Algorithm.prepare_key`
- `Algorithm.to_jwk`
- `ECAlgorithm.to_jwk`
- `HMACAlgorithm.prepare_key`
- `NoneAlgorithm.prepare_key`
- `OKPAlgorithm.to_jwk`
- `PyJWKClient.fetch_data`
- `PyJWKClient.get_jwk_set`
- `PyJWKClient.get_signing_keys`
- `PyJWKSet.__init__`
- `PyJWT._validate_iss`
- `RSAAlgorithm.from_jwk`
- `RSAAlgorithm.to_jwk`

## Salvos só em sem-rag

_Nenhum._

## Matriz de falhas por símbolo (perfis RAG)

| Símbolo | sem-rag | rag-limitado | rag-completo | com-cache |
| --- | --- | --- | --- | --- |
| `Algorithm.check_crypto_key_type` | FALHA (repair_skipped:pytest_collection_error) | OK | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) |
| `Algorithm.from_jwk` | FALHA (tests_failed) | OK | FALHA (tests_failed) | FALHA (repair_skipped:pytest_collection_error) |
| `Algorithm.prepare_key` | FALHA (repair_skipped:pytest_collection_error) | FALHA (tests_failed) | FALHA (repair_skipped:pytest_collection_error) | FALHA (tests_failed) |
| `Algorithm.to_jwk` | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) | FALHA (tests_failed) | FALHA (repair_skipped:pytest_collection_error) |
| `Algorithm.verify` | FALHA (repair_skipped:pytest_collection_error) | OK | FALHA (repair_skipped:pytest_collection_error) | OK |
| `ECAlgorithm._validate_curve` | FALHA (tests_failed) | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) | OK |
| `ECAlgorithm.from_jwk` | FALHA (repair_skipped:pytest_collection_error) | OK | FALHA (repair_skipped:pytest_collection_error) | FALHA (tests_failed) |
| `ECAlgorithm.prepare_key` | OK | OK | OK | FALHA (repair_skipped:pytest_collection_error) |
| `ECAlgorithm.sign` | OK | OK | OK | FALHA (repair_skipped:pytest_collection_error) |
| `ECAlgorithm.to_jwk` | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) |
| `ECAlgorithm.verify` | FALHA (tests_failed) | OK | OK | FALHA (tests_failed) |
| `HMACAlgorithm.from_jwk` | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) | OK | FALHA (repair_skipped:pytest_collection_error) |
| `HMACAlgorithm.prepare_key` | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) |
| `JWKSetCache.get` | FALHA (tests_failed) | OK | OK | OK |
| `MissingRequiredClaimError.__init__` | OK | OK | OK | FALHA (tests_failed) |
| `NoneAlgorithm.prepare_key` | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) |
| `OKPAlgorithm.from_jwk` | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) | OK | OK |
| `OKPAlgorithm.prepare_key` | OK | FALHA (tests_failed) | OK | OK |
| `OKPAlgorithm.to_jwk` | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) |
| `PyJWK.__init__` | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) | OK | FALHA (repair_skipped:pytest_collection_error) |
| `PyJWK.key_id` | OK | FALHA (tests_failed) | OK | OK |
| `PyJWKClient.__init__` | FALHA (tests_failed) | OK | FALHA (repair_skipped:pytest_collection_error) | FALHA (tests_failed) |
| `PyJWKClient.fetch_data` | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) | FALHA (error:closing parenthesis '}' does not match opening parenthesis '[' (<unknown>, line 98)) | FALHA (repair_skipped:pytest_collection_error) |
| `PyJWKClient.get_jwk_set` | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) | FALHA (tests_failed) | FALHA (tests_failed) |
| `PyJWKClient.get_signing_key` | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) | OK | OK |
| `PyJWKClient.get_signing_keys` | FALHA (repair_skipped:pytest_collection_error) | FALHA (tests_failed) | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) |
| `PyJWKClient.match_kid` | OK | OK | FALHA (repair_skipped:pytest_collection_error) | OK |
| `PyJWKSet.__init__` | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) | FALHA (tests_failed) | FALHA (tests_failed) |
| `PyJWKSet.__iter__` | FALHA (tests_failed) | OK | OK | FALHA (repair_skipped:pytest_collection_error) |
| `PyJWKSet.from_dict` | FALHA (tests_failed) | OK | OK | OK |
| `PyJWKSet.from_json` | FALHA (repair_skipped:pytest_collection_error) | OK | OK | OK |
| `PyJWS.__init__` | OK | OK | FALHA (repair_skipped:pytest_collection_error) | OK |
| `PyJWS._load` | FALHA (repair_skipped:pytest_collection_error) | OK | OK | FALHA (tests_failed) |
| `PyJWS._validate_crit` | OK | OK | OK | FALHA (repair_skipped:pytest_collection_error) |
| `PyJWS._validate_kid` | FALHA (repair_skipped:pytest_collection_error) | OK | OK | OK |
| `PyJWS._verify_signature` | OK | FALHA (repair_skipped:pytest_collection_error) | OK | OK |
| `PyJWS.decode` | OK | FALHA (repair_skipped:pytest_collection_error) | OK | FALHA (repair_skipped:pytest_collection_error) |
| `PyJWS.decode_complete` | FALHA (tests_failed) | FALHA (tests_failed) | FALHA (repair_skipped:pytest_collection_error) | OK |
| `PyJWS.get_algorithm_by_name` | FALHA (repair_skipped:pytest_collection_error) | OK | OK | OK |
| `PyJWS.register_algorithm` | FALHA (repair_skipped:pytest_collection_error) | OK | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) |
| `PyJWT._decode_payload` | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) | OK | OK |
| `PyJWT._merge_options` | FALHA (tests_failed) | OK | OK | OK |
| `PyJWT._validate_aud` | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) | OK | FALHA (repair_skipped:pytest_collection_error) |
| `PyJWT._validate_exp` | OK | FALHA (repair_skipped:pytest_collection_error) | OK | OK |
| `PyJWT._validate_iat` | FALHA (repair_skipped:pytest_collection_error) | OK | OK | OK |
| `PyJWT._validate_iss` | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) |
| `PyJWT._validate_jti` | OK | OK | FALHA (tests_failed) | OK |
| `PyJWT._validate_required_claims` | OK | FALHA (tests_failed) | OK | OK |
| `PyJWT._validate_sub` | FALHA (tests_failed) | OK | OK | OK |
| `PyJWT.decode` | FALHA (tests_failed) | OK | OK | OK |
| `RSAAlgorithm.from_jwk` | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) |
| `RSAAlgorithm.prepare_key` | FALHA (repair_skipped:pytest_collection_error) | FALHA (tests_failed) | OK | OK |
| `RSAAlgorithm.to_jwk` | FALHA (repair_skipped:pytest_collection_error) | FALHA (repair_skipped:pytest_collection_error) | FALHA (tests_failed) | FALHA (repair_skipped:pytest_collection_error) |
| `RSAAlgorithm.verify` | FALHA (repair_skipped:pytest_collection_error) | OK | OK | OK |
| `RSAPSSAlgorithm.sign` | OK | FALHA (tests_failed) | OK | OK |
| `get_default_algorithms` | OK | OK | OK | FALHA (tests_failed) |
| `is_ssh_key` | OK | OK | FALHA (repair_skipped:pytest_collection_error) | OK |
| `to_base64url_uint` | OK | OK | OK | FALHA (tests_failed) |

