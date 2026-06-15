import pytest
from repositorios.code_katas.src.parenthetics import Node

# Caminho feliz: inicializa com valores simples
def test_init_happy_path():
    node = Node(value=10, next_node=None, previous_node=None)
    assert node.value == 10
    assert node.next_node is None
    assert node.previous_node is None

# Defaults: sem argumentos, todos None
def test_init_defaults():
    node = Node()
    assert node.value is None
    assert node.next_node is None
    assert node.previous_node is None

# Parametrizado: várias combinações de value, next_node e previous_node
@pytest.mark.parametrize("value, next_node, previous_node", [
    (10, None, None),
    (None, Node(1), None),
    ("v", Node(1), Node(2)),
])
def test_init_parametrized_values(value, next_node, previous_node):
    node = Node(value, next_node, previous_node)
    assert node.value == value
    assert node.next_node is next_node
    assert node.previous_node is previous_node

# Identity preservation: referências de next_node e previous_node são armazenadas
def test_init_stores_referenced_nodes():
    next_node = Node("next")
    prev_node = Node("prev")
    node = Node("cur", next_node=next_node, previous_node=prev_node)
    assert node.next_node is next_node
    assert node.previous_node is prev_node
