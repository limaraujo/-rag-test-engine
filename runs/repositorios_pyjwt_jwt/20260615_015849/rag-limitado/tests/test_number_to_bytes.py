import pytest
from repositorios.pyjwt.jwt.utils import number_to_bytes

# happy path: small number fits into 1 byte
def test_number_to_bytes_one_byte_happy_path():
    assert number_to_bytes(1, 1) == b'\x01'

# happy path: two bytes, exact fit for 0xABCD
def test_number_to_bytes_two_bytes_happy_path():
    assert number_to_bytes(0xABCD, 2) == b'\xab\xcd'

# edge: zero value across multiple bytes
def test_number_to_bytes_zero_padding():
    assert number_to_bytes(0, 3) == b'\x00\x00\x00'

# error path: number too large for the given width raises ValueError
def test_number_to_bytes_raises_on_odd_length():
    with pytest.raises(ValueError):
        number_to_bytes(0x100, 1)
