import pytest
from repositorios.pyjwt.jwt.utils import bytes_to_number

# happy path: várias entradas válidas convertem corretamente
@pytest.mark.parametrize("input_bytes, expected", [
    (b'\x00', 0),
    (b'\xff', 255),
    (b'\x01\x02', 0x0102),
    (b'\x01\x02\x03', 0x010203),
])
def test_bytes_to_number_happy_path(input_bytes, expected):
    result = bytes_to_number(input_bytes)
    assert isinstance(result, int)
    assert result == expected

# edge: entrada vazia levanta ValueError
def test_bytes_to_number_empty_raises():
    with pytest.raises(ValueError):
        bytes_to_number(b'')

# corpo principal: verifica conversão de entrada maior (big-endian)
def test_bytes_to_number_large_input():
    data = bytes(range(1, 9))  # 8 bytes: 01 02 03 04 05 06 07 08
    expected = int.from_bytes(data, 'big')
    assert bytes_to_number(data) == expected
