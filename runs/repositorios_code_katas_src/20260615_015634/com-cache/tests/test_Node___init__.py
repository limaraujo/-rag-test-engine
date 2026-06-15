import pytest
from repositorios.code_katas.src.parenthetics import Node


# happy path: default constructor initializes fields to None
def test_node_init_defaults():
    n = Node()
    assert n.value is None
    assert n.next_node is None
    assert n.previous_node is None

# test: init with explicit values assigns attributes correctly (various types)
@pytest.mark.parametrize(
    "value, next_node, previous_node",
    [
        ("val", None, None),
        (123, "nxt", "prv"),
        (None, None, "last"),
        (3.14, {"a": 1}, [1, 2, 3]),
    ],
)
def test_node_init_with_values(value, next_node, previous_node):
    n = Node(value, next_node, previous_node)
    assert n.value == value
    assert n.next_node is next_node
    assert n.previous_node is previous_node
