import pytest
from cryptography.hazmat.primitives import hashes
from repositorios.pyjwt.jwt.algorithms import RSAAlgorithm

# happy path: verifica que RSAAlgorithm armazena o hash_alg fornecido (SHA256)
def test_rsa_algorithm_init_stores_hash_alg_sha256():
    algo = RSAAlgorithm(hash_alg=hashes.SHA256)
    assert algo.hash_alg is hashes.SHA256

# variety: verifica compatibilidade com vários algoritmos de hash
@pytest.mark.parametrize("hash_alg_class", [hashes.SHA256, hashes.SHA384, hashes.SHA512])
def test_rsa_algorithm_init_stores_hash_alg_various(hash_alg_class):
    algo = RSAAlgorithm(hash_alg=hash_alg_class)
    assert algo.hash_alg is hash_alg_class
