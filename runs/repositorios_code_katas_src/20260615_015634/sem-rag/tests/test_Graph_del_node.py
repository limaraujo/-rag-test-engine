import pytest
from repositorios.code_katas.src.flight_graph import Graph

# curto: happy path - delete existing node and remove its references from others
def test_del_node_happy_path_removes_node_and_references():
    g = Graph()
    g.graph = {
        'A': {'B': True, 'C': True},
        'B': {'A': True},
        'C': {}
    }
    g.del_node('A')
    assert 'A' not in g.graph
    assert 'A' not in g.graph.get('B', {})
    assert g.graph['B'] == {}
    assert g.graph['C'] == {}

# curto: missing_key - attempting to delete a non-existent node raises KeyError
def test_del_node_missing_key_raises():
    g = Graph()
    g.graph = {'A': {'B': True}}
    with pytest.raises(KeyError) as excinfo:
        g.del_node('X')
    assert "You can't delete a node that does not exist." in str(excinfo.value)

# curto: branch - node exists but is not referenced by any other node
def test_del_node_no_incoming_references():
    g = Graph()
    g.graph = {
        'A': {'B': True},
        'B': {}
    }
    g.del_node('A')
    assert 'A' not in g.graph
    assert g.graph == {'B': {}}
