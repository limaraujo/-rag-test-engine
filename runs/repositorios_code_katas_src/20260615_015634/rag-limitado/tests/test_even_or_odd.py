import pytest
from repositorios.code_katas.src.even_odd import even_or_odd

# Verifica o retorno correto para números pares e ímpares, incluindo o zero e valores negativos (cobrir as duas branches)
@pytest.mark.parametrize("number, expected", [
    (0, "Even"),
    (1, "Odd"),
    (-1, "Odd"),
    (-2, "Even"),
])
def test_even_or_odd_various_numbers(number, expected):
    assert even_or_odd(number) == expected
