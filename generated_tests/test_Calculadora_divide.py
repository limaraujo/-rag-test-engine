import pytest
from mockes.exemplo import Calculadora

def test_divide_happy_path():
    "Verifica divisão válida retorna resultado float correto."
    calc = Calculadora(nome="MinhaCalc")
    result = calc.divide(10, 2)
    assert isinstance(result, float)
    assert result == 5.0

def test_divide_zero_division():
    "Verifica que dividir por zero lança ValueError com mensagem adequada."
    calc = Calculadora(nome="CalcZero")
    with pytest.raises(ValueError, match="Divisão por zero não é permitida."):
        calc.divide(7, 0)

def test_divide_invalid_input():
    "Verifica comportamento quando entradas inválidas (tipo errado) são fornecidas."
    calc = Calculadora(nome="CalcTipo")
    # passar uma string como divisor deve causar TypeError ao tentar dividir
    with pytest.raises(TypeError):
        calc.divide(10, "dois")