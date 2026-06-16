from repositorios.code_katas.src.sum_highlow import sum_array

# curto: happy path com números variados; verifica exclusão de min e max
def test_sum_array_happy_path():
    arr = [6, 2, 1, 8, 10]
    assert sum_array(arr) == 16

# curto: branch else para entrada vazia
def test_sum_array_empty():
    assert sum_array([]) == 0

# curto: branch else para lista com único elemento
def test_sum_array_single_element():
    assert sum_array([5]) == 0

# curto: duplicates de min/max; verifica soma do meio corretamente
def test_sum_array_with_duplicates():
    arr = [1, 1, 2, 3, 3]
    assert sum_array(arr) == 6
