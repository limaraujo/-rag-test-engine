import pytest
from mockes.exemplo import Calculadora

def test_multiplica_happy_path_positive():
    "Multiplica dois inteiros positivos produz o produto correto."
    calc = Calculadora(nome="Principal")
    result = calc.multiplica(6, 7)
    assert result == 42
    assert isinstance(result, int)

def test_multiplica_negative_operand():
    "Multiplica um inteiro negativo por um positivo produz resultado negativo correto."
    calc = Calculadora(nome="Negativo")
    result = calc.multiplica(-4, 5)
    assert result == -20
    assert isinstance(result, int)

def test_multiplica_with_zero():
    "Multiplicar por zero resulta em zero."
    calc = Calculadora(nome="ZeroTest")
    assert calc.multiplica(0, 12345) == 0
    assert calc.multiplica(12345, 0) == 0

def test_multiplica_large_numbers():
    "Multiplicação de grandes inteiros resulta no valor esperado sem perda."
    calc = Calculadora(nome="Big")
    a = 10**12
    b = 10**6
    assert calc.multiplica(a, b) == 10**18

def test_multiplica_float_inputs():
    "Se recebendo floats, a operação realiza a multiplicação normal (resultado float)."
    calc = Calculadora(nome="FloatTest")
    result = calc.multiplica(2.5, 4.0)
    assert result == 10.0
    assert isinstance(result, float)

def test_multiplica_invalid_input_string_string():
    "Multiplicar duas strings deve levantar TypeError (operação inválida)."
    calc = Calculadora(nome="Invalid")
    with pytest.raises(TypeError):
        calc.multiplica("a", "b")