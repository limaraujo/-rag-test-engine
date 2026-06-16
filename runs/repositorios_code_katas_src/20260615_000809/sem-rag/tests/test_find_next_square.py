import pytest
from repositorios.code_katas.src.next_sq import find_next_square

# Verifica retorno para quadrados perfeitos (happy path)
@pytest.mark.parametrize("sq,expected", [
    (0, 1),
    (1, 4),
    (4, 9),
    (9, 16),
    (144, 169),
])
def test_find_next_square_happy_path(sq, expected):
    assert find_next_square(sq) == expected

# Verifica retorno -1 para entradas que não são quadrados perfeitos (caso negativo)
@pytest.mark.parametrize("sq,expected", [
    (2, -1),
    (3, -1),
    (5, -1),
    (10, -1),
    (15, -1),
])
def test_find_next_square_non_square(sq, expected):
    assert find_next_square(sq) == expected
