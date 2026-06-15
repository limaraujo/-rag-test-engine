from repositorios.code_katas.src.flight_graph import Graph

# Teste happy path: __init__ cria uma instância com atributo graph igual a dict vazio
def test_init_creates_empty_graph_and_type():
    g = Graph()
    assert isinstance(g, Graph)
    assert isinstance(g.graph, dict)
    assert g.graph == {}

# Teste independência entre instâncias: cada Graph possui seu próprio dicionário
def test_init_graphs_are_independent():
    g1 = Graph()
    g2 = Graph()
    g1.graph['a'] = 1
    assert 'a' in g1.graph
    assert 'a' not in g2.graph
    assert g1.graph is not g2.graph

# Teste verificação adicional de tipo da propriedade após inicialização
def test_init_graph_attribute_is_dict_instantly():
    g = Graph()
    assert type(g.graph) is dict
