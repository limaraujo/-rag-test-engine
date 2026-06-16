import pytest
from repositorios.pyjwt.jwt.utils import number_to_bytes

# Teste: caminho feliz cobrindo vários casos de tamanhos de bytes e padding mínimo
@pytest.mark.parametrize("num, num_bytes, expected", [
    (0, 1, b'\x00'),            # zero com tamanho 1
    (1, 1, b'\x01'),             # simples
    (255, 1, b'\xff'),           # limite de 1 byte
    (1, 2, b'\x00\x01'),          # padding para 2 bytes
    (65535, 2, b'\xff\xff'),      # máximo para 2 bytes
])
def test_number_to_bytes_happy_path(num, num_bytes, expected):
    assert number_to_bytes(num, num_bytes) == expected

# Teste: padding com width de 3 bytes (edge de padding)
@pytest.mark.parametrize("num, num_bytes, expected", [
    (0x1234, 3, b'\x00\x12\x34'),
])
def test_number_to_bytes_padding_width_three(num, num_bytes, expected):
    assert number_to_bytes(num, num_bytes) == expected
