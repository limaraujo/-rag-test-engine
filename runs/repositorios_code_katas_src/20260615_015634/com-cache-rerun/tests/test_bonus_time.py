from repositorios.code_katas.src.fatcat import bonus_time

# Test 1: happy path with bonus True
def test_bonus_time_with_bonus_true_returns_salary_times_ten():
    assert bonus_time(100, True) == "$1000"

# Test 2: no bonus
def test_bonus_time_without_bonus_returns_salary_prefixed():
    assert bonus_time(100, False) == "$100"

# Test 3: edge case zero salary with bonus
def test_bonus_time_with_zero_salary_and_bonus_true():
    assert bonus_time(0, True) == "$0"

# Test 4: float salary with bonus
def test_bonus_time_with_float_salary_and_bonus_true():
    assert bonus_time(12.5, True) == "$125.0"
