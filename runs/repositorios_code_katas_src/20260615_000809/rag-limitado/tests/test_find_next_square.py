import pytest
from repositorios.code_katas.src.next_sq import find_next_square

# Verifica caminho feliz: entradas que são quadrados perfeitos retornam o próximo quadrado
@pytest.mark.parametrize("sq, expected", [
    (0, 1),
    (1, 4),
    (4, 9),
    (9, 16),
    (16, 25),
])
def test_find_next_square_perfect(sq, expected):
    assert find_next_square(sq) == expected

# Verifica retorno -1 para entradas que não são quadrados perfeitos (cobrir branch else)
@pytest.mark.parametrize("sq", [2, 3, 5, 10])
def test_find_next_square_not_perfect(sq):
    assert find_next_square(sq) == -1
