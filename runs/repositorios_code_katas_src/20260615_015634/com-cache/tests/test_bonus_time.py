from repositorios.code_katas.src.fatcat import bonus_time

# Verifica caminho feliz: bônus ativo (bonus=True), salário 100 → "$1000"
def test_bonus_time_with_bonus_true_salary_100():
    assert bonus_time(100, True) == "$1000"

# Verifica cenário sem bônus: bônus=False, salário 100 → "$100"
def test_bonus_time_without_bonus_salary_100():
    assert bonus_time(100, False) == "$100"

# Verifica caso de borda: salário zero com bônus ativo
def test_bonus_time_with_bonus_true_zero_salary():
    assert bonus_time(0, True) == "$0"

# Verifica caso de borda: salário zero sem bônus
def test_bonus_time_without_bonus_zero_salary():
    assert bonus_time(0, False) == "$0"
