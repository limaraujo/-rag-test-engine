import pytest
from repositorios.code_katas.src.fatcat import bonus_time

# Testa retorno com bônus ativo (multiplica salary) e sem bônus (salary simples)
@pytest.mark.parametrize("salary,bonus,expected", [
    (100, True, "$1000"),
    (100, False, "$100"),
    (0, True, "$0"),
    (2.5, True, "$25.0"),
])
def test_bonus_time_basic_cases(salary, bonus, expected):
    assert bonus_time(salary, bonus) == expected
