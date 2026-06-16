import pytest
from repositorios.pyjwt.jwt.utils import to_base64url_uint

@pytest.mark.parametrize("val, expected", [
    (0, b"AA"),
    (5, b"BQ"),
    (255, b"_w"),
])
def test_to_base64url_uint_happy_path(val, expected):
    assert to_base64url_uint(val) == expected

def test_to_base64url_uint_negative_raises():
    with pytest.raises(ValueError, match="Must be a positive integer"):
        to_base64url_uint(-1)

def test_to_base64url_uint_with_bit_length_override():
    assert to_base64url_uint(1, bit_length=16) == b"AAE"
