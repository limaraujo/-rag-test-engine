import pytest
from repositorios.pyjwt.jwt.utils import bytes_to_number

# curto: happy path - vários inputs exemplares para bytes_to_number via parametrização
@pytest.mark.parametrize("input_bytes, expected", [
    (b"\x01", 1),
    (b"\x01\x02", 0x0102),
    (b"\x00\x01", 1),
])
def test_bytes_to_number_happy_path_parametrized(input_bytes, expected):
    assert bytes_to_number(input_bytes) == expected

# curto: erro - entrada vazia levanta ValueError
def test_bytes_to_number_empty_raises():
    with pytest.raises(ValueError):
        bytes_to_number(b"")
