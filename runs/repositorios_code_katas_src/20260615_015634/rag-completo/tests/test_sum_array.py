from repositorios.code_katas.src.sum_highlow import sum_array

# teste feliz: lista com vários números (remove min e max)
def test_sum_array_happy_path():
    assert sum_array([1, 2, 3, 4, 5]) == 9

# caso de borda: lista com um único elemento retorna 0
def test_sum_array_single_element_returns_zero():
    assert sum_array([7]) == 0
