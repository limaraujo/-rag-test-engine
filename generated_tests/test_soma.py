from mockes.exemplo import soma
import pytest

def test_soma_happy_path():
    "Retorna a soma de dois inteiros positivos corretamente."
    assert soma(3, 5) == 8

def test_soma_negative_numbers():
    "Retorna a soma correta quando ambos os operandos são negativos."
    assert soma(-4, -6) == -10

def test_soma_mixed_signs():
    "Retorna a soma correta quando os operandos têm sinais diferentes."
    assert soma(-7, 3) == -4

def test_soma_with_zero():
    "Somar zero com um inteiro retorna o outro inteiro inalterado."
    assert soma(0, 9) == 9
    assert soma(9, 0) == 9

def test_soma_large_integers():
    "Lida corretamente com inteiros muito grandes sem perda de precisão."
    a = 10**18
    b = 10**18
    assert soma(a, b) == 2 * 10**18

def test_soma_booleans():
    "Booleans são tratados como inteiros (True == 1, False == 0) na soma."
    assert soma(True, True) == 2
    assert soma(True, False) == 1

def test_soma_floats():
    "Aceita floats e retorna o resultado em ponto flutuante."
    assert soma(2.5, 1.5) == 4.0

def test_soma_string_concat():
    "Quando os dois argumentos forem strings, realiza concatenação."
    assert soma("foo", "bar") == "foobar"

def test_soma_type_mismatch_raises():
    "Misturar tipos incompatíveis (ex.: int + str) resulta em TypeError."
    with pytest.raises(TypeError):
        soma(1, "2")