from repositorios.code_katas.src.minmax import mini

# Verifica caminho principal com lista não vazia
def test_mini_happy_path():
    assert mini([3, 1, 2]) == 1
    assert mini([10, -1, 5, -1, 0]) == -1

# Verifica caminho alternativo com lista vazia
def test_mini_empty_list():
    assert mini([]) == []
