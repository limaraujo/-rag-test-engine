import pytest
from mockes.exemplo import Calculadora


def test_multiplica_happy_path():
    """Multiplica dois inteiros positivos corretamente."""
    calc = Calculadora(nome="CalcHappy")
    assert calc.multiplica(6, 7) == 42


def test_multiplica_large_numbers():
    """Multiplicação de grandes inteiros resulta no valor esperado sem perda."""
    calc = Calculadora(nome="Big")
    a = 10**12
    b = 10**6
    assert calc.multiplica(a, b) == 10**18


def test_multiplica_float_inputs():
    """Se recebendo floats, a operação realiza a multiplicação normal (resultado float)."""
    calc = Calculadora(nome="FloatTest")
    result = calc.multiplica(2.5, 4.0)
    assert result == 10.0
    assert isinstance(result, float)


def test_multiplica_invalid_input_string_string():
    """Multiplicar duas strings deve levantar TypeError (operação inválida)."""
    calc = Calculadora(nome="Invalid")
    with pytest.raises(TypeError):
        calc.multiplica("a", "b")


def test_multiplica_invalid_input_none():
    """Chamar multiplica com entrada inválida (None) gera TypeError."""
    calc = Calculadora("Null")
    with pytest.raises(TypeError):
        calc.multiplica(None, 5)


def test_multiplica_negative_numbers():
    """Multiplica números negativos e positivos corretamente."""
    calc = Calculadora(nome="NegPos")
    assert calc.multiplica(-3, 5) == -15


def test_multiplica_zero():
    """Multiplica envolvendo zero resulta em zero."""
    calc = Calculadora(nome="Zero")
    assert calc.multiplica(0, 123) == 0
    assert calc.multiplica(999, 0) == 0


def test_multiplica_mixed_numeric_types():
    """Multiplica inteiros com floats resulta em float correspondente."""
    calc = Calculadora(nome="Mixed")
    res = calc.multiplica(3, 2.5)
    assert res == 7.5
    assert isinstance(res, float)
