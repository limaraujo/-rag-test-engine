import pytest
from repositorios.pyjwt.jwt.api_jws import PyJWS

# Verifica o caminho feliz com algoritmos válidos e o caso com lista vazia
@pytest.mark.parametrize("valids", [
    {"HS256", "RS256"},
    set(),
])
def test_get_algorithms_returns_expected(valids):
    inst = object.__new__(PyJWS)
    inst._valid_algs = valids
    result = inst.get_algorithms()
    assert isinstance(result, list)
    assert set(result) == valids
