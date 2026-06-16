import pytest
from repositorios.code_katas.src.string2num import string_to_number

# Testa caminho feliz: converte string numérica positiva para inteiro
def test_string_to_number_positive():
    assert string_to_number("123") == 123

# Testa caminho com sinal negativo
def test_string_to_number_negative():
    assert string_to_number("-42") == -42

# Testa caminho com sinal de mais
def test_string_to_number_with_plus():
    assert string_to_number("+3") == 3

# Testa exceção para entrada não numérica
def test_string_to_number_invalid_raises_value_error():
    with pytest.raises(ValueError):
        string_to_number("abc")
