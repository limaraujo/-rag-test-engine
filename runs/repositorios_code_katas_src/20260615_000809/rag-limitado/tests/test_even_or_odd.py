import pytest
from repositorios.code_katas.src.even_odd import even_or_odd

# Verifica que números pares retornam 'Even' (caminho principal)
@pytest.mark.parametrize("number", [0, 2, -4, 8])
def test_even_or_odd_returns_Even_for_even_numbers(number):
    assert even_or_odd(number) == "Even"

# Verifica que números ímpares retornam 'Odd' (caminho alternativo)
@pytest.mark.parametrize("number", [1, -1, 3, -5])
def test_even_or_odd_returns_Odd_for_odd_numbers(number):
    assert even_or_odd(number) == "Odd"

# Verifica que entradas de tipo incorreto levantam TypeError
def test_even_or_odd_raises_type_error_for_invalid_input():
    with pytest.raises(TypeError):
        even_or_odd("string")
