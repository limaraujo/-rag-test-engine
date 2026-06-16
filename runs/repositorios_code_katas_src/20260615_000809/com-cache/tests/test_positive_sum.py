import pytest
from repositorios.code_katas.src.sum_positive import positive_sum

# Verifica diferentes entradas: caminho feliz e borda (lista vazia, None)
@pytest.mark.parametrize("arr, expected", [
    ([1, 2, -3, 0, 4], 7),
    ([-1, -2, 0], 0),
    ([], 0),
    (None, 0),
])
def test_positive_sum_various_inputs(arr, expected):
    assert positive_sum(arr) == expected
