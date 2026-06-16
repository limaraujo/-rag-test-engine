import pytest
from repositorios.code_katas.src.next_sq import find_next_square

# Testa caminho feliz: entradas são quadrados perfeitos, retornam o próximo quadrado
@pytest.mark.parametrize("sq, expected", [
    (0, 1),
    (1, 4),
    (4, 9),
    (9, 16),
    (16, 25),
])
def test_find_next_square_perfect(sq, expected):
    assert find_next_square(sq) == expected

# Testa caso não perfeito: entradas não são quadrados perfeitos, retornam -1
@pytest.mark.parametrize("sq", [2, 3, 5, 10, 20, 26, 99])
def test_find_next_square_not_perfect(sq):
    assert find_next_square(sq) == -1
