import pytest
from repositorios.pyjwt.jwt.utils import bytes_from_int

# happy path: bit_length=None for a positive small integer
def test_bytes_from_int_default_bit_length_positive():
    assert bytes_from_int(5) == b"\x05"

# padding: explicit bit_length larger than needed should pad with leading zeros
def test_bytes_from_int_explicit_bit_length_padding():
    assert bytes_from_int(5, bit_length=16) == b"\x00\x05"

# edge: zero value with default bit_length yields empty bytes
def test_bytes_from_int_zero_returns_empty_when_no_bit_length():
    assert bytes_from_int(0) == b""

# exception: too small bit_length for non-zero value raises OverflowError
def test_bytes_from_int_too_small_bit_length_raisesOverflowError():
    with pytest.raises(OverflowError):
        bytes_from_int(1, bit_length=0)
