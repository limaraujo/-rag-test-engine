import pytest
from repositorios.code_katas.src.monkey import monkey_count

# Verifica caminho principal (happy path): retorna sequência de 1 a n
def test_monkey_count_happy_path():
    assert monkey_count(5) == [1, 2, 3, 4, 5]

# Verifica borda: entradas não positivas retornam lista vazia
@pytest.mark.parametrize("n, expected", [
    (0, []),
    (-3, []),
])
def test_monkey_count_non_positive(n, expected):
    assert monkey_count(n) == expected

# Verifica exceções para tipos não inteiros (erro de tipo ao usar floats/strings)
@pytest.mark.parametrize("invalid_input", [3.5, "4"])
def test_monkey_count_invalid_input_raises_type_error(invalid_input):
    with pytest.raises(TypeError):
        monkey_count(invalid_input)

# Verifica integridade para n grande: tamanho, início e fim da sequência
def test_monkey_count_large_n_integrity():
    n = 100
    result = monkey_count(n)
    assert isinstance(result, list)
    assert len(result) == n
    assert result[0] == 1
    assert result[1] == 2
    assert result[-1] == n
