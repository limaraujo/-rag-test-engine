import pytest
from repositorios.code_katas.src.fatcat import bonus_time

# verifica caminho feliz com bônus (casos com diferentes salários)
@pytest.mark.parametrize("salary, expected", [
    (1000, "$10000"),
    (0, "$0"),
    (12.5, "$125.0"),
])
def test_bonus_time_with_bonus(salary, expected):
    assert bonus_time(salary, True) == expected

# verifica caminho sem bônus (casos com diferentes salários)
@pytest.mark.parametrize("salary, expected", [
    (1000, "$1000"),
    (0, "$0"),
    (12.5, "$12.5"),
])
def test_bonus_time_without_bonus(salary, expected):
    assert bonus_time(salary, False) == expected
