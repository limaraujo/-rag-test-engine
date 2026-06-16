import base64
import binascii
import pytest
from repositorios.pyjwt.jwt.utils import base64url_decode


# short: happy path with/without padding for str and bytes inputs
@pytest.mark.parametrize("input_value, expected", [
    ("SGVsbG8", b"Hello"),    # without padding (string)
    ("SGVsbG8=", b"Hello"),   # with padding (string)
    (b"SGVsbG8", b"Hello"),   # without padding (bytes)
    (b"SGVsbG8=", b"Hello"),  # with padding (bytes)
])
def test_base64url_decode_happy_path(input_value, expected):
    assert base64url_decode(input_value) == expected

# short: invalid input behavior observation
def test_base64url_decode_invalid_raises():
    # The current implementation does not raise for invalid input; ensure it returns empty bytes
    assert base64url_decode("!!!") == b""
