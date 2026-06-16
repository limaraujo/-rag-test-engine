import pytest
from repositorios.pyjwt.jwt.utils import bytes_from_int

# teste 1: caminho padrão (bit_length=None) com valor que requer 2 bytes (happy path)
def test_bytes_from_int_default_bits_happy_path():
    val = 256
    assert bytes_from_int(val) == b'\x01\x00'

# teste 2: fornecer bit_length explicitamente maior que o necessário (cobrir caminho de branch)
def test_bytes_from_int_explicit_bit_length():
    val = 1
    bit_length = 16
    assert bytes_from_int(val, bit_length=bit_length) == b'\x00\x01'

# teste 3: fornecer bit_length insuficiente que deve causar OverflowError
def test_bytes_from_int_explicit_bit_length_too_small():
    with pytest.raises(OverflowError):
        bytes_from_int(256, bit_length=8)

# teste 4: valor negativo levanta OverflowError (cobrir comportamento com signed=False)
def test_bytes_from_int_negative_raises():
    with pytest.raises(OverflowError):
        bytes_from_int(-1)
