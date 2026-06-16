import pytest
import binascii
from repositorios.pyjwt.jwt.utils import number_to_bytes

# Test happy path: verify correct fixed-length encoding for common cases
@pytest.mark.parametrize("num,num_bytes,expected", [
    (1, 1, b'\x01'),
    (2, 3, b'\x00\x00\x02'),
    (0xFFFF, 2, b'\xff\xff'),
])
def test_number_to_bytes_happy_path(num, num_bytes, expected):
    assert number_to_bytes(num, num_bytes) == expected

# Test exception path: input that doesn't fit into the requested number of bytes raises an error
def test_number_to_bytes_overflow_raises():
    with pytest.raises(binascii.Error):
        number_to_bytes(0x10000, 2)
