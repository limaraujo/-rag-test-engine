import pytest
from repositorios.code_katas.src.fatcat import bonus_time

# parametrize: verifica múltiplos cenários (happy path, sem bônus, zero e negativo) em bonus_time
@pytest.mark.parametrize("salary,bonus,expected", [
    (100, True, "$1000"),   # happy path: bonus applied
    (100, False, "$100"),   # branch: no bonus
    (0, True, "$0"),         # edge: zero salary with bonus
    (-50, True, "$-500"),    # edge: negative salary with bonus
])
def test_bonus_time_parametrized(salary, bonus, expected):
    assert bonus_time(salary, bonus) == expected
