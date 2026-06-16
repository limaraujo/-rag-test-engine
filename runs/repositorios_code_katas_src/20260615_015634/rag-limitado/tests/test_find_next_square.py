import pytest
from repositorios.code_katas.src.next_sq import find_next_square

# caminho feliz: entradas que são quadrados perfeitos retornam o próximo quadrado
@pytest.mark.parametrize("sq,expected", [
    (0, 1),
    (4, 9),
    (9, 16),
])
def test_find_next_square_perfect_inputs(sq, expected):
    assert find_next_square(sq) == expected

# caso de borda: entradas que não são quadrados perfeitos retornam -1
@pytest.mark.parametrize("sq,expected", [
    (2, -1),
    (3, -1),
])
def test_find_next_square_non_perfect_inputs(sq, expected):
    assert find_next_square(sq) == expected

# exceção: entrada negativa levanta ValueError
def test_find_next_square_negative_raises():
    with pytest.raises(ValueError):
        find_next_square(-1)
