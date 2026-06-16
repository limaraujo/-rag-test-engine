from repositorios.code_katas.src.sum_positive import positive_sum

# teste: caminho feliz com mistura de positivos, negativos e zero
def test_positive_sum_happy_path_mixed_numbers():
    arr = [1, -2, 3, 0, 4]
    assert positive_sum(arr) == 8

# teste: borda/rota -> entrada vazia
def test_positive_sum_empty_list():
    assert positive_sum([]) == 0

# teste: caminho com nenhum positivo (apenas negativos e zero)
def test_positive_sum_all_negatives_and_zero():
    assert positive_sum([-1, 0, -5]) == 0

# teste: inclui números de ponto flutuante positivos
def test_positive_sum_with_floats_positive_values():
    assert positive_sum([1.5, 2.5, -1.0]) == 4.0
