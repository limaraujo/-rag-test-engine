import pytest
from repositorios.code_katas.src.even_odd import even_or_odd

# verifica branch: retorna "Even" para número par e "Odd" para número ímpar
@pytest.mark.parametrize("input_value, expected", [(2, "Even"), (3, "Odd")])
def test_even_or_odd_even_and_odd(input_value, expected):
    assert even_or_odd(input_value) == expected
