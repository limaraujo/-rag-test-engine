import pytest
from repositorios.pyjwt.jwt.utils import base64url_encode

# happy path: verify multiple inputs produce expected base64url-encoded outputs without padding
@pytest.mark.parametrize("inp, expected", [
    (b"", b""),
    (b"a", b"YQ"),
    (b"aa", b"YWE"),
    (b"hello", b"aGVsbG8"),
])
def test_base64url_encode_happy_path(inp: bytes, expected: bytes):
    assert base64url_encode(inp) == expected

# exception path: non-bytes input should raise TypeError
def test_base64url_encode_raises_type_error_on_non_bytes():
    with pytest.raises(TypeError):
        base64url_encode("not bytes")
