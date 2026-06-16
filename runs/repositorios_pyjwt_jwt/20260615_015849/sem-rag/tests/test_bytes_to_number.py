import pytest
from repositorios.pyjwt.jwt.utils import bytes_to_number

# happy path: multiple inputs converted to expected integers
@pytest.mark.parametrize("input_bytes, expected", [
    (b'\x01\x02', 258),
    (b'\xff', 255),
    (b'\x00\x01', 1),
])
def test_bytes_to_number_happy_path(input_bytes, expected):
    assert bytes_to_number(input_bytes) == expected

# edge case: empty input raises ValueError
def test_bytes_to_number_empty_raises_value_error():
    with pytest.raises(ValueError):
        bytes_to_number(b'')
