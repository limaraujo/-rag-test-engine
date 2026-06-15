from repositorios.code_katas.src.sum_positive import positive_sum

# verifica soma de positivos (happy path)
def test_positive_sum_happy_path():
    assert positive_sum([1, -2, 3, 0, 4]) == 8

# verifica comportamento com lista vazia (branch else)
def test_positive_sum_empty_list():
    assert positive_sum([]) == 0

# verifica comportamento com todos negativos/zero (sem positivos)
def test_positive_sum_no_positives():
    assert positive_sum([-1, 0, -5]) == 0

# verifica comportamento com None (branch else)
def test_positive_sum_none_input():
    assert positive_sum(None) == 0
