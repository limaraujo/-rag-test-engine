import pytest
from repositorios.code_katas.src.fatcat import bonus_time

# Parametrizado: cobre cenários de bonus True/False e casos de borda (negativo e zero)
@pytest.mark.parametrize("salary,bonus,expected", [
    (100, True, "$1000"),
    (100, False, "$100"),
    (-50, True, "$-500"),
    (0, True, "$0"),
])
def test_bonus_time_variants(salary, bonus, expected):
    assert bonus_time(salary, bonus) == expected
