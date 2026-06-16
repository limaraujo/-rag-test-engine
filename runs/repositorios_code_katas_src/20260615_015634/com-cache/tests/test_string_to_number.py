import pytest
from repositorios.code_katas.src.string2num import string_to_number

# Testa conversões válidas para múltiplos casos (happy path)
@pytest.mark.parametrize("input_str, expected", [
    ("123", 123),
    ("-123", -123),
    (" 42 ", 42),
])
def test_string_to_number_valid(input_str, expected):
    assert string_to_number(input_str) == expected

# Testa exceção para entrada não numérica (caso de borda)
def test_string_to_number_invalid_raises():
    with pytest.raises(ValueError):
        string_to_number("abc")
