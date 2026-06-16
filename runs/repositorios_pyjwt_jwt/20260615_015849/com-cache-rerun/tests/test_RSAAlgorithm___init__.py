import pytest
from cryptography.hazmat.primitives import hashes
from repositorios.pyjwt.jwt.algorithms import RSAAlgorithm

# Happy path: verify RSAAlgorithm.__init__ stores the provided hash algorithm type
@pytest.mark.parametrize("hash_alg", [hashes.SHA256, hashes.SHA384, hashes.SHA512])
def test_rsa_algorithm_init_stores_hash_alg(hash_alg):
    rsa = RSAAlgorithm(hash_alg)
    assert rsa.hash_alg is hash_alg
