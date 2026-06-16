from repositorios.code_katas.src.minmax import maxi

# verifica o caminho feliz com inteiros (caso positivo)
def test_maxi_happy_path_integers():
    assert maxi([1, 3, 2]) == 3

# verifica o caso com números negativos (branch de valores menores)
def test_maxi_negative_numbers():
    assert maxi([-1, -5, -3]) == -1

# verifica o funcionamento com strings ordenáveis (tipos compatíveis)
def test_maxi_strings():
    assert maxi(['a', 'z', 't']) == 'z'

# verifica o caso de lista vazia (branch falsa)
def test_maxi_empty_list():
    assert maxi([]) == []
