import pytest
from mockes.exemplo import Calculadora

def test_potencia_happy_path():
    """Calcula potencia com expoente positivo (caminho feliz)."""
    calc = Calculadora("calc")
    assert calc.potencia(3, 4) == 81

def test_potencia_zero_exponent():
    """Qualquer número elevado a zero resulta em 1."""
    calc = Calculadora("calc")
    assert calc.potencia(7, 0) == 1

def test_potencia_zero_base_zero_exponent():
    """0 elevado a 0 segue a semântica do Python e retorna 1."""
    calc = Calculadora(nome="CalcZero")
    assert calc.potencia(0, 0) == 1

def test_potencia_negative_exponent_raises():
    """Expoente negativo deve levantar ValueError com mensagem adequada."""
    calc = Calculadora("calc")
    with pytest.raises(ValueError, match="Expoente negativo não é permitido."):
        calc.potencia(2, -3)

def test_potencia_negative_base_odd_exponent():
    """Base negativa com expoente ímpar resulta em negativo."""
    calc = Calculadora("calc")
    assert calc.potencia(-2, 3) == -8

def test_potencia_negative_base_even_exponent():
    """Base negativa com expoente par resulta em positivo."""
    calc = Calculadora("calc")
    assert calc.potencia(-2, 4) == 16

def test_potencia_invalid_input_none_raises():
    """Entrada None deve levar a TypeError."""
    calc = Calculadora("calc")
    with pytest.raises(TypeError):
        calc.potencia(None, 2)

def test_potencia_invalid_input_type_raises():
    """Tipos não inteiros que não podem ser exponentiados levantam TypeError."""
    calc = Calculadora("calc")
    with pytest.raises(TypeError):
        calc.potencia("2", 3)
    with pytest.raises(TypeError):
        calc.potencia(2, "3")
