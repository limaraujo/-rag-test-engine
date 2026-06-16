import pytest
from repositorios.pyjwt.jwt.api_jwk import PyJWTSetWithTimestamp

# happy path: get_jwk_set retorna o valor armazenado para diferentes tipos de valor
@pytest.mark.parametrize("value", [123, "abc", {"a": 1}, [1, 2, 3], None, object()])
def test_get_jwk_set_returns_stored_value(value):
    inst = PyJWTSetWithTimestamp.__new__(PyJWTSetWithTimestamp)
    inst.jwk_set = value
    assert inst.get_jwk_set() is value
