from repositorios.code_katas.src.flight_graph import Graph

# Verifica caminho feliz: grafico com várias chaves preserva a ordem de inserção
def test_nodes_happy_path_order():
    g = Graph()
    g.graph = {'node1': 1, 'node2': 2, 'node3': 3}
    assert g.nodes() == ['node1', 'node2', 'node3']

# Verifica caso de borda: grafo vazio retorna lista vazia
def test_nodes_empty_returns_empty_list():
    g = Graph()
    g.graph = {}
    assert g.nodes() == []

# Verifica suporte a chaves não-string (ex.: inteiros) mantendo tipo de chave
def test_nodes_handles_non_string_keys():
    g = Graph()
    g.graph = {1: 'one', 2: 'two', 3: 'three'}
    assert g.nodes() == [1, 2, 3]
