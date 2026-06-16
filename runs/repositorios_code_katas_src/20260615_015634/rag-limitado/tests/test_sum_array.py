from repositorios.code_katas.src.sum_highlow import sum_array

# happy path: lista com múltiplos elementos, soma dos internos (exclui min e max)
def test_sum_array_happy_path():
    assert sum_array([1, 2, 3, 4]) == 5

# borda: entrada None deve retornar 0
def test_sum_array_none_returns_zero():
    assert sum_array(None) == 0

# borda: lista com único elemento deve retornar 0
def test_sum_array_single_element_returns_zero():
    assert sum_array([5]) == 0
