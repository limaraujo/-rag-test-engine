from repositorios.code_katas.src.minmax import maxi

# happy path: maior valor em uma lista de inteiros
def test_maxi_happy_path():
    assert maxi([1, 3, 2, 5, 4]) == 5

# caso com números negativos
def test_maxi_negative_numbers():
    assert maxi([-10, -1, -20]) == -1

# caso com duplicatas do maior valor
def test_maxi_with_duplicates():
    assert maxi([1, 5, 5, 3]) == 5

# branch else: lista vazia deve retornar a própria lista
def test_maxi_empty_list_returns_same():
    assert maxi([]) == []
