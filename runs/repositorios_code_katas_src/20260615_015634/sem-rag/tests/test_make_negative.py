import pytest
from repositorios.code_katas.src.return_negative import make_negative

# Teste de caminho feliz com inteiro positivo
def test_make_negative_positive_int():
    assert make_negative(5) == -5

# Teste de caminho feliz com número já negativo permanece negativo
def test_make_negative_negative_int():
    assert make_negative(-3) == -3

# Teste de borda: zero permanece zero
def test_make_negative_zero():
    assert make_negative(0) == 0

# Teste de exceção: entrada não numérica deve falhar com TypeError
def test_make_negative_invalid_type_raises():
    with pytest.raises(TypeError):
        make_negative("string")
