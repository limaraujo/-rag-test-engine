from cryptography.hazmat.primitives import hashes
import pytest
from repositorios.pyjwt.jwt.algorithms import RSAAlgorithm

# Verifica o caminho feliz: atribuição do hash_alg passado (SHA256, SHA384)
@pytest.mark.parametrize("hash_alg", [hashes.SHA256, hashes.SHA384])
def test_rsa_algorithm_init_sets_hash_alg(hash_alg):
    alg = RSAAlgorithm(hash_alg=hash_alg)
    assert alg.hash_alg is hash_alg
