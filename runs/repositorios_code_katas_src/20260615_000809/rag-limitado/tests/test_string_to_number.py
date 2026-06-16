import pytest
from repositorios.code_katas.src.string2num import string_to_number

# curto: happy path - converte "123" para 123
def test_string_to_number_happy_path_positive():
    assert string_to_number("123") == 123

# curto: borda - converte string com sinal negativo "-45" para -45
def test_string_to_number_negative():
    assert string_to_number("-45") == -45

# curto: borda/entrada comum - remove zeros à esquerda "0007" vira 7
def test_string_to_number_leading_zeros():
    assert string_to_number("0007") == 7

# curto: exceção - entrada não numérica deve levantar ValueError
def test_string_to_number_invalid_raises_value_error():
    with pytest.raises(ValueError):
        string_to_number("abc")
