import pytest
from repositorios.code_katas.src.monkey import monkey_count

# happy path: verifica retorno de 1 a 5
def test_monkey_count_happy_path():
    assert monkey_count(5) == [1, 2, 3, 4, 5]

# caso único: n=1 retorna [1]
def test_monkey_count_single():
    assert monkey_count(1) == [1]

# borda: valores não positivos (0 e negativo) retornam lista vazia
@pytest.mark.parametrize("n", [0, -3])
def test_monkey_count_non_positive(n):
    assert monkey_count(n) == []
