import pytest
import binascii
from repositorios.pyjwt.jwt.utils import number_to_bytes

# curto: happy path - número pequeno cabe em 1 byte
def test_number_to_bytes_happy_path_one_byte():
    assert number_to_bytes(1, 1) == b"\x01"

# curto: padding - número pequeno ocupa 2 bytes com zero à esquerda
def test_number_to_bytes_padding_to_two_bytes():
    assert number_to_bytes(1, 2) == b"\x00\x01"

# curto: representação multi-byte - 0x1234 em 2 bytes
def test_number_to_bytes_two_bytes_representation():
    assert number_to_bytes(0x1234, 2) == b"\x12\x34"

# curto: overflow/overflow de largura - número não cabe na largura solicitada
def test_number_to_bytes_overflow_raises():
    with pytest.raises((ValueError, binascii.Error)):
        number_to_bytes(0x123, 1)
