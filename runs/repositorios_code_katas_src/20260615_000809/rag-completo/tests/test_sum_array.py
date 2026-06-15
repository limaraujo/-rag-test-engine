import pytest
from repositorios.code_katas.src.sum_highlow import sum_array

# Verifica múltiplos cenários com sum_array: caminho feliz, bordas vazias/únicas e casos com negativos/duplicatas
@pytest.mark.parametrize("arr,expected", [
    ([1, 2, 3, 4], 5),   # caminho feliz
    ([], 0),              # borda: lista vazia
    ([10], 0),            # borda: único elemento
    ([-1, -2, 5, 3, 3], 5),  # casos com negativos e duplicatas
    ([5, 5, 5], 5),       # todos iguais
])
def test_sum_array_various(arr, expected):
    assert sum_array(arr) == expected
