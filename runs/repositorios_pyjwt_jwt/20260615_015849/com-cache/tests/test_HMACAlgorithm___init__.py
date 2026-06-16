import hashlib
import pytest
from repositorios.pyjwt.jwt.algorithms import HMACAlgorithm


# Verifica que __init__ armazena o hash_alg fornecido (caminho feliz com diferentes hash_alg)
@pytest.mark.parametrize("hash_alg", [hashlib.sha256(), hashlib.sha1(), object()])
def test_hmacalgorithm_init_stores_hash_alg(hash_alg):
    alg = HMACAlgorithm(hash_alg)
    assert alg.hash_alg is hash_alg
