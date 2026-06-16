import pytest
from cryptography.hazmat.primitives import hashes
from repositorios.pyjwt.jwt.algorithms import RSAAlgorithm

# Verifica que __init__ guarda o hash_alg fornecido (casos SHA256 e SHA512)
@pytest.mark.parametrize("hash_alg", [hashes.SHA256, hashes.SHA512])
def test_rsa_algorithm_init_stores_hash_alg(hash_alg):
    algo = RSAAlgorithm(hash_alg)
    assert algo.hash_alg is hash_alg
