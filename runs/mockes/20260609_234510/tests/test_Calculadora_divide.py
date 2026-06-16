import pytest
from mockes.exemplo import Calculadora

def test_divide_happy_path():
    "Divide dois inteiros com resultado float igual a 5.0."
    calc = Calculadora("calc")
    assert calc.divide(10, 2) == 5.0

def test_divide_non_integer_result():
    "Divide dois inteiros produzindo resultado não inteiro (float)."
    calc = Calculadora("calc")
    assert calc.divide(7, 2) == 3.5

def test_divide_zero_division_raises():
    "Divisão por zero deve levantar ValueError com mensagem adequada."
    calc = Calculadora("calc")
    with pytest.raises(ValueError, match="Divisão por zero não é permitida."):
        calc.divide(5, 0)

def test_divide_invalid_input_none():
    "Chamar divide com entrada inválida (None) gera TypeError."
    calc = Calculadora("calc")
    with pytest.raises(TypeError):
        calc.divide(None, 2)

def test_divide_invalid_input_type_strings():
    "Chamar divide com entrada inválida (strings) gera TypeError."
    calc = Calculadora("calc")
    with pytest.raises(TypeError):
        calc.divide(5, "two")

def test_divide_large_values():
    "Divide valores grandes produzindo o resultado esperado em float."
    calc = Calculadora("calc")
    assert calc.divide(1000000, 4) == 250000.0

def test_divide_negative_values():
    "Divide dois números, incluindo negativo, resultando em float negativo."
    calc = Calculadora("calc")
    assert calc.divide(-9, 3) == -3.0
