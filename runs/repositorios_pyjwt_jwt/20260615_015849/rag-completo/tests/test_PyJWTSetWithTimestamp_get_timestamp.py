import pytest
from repositorios.pyjwt.jwt.api_jwk import PyJWTSetWithTimestamp

# Verifica o retorno de get_timestamp corresponde ao atributo timestamp (caminho feliz)
@pytest.mark.parametrize("ts", [0.0, 1.5, -2.25, 1234567890.123])
def test_get_timestamp_returns_stored_timestamp(ts):
    obj = PyJWTSetWithTimestamp.__new__(PyJWTSetWithTimestamp)
    obj.timestamp = ts
    result = obj.get_timestamp()
    assert isinstance(result, float)
    assert result == ts
