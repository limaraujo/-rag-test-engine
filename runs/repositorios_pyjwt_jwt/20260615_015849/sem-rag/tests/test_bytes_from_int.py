import pytest
from repositorios.pyjwt.jwt.utils import bytes_from_int

# happy path: default bit_length=None with a small positive integer
def test_bytes_from_int_default_length():
    assert bytes_from_int(1) == b"\x01"

# branch: explicit bit_length provided affecting the output length
def test_bytes_from_int_with_explicit_bit_length():
    assert bytes_from_int(255, bit_length=16) == b"\x00\xff"

# edge case: zero value returns empty bytes when bit_length is None
def test_bytes_from_int_zero_returns_empty_bytes():
    assert bytes_from_int(0) == b""  # bit_length defaults to 0 for 0

# error path: negative value should raise OverflowError with unsigned encoding
def test_bytes_from_int_negative_raises_overflow():
    with pytest.raises(OverflowError):
        bytes_from_int(-1)
