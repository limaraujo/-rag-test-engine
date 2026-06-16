from repositorios.code_katas.src.minmax import mini

# caminho principal: lista não vazia retorna o menor elemento
def test_mini_happy_path_returns_smallest():
    assert mini([3, 1, 2]) == 1

# caso de borda: lista vazia retorna a própria lista
def test_mini_empty_list_returns_same():
    assert mini([]) == []

# caso de borda: None retorna None
def test_mini_none_returns_none():
    assert mini(None) is None

# caso de borda: lista com um único elemento retorna esse elemento
def test_mini_single_element_returns_itself():
    assert mini([7]) == 7
