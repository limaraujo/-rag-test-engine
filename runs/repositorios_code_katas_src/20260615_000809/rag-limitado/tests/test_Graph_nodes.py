from repositorios.code_katas.src.flight_graph import Graph

# Verifica o caminho feliz: gráfico não vazio retorna todas as chaves na ordem de inserção
def test_nodes_non_empty_insertion_order():
    g = Graph()
    g.graph = {'A': 1, 'B': 2, 'C': 3}
    assert g.nodes() == ['A', 'B', 'C']

# Verifica o caso de borda: gráfico vazio retorna lista vazia
def test_nodes_empty_graph_returns_empty_list():
    g = Graph()
    g.graph = {}
    assert g.nodes() == []
