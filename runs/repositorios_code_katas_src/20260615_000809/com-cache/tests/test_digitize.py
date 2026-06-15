import pytest
from repositorios.code_katas.src.convert import digitize

# Teste happy path: número simples, verifica inversão de dígitos
def test_digitize_happy_path_basic():
    assert digitize(3521) == [1, 2, 5, 3]

# Teste borda: zero retorna lista com zero
def test_digitize_zero_returns_single_zero():
    assert digitize(0) == [0]

# Teste com dois dígitos incluindo zero interno (10 -> [0, 1])
def test_digitize_two_digits_including_zero():
    assert digitize(10) == [0, 1]

# Teste de exceção: números negativos não são suportados
def test_digitize_negative_raises_value_error():
    with pytest.raises(ValueError):
        digitize(-123)
