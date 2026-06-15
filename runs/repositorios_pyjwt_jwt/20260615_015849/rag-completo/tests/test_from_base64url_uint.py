import base64
import pytest
from repositorios.pyjwt.jwt.utils import from_base64url_uint

# curto: happy path — valida conversão base64url para int usando string e bytes com vários valores
@pytest.mark.parametrize("value", [0, 1, 123456789])
def test_from_base64url_uint_happy_path_string_and_bytes(value):
    bit_length = max(1, (value.bit_length() + 7) // 8)
    data = value.to_bytes(bit_length, byteorder="big")

    encoded_str = base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")
    encoded_bytes = base64.urlsafe_b64encode(data).rstrip(b"=")

    assert from_base64url_uint(encoded_str) == value
    assert from_base64url_uint(encoded_bytes) == value

# curto: borda com leading zeros — garante que zeros à esquerda não alteram o valor
def test_from_base64url_uint_with_leading_zero_bytes():
    data = b"\x00\x01"  # valor esperado = 1
    encoded_str = base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")
    encoded_bytes = base64.urlsafe_b64encode(data).rstrip(b"=")

    assert from_base64url_uint(encoded_str) == 1
    assert from_base64url_uint(encoded_bytes) == 1

# curto: tratamento de erro — entrada não suportada levanta TypeError
def test_from_base64url_uint_raises_on_invalid_input_type():
    with pytest.raises(TypeError):
        from_base64url_uint(123)
