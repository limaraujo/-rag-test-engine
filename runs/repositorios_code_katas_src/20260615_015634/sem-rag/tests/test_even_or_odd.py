import pytest
from repositorios.code_katas.src.even_odd import even_or_odd

# Verifica retorno para números pares e ímpares usando parametrização (cobrir ambas ramificações)
@pytest.mark.parametrize("value, expected", [
    (2, "Even"),
    (3, "Odd"),
    (0, "Even"),
    (-1, "Odd"),
    (-4, "Even"),
])
def test_even_or_odd_various_numbers(value, expected):
    assert even_or_odd(value) == expected
