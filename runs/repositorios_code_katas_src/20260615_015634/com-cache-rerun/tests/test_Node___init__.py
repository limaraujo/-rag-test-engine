from repositorios.code_katas.src.parenthetics import Node

# short: happy path - default constructor initializes fields to None
def test_node_init_defaults():
    n = Node()
    assert n.value is None
    assert n.next_node is None
    assert n.previous_node is None

# short: explicit all-values initialization
def test_node_init_with_all_values():
    n = Node(value=10, next_node='next', previous_node='prev')
    assert n.value == 10
    assert n.next_node == 'next'
    assert n.previous_node == 'prev'

# short: partial initialization where only value is provided
def test_node_init_with_partial_values():
    n = Node(value='a')
    assert n.value == 'a'
    assert n.next_node is None
    assert n.previous_node is None
