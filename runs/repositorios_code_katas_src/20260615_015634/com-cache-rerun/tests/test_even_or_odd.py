import pytest
from repositorios.code_katas.src.even_odd import even_or_odd

# Testa números inteiros positivos/negativos e zero para cobrir caminhos da condição (Even/Odd)
@pytest.mark.parametrize("number,expected", [
    (0, "Even"),
    (1, "Odd"),
    (2, "Even"),
    (-1, "Odd"),
    (-2, "Even"),
])
def test_even_or_odd_various_inputs(number, expected):
    assert even_or_odd(number) == expected
