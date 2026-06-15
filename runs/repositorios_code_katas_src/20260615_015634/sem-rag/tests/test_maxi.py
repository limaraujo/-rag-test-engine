from repositorios.code_katas.src.minmax import maxi

# happy path: não vazia retorna o maior item
def test_maxi_non_empty_numeric_list():
    assert maxi([1, 3, 2, 5, 4]) == 5

# branch: caso de borda - lista vazia retorna a própria lista
def test_maxi_empty_list_returns_empty():
    assert maxi([]) == []
