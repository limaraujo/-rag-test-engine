import pytest
from repositorios.code_katas.src.flight_graph import Graph


class _Dummy:
    pass

# happy path: edge exists between A and B
def test_adjacent_happy_path_edge_exists():
    obj = _Dummy()
    obj.graph = {'A': {'B': {}}, 'B': {'A': {}}}
    assert Graph.adjacent(obj, 'A', 'B') is True

# error path: node1 not in graph raises KeyError
def test_adjacent_raises_keyerror_node1_missing():
    obj = _Dummy()
    obj.graph = {'A': {'B': {}}, 'B': {'A': {}}}
    with pytest.raises(KeyError) as excinfo:
        Graph.adjacent(obj, 'X', 'A')
    assert "X is not in the graph." in str(excinfo.value)

# error path: node2 not in graph raises KeyError
def test_adjacent_raises_keyerror_node2_missing():
    obj = _Dummy()
    obj.graph = {'A': {'B': {}}, 'B': {'A': {}}}
    with pytest.raises(KeyError) as excinfo:
        Graph.adjacent(obj, 'A', 'Y')
    assert "Y is not in the graph." in str(excinfo.value)

# border: nodes exist but are not connected returns False
def test_adjacent_not_connected_returns_false():
    obj = _Dummy()
    obj.graph = {'A': {'B': {}}, 'B': {'A': {}}, 'C': {}}
    assert Graph.adjacent(obj, 'A', 'C') is False
