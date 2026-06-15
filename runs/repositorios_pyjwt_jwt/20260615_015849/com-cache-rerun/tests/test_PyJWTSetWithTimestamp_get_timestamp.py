import pytest
from repositorios.pyjwt.jwt.api_jwk import PyJWTSetWithTimestamp


# teste: happy path - get_timestamp devolve o timestamp configurado (float values)
@pytest.mark.parametrize("ts", [0.0, 1.23, -5.0, 1e6])
def test_get_timestamp_returns_configured_timestamp(ts):
    inst = PyJWTSetWithTimestamp.__new__(PyJWTSetWithTimestamp)
    inst.timestamp = ts
    assert inst.get_timestamp() == ts

# teste: mudança de timestamp é refletida por get_timestamp
def test_get_timestamp_reflects_timestamp_changes():
    inst = PyJWTSetWithTimestamp.__new__(PyJWTSetWithTimestamp)
    inst.timestamp = 0.0
    assert inst.get_timestamp() == 0.0
    inst.timestamp = 42.42
    assert inst.get_timestamp() == 42.42
