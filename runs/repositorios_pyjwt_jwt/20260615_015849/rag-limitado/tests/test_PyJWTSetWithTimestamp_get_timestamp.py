import pytest
from repositorios.pyjwt.jwt.api_jwk import PyJWTSetWithTimestamp

# Verifica que get_timestamp retorna o timestamp armazenado para vários valores numéricos (path happy e bordas)
@pytest.mark.parametrize("ts", [1.23, 0, -5.0, 42])
def test_get_timestamp_returns_stored_timestamp(ts):
    obj = object.__new__(PyJWTSetWithTimestamp)
    obj.timestamp = ts
    assert obj.get_timestamp() == ts
