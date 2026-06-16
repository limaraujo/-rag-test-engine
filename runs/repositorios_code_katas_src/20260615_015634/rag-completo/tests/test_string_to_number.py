import pytest
from repositorios.code_katas.src.string2num import string_to_number

# Teste feliz: converte string numérica simples para inteiro
def test_string_to_number_happy_path():
    assert string_to_number("123") == 123

# Teste com sinal negativo: verifica que "-5" é convertido corretamente
def test_string_to_number_negative():
    assert string_to_number("-5") == -5

# Teste com espaços em branco ao redor: " 42 " deve ser convertido para 42
def test_string_to_number_whitespace():
    assert string_to_number(" 42 ") == 42

# Teste de exceção para entradas não numéricas
def test_string_to_number_invalid_raises():
    with pytest.raises(ValueError):
        string_to_number("abc")
