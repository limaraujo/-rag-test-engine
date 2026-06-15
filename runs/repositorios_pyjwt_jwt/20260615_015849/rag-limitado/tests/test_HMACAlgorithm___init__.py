import hashlib
from repositorios.pyjwt.jwt.algorithms import HMACAlgorithm

# happy path: armazena o hash_alg fornecido
def test_hmacalgorithm_init_stores_provided_hashlib_hash():
    ha = hashlib.sha256()
    alg = HMACAlgorithm(hash_alg=ha)
    assert alg.hash_alg is ha
