import pytest
from repositorios.code_katas.src.string2num import string_to_number

# Verifica parsing de valores inteiros válidos (happy path)
@pytest.mark.parametrize("input_str, expected", [
    ("123", 123),
    ("0", 0),
    ("-45", -45),
    (" 67 ", 67),
])
def test_string_to_number_valid(input_str, expected):
    assert string_to_number(input_str) == expected

# Verifica entradas inválidas levantam ValueError
@pytest.mark.parametrize("input_str", ["", "abc", "12.3"])
def test_string_to_number_invalid_raises(input_str):
    with pytest.raises(ValueError):
        string_to_number(input_str)
