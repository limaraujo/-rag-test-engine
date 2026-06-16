from repositorios.code_katas.src.sum_positive import positive_sum

# Teste: caminho feliz com lista contendo positivos, negativos e zeros
def test_positive_sum_happy_path():
    assert positive_sum([1, -2, 3, 0, 4]) == 8

# Teste: ramo False (lista vazia) retorna 0
def test_positive_sum_empty_list_branch():
    assert positive_sum([]) == 0

# Teste: lista não contém positivos (todos <= 0) retorna 0
def test_positive_sum_no_positives():
    assert positive_sum([-1, 0, -5]) == 0

# Teste: entrada None trata como falsy e retorna 0
def test_positive_sum_none_input():
    assert positive_sum(None) == 0
