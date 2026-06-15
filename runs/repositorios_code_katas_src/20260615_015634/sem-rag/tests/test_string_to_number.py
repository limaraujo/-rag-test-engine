import pytest
from repositorios.code_katas.src.string2num import string_to_number

# short: happy path: verifica conversão de strings numéricas simples (inclui negativo)
@pytest.mark.parametrize("input_str, expected", [
    ("0", 0),
    ("7", 7),
    ("-42", -42),
    ("123", 123),
])
def test_string_to_number_happy_path(input_str, expected):
    assert string_to_number(input_str) == expected

# short: exceção: entradas não numéricas devem levantar ValueError
@pytest.mark.parametrize("input_str", ["abc", ""])
def test_string_to_number_raises_for_invalid_input(input_str):
    with pytest.raises(ValueError):
        string_to_number(input_str)
