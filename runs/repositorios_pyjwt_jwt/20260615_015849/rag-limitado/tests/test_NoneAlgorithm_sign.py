import pytest
from repositorios.pyjwt.jwt.algorithms import NoneAlgorithm

# Verifica: sign retorna bytes vazios para entradas variadas (happy path e key não-None)
@pytest.mark.parametrize("msg, key", [
    (b"hello", None),
    (b"", None),
    (b"data", 12345),
])
def test_none_algorithm_sign_returns_empty_bytes_for_various_inputs(msg, key):
    alg = NoneAlgorithm()
    assert alg.sign(msg, key) == b""
