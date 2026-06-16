import pytest
from repositorios.code_katas.src.flight_graph import Graph

# curto: happy path - edge exists and both nodes exist; node2 has outgoing edges
def test_del_edge_happy_path():
    g = Graph()
    g.graph = {'A': {'B': 1}, 'B': {'C': 2}, 'C': {}}
    g.del_edge('A', 'B')
    assert 'B' not in g.graph['A']

# curto: missing_key - either node1 or node2 not present in the graph
@pytest.mark.parametrize("node1,node2", [
    ("X", "A"),
    ("A", "Y"),
    ("X", "Y"),
])
def test_del_edge_missing_key_raises_KeyError(node1, node2):
    g = Graph()
    g.graph = {'A': {'B': 1}, 'B': {'C': 2}, 'C': {}}
    with pytest.raises(KeyError):
        g.del_edge(node1, node2)

# curto: edge exists but node2 has no outgoing edges -> ValueError
def test_del_edge_edge_exists_but_node2_no_outgoing_raises_ValueError():
    g = Graph()
    g.graph = {'A': {'B': 1}, 'B': {}, 'C': {}}
    with pytest.raises(ValueError):
        g.del_edge('A', 'B')

# curto: edge not present between existing nodes -> ValueError
def test_del_edge_edge_not_present_between_existing_nodes_raises_ValueError():
    g = Graph()
    g.graph = {'A': {'E': 5}, 'B': {'C': 2}, 'C': {}}
    with pytest.raises(ValueError):
        g.del_edge('A', 'B')
