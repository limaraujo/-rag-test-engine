import pytest
from repositorios.pyjwt.jwt.utils import bytes_from_int

# Verifica o caminho feliz: valor pequeno sem bit_length retorna 1 byte
def test_bytes_from_int_happy_path_no_bit_length():
    assert bytes_from_int(1) == b"\x01"

# Verifica o redimensionamento com bit_length explícito (bit_length maior que necessário)
def test_bytes_from_int_explicit_bit_length_padding():
    assert bytes_from_int(1, bit_length=16) == b"\x00\x01"

# Verifica o caso de zero sem bit_length (resultado esperado: bytes vazios)
def test_bytes_from_int_zero_value_no_bit_length():
    assert bytes_from_int(0) == b""

# Verifica exceção para inteiros negativos
def test_bytes_from_int_negative_raises_overflow():
    with pytest.raises(OverflowError):
        bytes_from_int(-1)
