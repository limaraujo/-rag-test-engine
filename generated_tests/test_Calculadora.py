from mockes.exemplo import Calculadora
import pytest


def test_multiplica_happy_path():
    "Multiplica dois inteiros positivos corretamente."
    calc = Calculadora("calc")
    assert calc.multiplica(6, 7) == 42


def test_multiplica_zero_and_negative():
    "Multiplica um número negativo por zero resultando em zero."
    calc = Calculadora("calc")
    assert calc.multiplica(-3, 0) == 0


def test_multiplica_invalid_input():
    "Chamar multiplica com entrada inválida (None) gera TypeError."
    calc = Calculadora("calc")
    with pytest.raises(TypeError):
        calc.multiplica(None, 5)


def test_divide_happy_path():
    "Divide dois inteiros com resultado inteiro em float."
    calc = Calculadora("calc")
    assert calc.divide(10, 2) == 5.0


def test_divide_non_integer_result():
    "Divide dois inteiros produzindo resultado não inteiro (float)."
    calc = Calculadora("calc")
    assert calc.divide(7, 2) == 3.5


def test_divide_by_zero_raises():
    "Divisão por zero deve levantar ValueError com mensagem adequada."
    calc = Calculadora("calc")
    with pytest.raises(ValueError, match="Divisão por zero não é permitida."):
        calc.divide(5, 0)


def test_divide_invalid_input():
    "Chamar divide com entrada inválida (None) gera TypeError."
    calc = Calculadora("calc")
    with pytest.raises(TypeError):
        calc.divide(None, 2)


def test_potencia_happy_path():
    "Calcula potencia com expoente positivo corretamente."
    calc = Calculadora("calc")
    assert calc.potencia(2, 5) == 32


def test_potencia_zero_exponent():
    "Qualquer número elevado a zero resulta em 1."
    calc = Calculadora("calc")
    assert calc.potencia(5, 0) == 1


def test_potencia_negative_exponent_raises():
    "Expoente negativo deve levantar ValueError com mensagem adequada."
    calc = Calculadora("calc")
    with pytest.raises(ValueError, match="Expoente negativo não é permitido."):
        calc.potencia(2, -3)


def test_potencia_invalid_input():
    "Chamar potencia com entrada inválida (None) gera TypeError."
    calc = Calculadora("calc")
    with pytest.raises(TypeError):
        calc.potencia(None, 2)