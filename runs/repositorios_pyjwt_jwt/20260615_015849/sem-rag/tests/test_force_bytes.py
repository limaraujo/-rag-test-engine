import pytest
from repositorios.pyjwt.jwt.utils import force_bytes

# Verifica a conversão de string para bytes usando UTF-8 (happy path)
def test_force_bytes_from_str():
    assert force_bytes("hello") == b"hello"

# Verifica que bytes já fornecidos são retornados como bytes idênticos (happy path)
def test_force_bytes_from_bytes():
    b = b"world"
    assert force_bytes(b) == b

# Verifica que tipos incompatíveis levantam TypeError (exceção explicitamente listada)
def test_force_bytes_invalid_type_raises_type_error():
    with pytest.raises(TypeError) as exc:
        force_bytes(123)
    assert str(exc.value) == "Expected a string value"
