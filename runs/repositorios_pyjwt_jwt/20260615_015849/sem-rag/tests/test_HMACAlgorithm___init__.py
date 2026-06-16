import hashlib
from repositorios.pyjwt.jwt.algorithms import HMACAlgorithm



# Test that __init__ stores the hash_alg argument on the instance (happy path)
class DummyHash:
    pass


# Test that __init__ stores distinct hash_alg for multiple instances
def test_hmac_algorithm_init_stores_distinct_hash_alg_per_instance():
    h1 = object()
    h2 = object()
    a1 = HMACAlgorithm(h1)
    a2 = HMACAlgorithm(h2)
    assert a1.hash_alg is h1
    assert a2.hash_alg is h2


# Test that __init__ stores the provided hash_alg (including real hashlib object)
def test_hmac_algorithm_init_stores_provided_hash_alg():
    dummy = DummyHash()
    alg = HMACAlgorithm(dummy)
    assert alg.hash_alg is dummy


def test_hmac_algorithm_init_stores_hashlib_object():
    h = hashlib.sha256()
    alg = HMACAlgorithm(h)
    assert alg.hash_alg is h
