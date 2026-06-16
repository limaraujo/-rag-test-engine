from repositorios.code_katas.src.flight_graph import Graph

# Teste: happy path, __init__ deve criar um dicionário vazio para graph
def test_init_creates_empty_graph_dict():
    g = Graph()
    assert isinstance(g.graph, dict)
    assert g.graph == {}

# Teste: instâncias independentes não compartilham o mesmo dict de graph
def test_init_instances_are_independent():
    g1 = Graph()
    g2 = Graph()
    g1.add_node("A")
    assert g2.graph == {}
    assert g1.graph != g2.graph
