from repositorios.code_katas.src.minmax import mini

# Verifica o caminho feliz: lista desordenada retorna o menor elemento
def test_mini_happy_path():
    assert mini([3, 1, 2]) == 1

# Caso de borda: lista vazia deve retornar a própria lista vazia
def test_mini_empty_list_returns_empty():
    assert mini([]) == []

# Caso de borda: input None deve retornar None
def test_mini_none_input_returns_none():
    assert mini(None) is None
