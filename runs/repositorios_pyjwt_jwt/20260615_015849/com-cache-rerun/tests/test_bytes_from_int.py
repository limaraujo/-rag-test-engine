import pytest
from repositorios.pyjwt.jwt.utils import bytes_from_int

# Verifica o caminho feliz: valor pequeno sem bit_length
def test_bytes_from_int_happy_path_no_bit_length():
    assert bytes_from_int(1) == b"\x01"

# Verifica o redimensionamento com bit_length explicitamente maior que o necessário
def test_bytes_from_int_with_specified_bit_length_larger():
    assert bytes_from_int(1, bit_length=16) == b"\x00\x01"

# Verifica o caso de zero: bit_length=None resulta em zero-length bytes
def test_bytes_from_int_zero_returns_empty():
    assert bytes_from_int(0) == b""

# Verifica exceção quando bit_length é insuficiente para o valor
def test_bytes_from_int_insufficient_bit_length_raises():
    with pytest.raises(OverflowError):
        bytes_from_int(256, bit_length=8)
