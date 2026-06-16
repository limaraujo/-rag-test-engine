from repositorios.code_katas.src.minmax import maxi

# teste de caminho feliz com inteiros
def test_maxi_numbers():
    lst = [3, 1, 4, 2, -5]
    assert maxi(lst) == 4

# teste de borda: lista vazia retorna a própria lista
def test_maxi_empty_list():
    assert maxi([]) == []

# teste com strings para confirmar comportamento de ordenação
def test_maxi_strings():
    lst = ["apple", "banana", "cherry", "date"]
    assert maxi(lst) == "date"
