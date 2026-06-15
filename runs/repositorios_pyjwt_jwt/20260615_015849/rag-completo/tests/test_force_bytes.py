import pytest
from repositorios.pyjwt.jwt.utils import force_bytes

# short: happy path - ascii string to UTF-8 bytes
def test_force_bytes_from_ascii_string():
    assert force_bytes("abc") == b"abc"

# short: unicode string is encoded in UTF-8
def test_force_bytes_from_unicode_string():
    assert force_bytes("é") == "é".encode("utf-8")

# short: bytes input is returned unchanged (same object)
def test_force_bytes_from_bytes_returns_same_object():
    data = b"data"
    assert force_bytes(data) is data

# short: invalid type raises TypeError with expected message
def test_force_bytes_raises_TypeError_for_invalid_type():
    with pytest.raises(TypeError) as exc:
        force_bytes(123)
    assert str(exc.value) == "Expected a string value"
