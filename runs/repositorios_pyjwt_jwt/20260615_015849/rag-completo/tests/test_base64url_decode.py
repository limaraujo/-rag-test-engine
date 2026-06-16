import pytest
from repositorios.pyjwt.jwt.utils import base64url_decode


def test_base64url_decode_happy_path_no_padding():
    input_val = "SGVsbG8"  # "Hello" base64url without '='
    assert base64url_decode(input_val) == b"Hello"


def test_base64url_decode_with_padding():
    input_val = "SGVsbG8="  # "Hello" with padding
    assert base64url_decode(input_val) == b"Hello"


def test_base64url_decode_bytes_input():
    input_val = b"SGVsbG8"  # bytes input
    assert base64url_decode(input_val) == b"Hello"


def test_base64url_decode_invalid_input_results_bytes():
    input_val = "!!!"
    result = base64url_decode(input_val)
    assert isinstance(result, (bytes, bytearray))
