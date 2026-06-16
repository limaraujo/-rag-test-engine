import base64
import pytest
from repositorios.pyjwt.jwt.utils import from_base64url_uint

def to_base64url_uint(n: int) -> str:
    data_len = max(1, (n.bit_length() + 7) // 8)
    data = n.to_bytes(data_len, byteorder="big")
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")

# Testa conversão de base64url para inteiro a partir de string (happy path)
@pytest.mark.parametrize("num", [0, 1, 255, 256, 9223372036854775807, 123456789])
def test_from_base64url_uint_str_input(num):
    s = to_base64url_uint(num)
    assert from_base64url_uint(s) == num

# Testa conversão de base64url para inteiro a partir de bytes (entrada do tipo bytes)
@pytest.mark.parametrize("num", [0, 1, 255, 256, 9223372036854775807, 123456789])
def test_from_base64url_uint_bytes_input(num):
    s = to_base64url_uint(num)
    b = s.encode("ascii")
    assert from_base64url_uint(b) == num
