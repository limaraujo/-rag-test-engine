from repositorios.code_katas.src.sum_of_nth_terms import series_sum

# Test zero terms: n=0 should return "0.00"
def test_series_sum_zero_terms_returns_zero_point_zero():
    assert series_sum(0) == "0.00"

# Test single term: n=1 should be 1.00
def test_series_sum_one_term_returns_one_point_zero():
    assert series_sum(1) == "1.00"

# Test two terms: n=2 should be 1 + 1/4 = 1.25
def test_series_sum_two_terms_returns_one_point_two_five():
    assert series_sum(2) == "1.25"

# Test three terms: n=3 should be 1 + 1/4 + 1/7 ≈ 1.392857 -> "1.39"
def test_series_sum_three_terms_rounds_correctly():
    assert series_sum(3) == "1.39"
