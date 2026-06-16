import pytest
from repositorios.pyjwt.jwt.api_jwk import PyJWTSetWithTimestamp

# Verifica que get_timestamp retorna o valor armazenado em timestamp para diversos valores numéricos (caminho feliz)
@pytest.mark.parametrize("value", [0.0, 1.23, -5.0, 1e9])
def test_get_timestamp_returns_internal_value(value):
    inst = PyJWTSetWithTimestamp.__new__(PyJWTSetWithTimestamp)
    inst.timestamp = value
    assert inst.get_timestamp() == value
