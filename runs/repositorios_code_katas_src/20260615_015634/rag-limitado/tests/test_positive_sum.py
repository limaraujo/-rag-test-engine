from repositorios.code_katas.src.sum_positive import positive_sum

# Teste curto: caminho feliz com lista não vazia contendo positivos/negativos/zeros
def test_positive_sum_happy_path_mixed_values():
    arr = [1, -2, 3, 0, 4]
    assert positive_sum(arr) == 8

# Teste curto: branch para lista vazia retorna 0
def test_positive_sum_empty_list():
    assert positive_sum([]) == 0
