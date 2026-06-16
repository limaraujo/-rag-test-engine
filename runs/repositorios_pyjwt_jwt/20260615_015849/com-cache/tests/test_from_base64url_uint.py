import pytest
from repositorios.pyjwt.jwt.utils import from_base64url_uint

# Verifica happy path com string base64url sem padding que representa 1
def test_from_base64url_uint_happy_path_str():
    assert from_base64url_uint("AQ") == 1

# Verifica happy path com input bytes sem padding que representa 1
def test_from_base64url_uint_happy_path_bytes():
    assert from_base64url_uint(b"AQ") == 1

# Verifica que código lida com múltiplos bytes (0x0102 -> 258) via string
def test_from_base64url_uint_multi_byte_str():
    assert from_base64url_uint("AQI") == 258

# Verifica que tipos inválidos levantam TypeError
def test_from_base64url_uint_invalid_input_type_raises():
    with pytest.raises(TypeError):
        from_base64url_uint(123)
