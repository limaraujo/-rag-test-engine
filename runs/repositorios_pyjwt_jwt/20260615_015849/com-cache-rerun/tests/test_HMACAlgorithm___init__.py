import pytest
from repositorios.pyjwt.jwt.algorithms import HMACAlgorithm

# curto: dummy hash class para simular HashlibHash
class DummyHash:
    pass


# curto: happy path - garante que __init__ armazena o hash_alg fornecido
def test_hmac_algorithm_init_happy_path_sets_hash_alg():
    dummy = DummyHash()
    alg = HMACAlgorithm(dummy)
    assert alg.hash_alg is dummy

# curto: cenários variáveis - verifica que diferentes tipos de input são aceitos e mantêm a referência
@pytest.mark.parametrize("value", [123, None, "sha256", DummyHash()])
def test_hmac_algorithm_init_accepts_various_types(value):
    alg = HMACAlgorithm(value)
    assert alg.hash_alg is value
