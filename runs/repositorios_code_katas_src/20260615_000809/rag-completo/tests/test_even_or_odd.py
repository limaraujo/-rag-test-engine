import pytest
from repositorios.code_katas.src.even_odd import even_or_odd

# Verifica o caminho principal: retorna 'Even' para números pares e 'Odd' para ímpares (casos pares e ímpares)
@pytest.mark.parametrize("value, expected", [
    (2, "Even"),
    (0, "Even"),
    (-3, "Odd"),
    (7, "Odd"),
])
def test_even_or_odd_parity(value, expected):
    assert even_or_odd(value) == expected
