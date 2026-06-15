from repositorios.code_katas.src.minmax import mini

# Verifica o caminho feliz: lista não vazia retorna o menor valor
def test_mini_happy_path_numbers():
    assert mini([3, 1, 2]) == 1

# Verifica que duplicatas não afetam o resultado: retorna o menor entre duplicates
def test_mini_with_duplicates_numbers():
    assert mini([5, 5, 3, 3, 7]) == 3

# Verifica o caminho alternativo (empty): lista vazia retorna a própria lista vazia
def test_mini_empty_list():
    assert mini([]) == []

# Verifica com números negativos: retorna o menor negativo
def test_mini_negative_numbers():
    assert mini([-1, -5, 0, 2]) == -5
