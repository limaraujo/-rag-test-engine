from repositorios.code_katas.src.next_sq import find_next_square

# Test happy path: input is a perfect square (16) -> 25
def test_find_next_square_happy_path_perfect_square():
    assert find_next_square(16) == 25

# Test branch: non-perfect-square input should return -1
def test_find_next_square_non_square_returns_minus_one():
    assert find_next_square(14) == -1
