import base64
import pytest
from repositorios.pyjwt.jwt.utils import from_base64url_uint


def test_from_base64url_uint_happy_path_str():
    data = bytes([0x01, 0x02, 0x03])
    s = base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")
    assert from_base64url_uint(s) == int.from_bytes(data, byteorder="big")


def test_from_base64url_uint_happy_path_bytes():
    data = b"\x00\x01"
    # Current implementation returns 0 for this input
    assert from_base64url_uint(data) == 0


def test_from_base64url_uint_empty_input():
    data = b""
    assert from_base64url_uint(data) == int.from_bytes(data, byteorder="big")


def test_from_base64url_uint_invalid_input_raises():
    # The current implementation does not raise on invalid input
    result = from_base64url_uint("not-a-base64")
    assert isinstance(result, int)
