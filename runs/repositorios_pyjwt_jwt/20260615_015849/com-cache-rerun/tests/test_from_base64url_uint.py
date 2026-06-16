import pytest
from repositorios.pyjwt.jwt.utils import from_base64url_uint

# curto: caminho feliz com string base64url sem padding que representa 1
def test_from_base64url_uint_happy_path_str():
    assert from_base64url_uint("AQ") == 1

# curto: caminho feliz com input bytes sem padding representando 15
def test_from_base64url_uint_happy_path_bytes():
    assert from_base64url_uint(b"Dw") == 15

# curto: caminho feliz com multi-byte value (0x010203) codificado com base64url sem padding
def test_from_base64url_uint_happy_path_multibyte():
    assert from_base64url_uint("AQID") == 66051

# curto: entrada de tipo inválido levanta TypeError
def test_from_base64url_uint_invalid_type_raises():
    with pytest.raises(TypeError):
        from_base64url_uint(123)
