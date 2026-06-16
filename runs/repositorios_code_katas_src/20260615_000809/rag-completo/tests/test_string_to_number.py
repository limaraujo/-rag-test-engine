import pytest
from repositorios.code_katas.src.string2num import string_to_number

# Verifica conversão correta de string para inteiro (happy path)
@pytest.mark.parametrize("input_str, expected", [
    ("0", 0),
    ("123", 123),
    ("-7", -7),
    (" 42 ", 42),
])
def test_string_to_number_happy_path(input_str, expected):
    assert string_to_number(input_str) == expected

# Verifica que entradas inválidas levantam ValueError
def test_string_to_number_raises_value_error():
    with pytest.raises(ValueError):
        string_to_number("abc")
    with pytest.raises(ValueError):
        string_to_number("")
    with pytest.raises(ValueError):
        string_to_number("1.0")
