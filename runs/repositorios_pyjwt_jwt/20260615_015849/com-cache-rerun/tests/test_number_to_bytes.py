import binascii
import pytest
from repositorios.pyjwt.jwt.utils import number_to_bytes

# curto: happy path - número pequeno cabe em 1 byte
def test_number_to_bytes_happy_path_one_byte():
    assert number_to_bytes(1, 1) == b"\x01"

# curto: padding - número pequeno ocupa 2 bytes com zeros à esquerda
def test_number_to_bytes_padding_two_bytes():
    assert number_to_bytes(2, 2) == b"\x00\x02"

# curto: múltiplos de bytes - número exatamente ocupa 2 bytes
def test_number_to_bytes_multi_byte_exact():
    assert number_to_bytes(0x1234, 2) == b"\x12\x34"

# curto: exceção para overflow hipotético - número exige mais bytes que o informado
def test_number_to_bytes_raises_on_overflow():
    with pytest.raises(binascii.Error):
        number_to_bytes(0x100, 1)
