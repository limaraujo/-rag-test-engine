import pytest
from repositorios.code_katas.src.even_odd import even_or_odd

# Verifica branches: retorna 'Even' para números pares (inclui 0) e 'Odd' para ímpares, cobrindo casos positivos e negativos
@pytest.mark.parametrize("number, expected", [
    (0, "Even"),    # caso par no edge (zero)
    (1, "Odd"),     # caso ímpar
    (-1, "Odd"),    # caso ímpar negativo
    (-2, "Even"),   # caso par negativo
])
def test_even_or_odd_branches(number, expected):
    assert even_or_odd(number) == expected
