import pytest
from repositorios.pyjwt.jwt.utils import bytes_to_number

# Verifica conversão válida de bytes para número (happy path)
@pytest.mark.parametrize("input_bytes, expected", [
    (b"\x00\x01", 1),
    (b"\xff", 255),
    (b"\x01\x00", 256),
])
def test_bytes_to_number_valid(input_bytes, expected):
    assert bytes_to_number(input_bytes) == expected

# Verifica comportamento com input vazio (edge case)
def test_bytes_to_number_empty_raises():
    with pytest.raises(ValueError):
        bytes_to_number(b"")
