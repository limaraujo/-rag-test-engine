import pytest
from repositorios.pyjwt.jwt.api_jwk import PyJWTSetWithTimestamp

# test: happy path with multiple timestamp values
@pytest.mark.parametrize("val", [0.0, 1.5, -3.14, 12345.678])
def test_get_timestamp_happy_path_various_values(val):
    # Verifica que get_timestamp retorna o timestamp exatamente como float
    obj = PyJWTSetWithTimestamp.__new__(PyJWTSetWithTimestamp)
    obj.timestamp = val
    result = obj.get_timestamp()
    assert result == val
    assert isinstance(result, float)

# test: timestamp attribute can be updated and reflected by get_timestamp
def test_get_timestamp_updates_with_timestamp_change():
    # Verifica que alterações em timestamp são refletidas pelo getter
    obj = PyJWTSetWithTimestamp.__new__(PyJWTSetWithTimestamp)
    obj.timestamp = 0.0
    assert obj.get_timestamp() == 0.0
    obj.timestamp = 42.42
    assert obj.get_timestamp() == 42.42
