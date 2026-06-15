import pytest
from repositorios.pyjwt.jwt.utils import base64url_decode


# curto: happy path - decodifica string sem padding (rem > 0)
def test_base64url_decode_str_no_padding():
    s = "SGVsbG8"  # "Hello" sem padding
    assert base64url_decode(s) == b"Hello"

# curto: path com padding já presente (rem == 0)
def test_base64url_decode_str_with_padding():
    s = "SGVsbG8="  # "Hello" com padding
    assert base64url_decode(s) == b"Hello"

# curto: aceitação de input em bytes sem padding (rem > 0)
def test_base64url_decode_bytes_no_padding():
    b = b"SGVsbG8"  # "Hello" sem padding
    assert base64url_decode(b) == b"Hello"
