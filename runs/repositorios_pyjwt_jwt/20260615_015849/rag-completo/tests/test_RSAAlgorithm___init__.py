from cryptography.hazmat.primitives import hashes
import pytest
from repositorios.pyjwt.jwt.algorithms import RSAAlgorithm

# happy path: ensure RSAAlgorithm.__init__ assigns the provided hash algorithm type
@pytest.mark.parametrize("hash_alg", [hashes.SHA256, hashes.SHA384, hashes.SHA512])
def test_rsa_algorithm_init_stores_hash_alg(hash_alg):
    rsa = RSAAlgorithm(hash_alg)
    assert rsa.hash_alg is hash_alg
