import pytest
from repositorios.pyjwt.jwt.utils import bytes_to_number

# curto: happy path e cenários com múltiplos bytes (converte bytes para inteiro, incluindo leading zeros)
@pytest.mark.parametrize("input_bytes, expected", [
    (b"\x01", 1),
    (b"\x01\x02", 258),
    (b"\x00\x01", 1),
])
def test_bytes_to_number_happy_path(input_bytes, expected):
    assert bytes_to_number(input_bytes) == expected

# curto: exceção em input vazio
def test_bytes_to_number_empty_raises():
    with pytest.raises(ValueError):
        bytes_to_number(b"")
