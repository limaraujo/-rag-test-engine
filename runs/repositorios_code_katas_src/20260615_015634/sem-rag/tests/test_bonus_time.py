from repositorios.code_katas.src.fatcat import bonus_time

# happy path: when bonus is True, salary is multiplied by 10 and formatted with $
def test_bonus_time_bonus_true_happy_path():
    assert bonus_time(100, True) == "$1000"

# branch: when bonus is False, original salary is returned formatted with $
def test_bonus_time_no_bonus_returns_salary():
    assert bonus_time(50, False) == "$50"

# edge: zero salary with bonus True should yield "$0"
def test_bonus_time_zero_salary_with_bonus_true():
    assert bonus_time(0, True) == "$0"

# edge: negative salary with bonus False exercises the else-branch
def test_bonus_time_negative_salary_no_bonus():
    assert bonus_time(-20, False) == "$-20"
