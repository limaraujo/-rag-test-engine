import pytest
from repositorios.code_katas.src.next_sq import find_next_square

@pytest.mark.parametrize("sq, expected", [
    (0, 1),
    (1, 4),
    (4, 9),
    (9, 16),
    (16, 25),
])
# caminho feliz: quadrados perfeitos retornam o próximo quadrado
def test_find_next_square_happy_path(sq, expected):
    assert find_next_square(sq) == expected

@pytest.mark.parametrize("sq, expected", [
    (2, -1),
    (3, -1),
    (5, -1),
    (10, -1),
])
# caminho não perfeito: entradas não são quadrados perfeitos retornam -1
def test_find_next_square_non_perfect(sq, expected):
    assert find_next_square(sq) == expected
