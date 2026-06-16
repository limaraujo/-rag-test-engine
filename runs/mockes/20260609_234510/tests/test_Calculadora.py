import pytest
from mockes.exemplo import Calculadora


def test_divide_happy_path():
    """Divide two integers yielding a float result (happy path)."""
    calc = Calculadora("calc")
    assert calc.divide(10, 2) == 5.0


def test_divide_by_zero_raises_value_error():
    calc = Calculadora("calc")
    with pytest.raises(ValueError):
        calc.divide(10, 0)


def test_divide_invalid_input_none_raises_type_error():
    calc = Calculadora("calc")
    with pytest.raises(TypeError):
        calc.divide(None, 2)


def test_divide_non_integer_result():
    calc = Calculadora("calc")
    assert calc.divide(7, 2) == 3.5


def test_multiplica_happy_path():
    calc = Calculadora("calc")
    assert calc.multiplica(3, 4) == 12


def test_multiplica_invalid_input_none_raises_type_error():
    calc = Calculadora("calc")
    with pytest.raises(TypeError):
        calc.multiplica(None, 5)


def test_multiplica_invalid_input_string_string():
    calc = Calculadora("calc")
    with pytest.raises(TypeError):
        calc.multiplica("a", "b")


def test_potencia_happy_path():
    calc = Calculadora("calc")
    assert calc.potencia(2, 5) == 32


def test_potencia_zero_exponent():
    calc = Calculadora("calc")
    assert calc.potencia(7, 0) == 1


def test_potencia_negative_exponent_raises_value_error():
    calc = Calculadora("calc")
    with pytest.raises(ValueError):
        calc.potencia(2, -1)


def test_potencia_invalid_input_none_raises_type_error():
    calc = Calculadora("calc")
    with pytest.raises(TypeError):
        calc.potencia(None, 2)
