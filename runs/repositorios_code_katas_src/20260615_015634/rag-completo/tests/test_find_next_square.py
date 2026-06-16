import pytest
from repositorios.code_katas.src.next_sq import find_next_square


# Teste de caminho feliz: quadrados perfeitos devem retornar o próximo quadrado perfeito
@pytest.mark.parametrize("inp, expected", [
    (16, 25),
    (9, 16),
    (1, 4),
    (0, 1),
])
def test_find_next_square_happy_path(inp, expected):
    assert find_next_square(inp) == expected

# Teste de caso não quadrado perfeito: deve retornar -1
@pytest.mark.parametrize("inp", [
    14, 20, 7, 50
])
def test_find_next_square_non_perfect_returns_minus_one(inp):
    assert find_next_square(inp) == -1
