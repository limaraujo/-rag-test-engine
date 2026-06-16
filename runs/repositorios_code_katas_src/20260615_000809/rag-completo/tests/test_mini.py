from repositorios.code_katas.src.minmax import mini

# caminho feliz: menor valor em lista não vazia
def test_mini_happy_path():
    assert mini([3, 1, 2, 5]) == 1

# caso com negativos e duplicatas
def test_mini_with_negatives_and_duplicates():
    assert mini([-3, -1, -3, 0, 2]) == -3

# lista com um elemento
def test_mini_single_element():
    assert mini([42]) == 42

# lista vazia: retorna a própria lista
def test_mini_empty_list_returns_empty():
    assert mini([]) == []
