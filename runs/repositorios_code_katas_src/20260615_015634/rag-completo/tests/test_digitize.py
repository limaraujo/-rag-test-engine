import pytest
from repositorios.code_katas.src.convert import digitize

# Teste de caminho feliz com diferentes inteiros positivos, incluindo 0
@pytest.mark.parametrize("n,expected", [
    (0, [0]),
    (123, [3, 2, 1]),
    (35231, [1, 3, 2, 5, 3]),
])
def test_digitize_happy_path_variants(n, expected):
    assert digitize(n) == expected

# Teste que entradas negativas levantam ValueError (caso de borda/erro explícito)
def test_digitize_negative_raises_value_error():
    with pytest.raises(ValueError):
        digitize(-123)
