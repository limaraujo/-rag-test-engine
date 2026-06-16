import pytest
from repositorios.pyjwt.jwt.algorithms import HMACAlgorithm

# Test 1: happy path - ensure integer hash_alg is stored
def test_hmacalgorithm_init_stores_hash_alg_with_int():
    # curto: verifica que hash_alg fornecido (inteiro) é armazenado
    dummy = 123
    alg = HMACAlgorithm(hash_alg=dummy)
    assert alg.hash_alg is dummy

# Test 2: happy path - ensure string hash_alg is stored
def test_hmacalgorithm_init_stores_hash_alg_with_string():
    # curto: verifica que hash_alg fornecido (string) é armazenado
    dummy = "sha256"
    alg = HMACAlgorithm(hash_alg=dummy)
    assert alg.hash_alg is dummy

# Test 3: happy path - ensure object hash_alg is stored
def test_hmacalgorithm_init_stores_hash_alg_with_object():
    # curto: verifica que hash_alg fornecido (objeto) é armazenado
    dummy = object()
    alg = HMACAlgorithm(hash_alg=dummy)
    assert alg.hash_alg is dummy
