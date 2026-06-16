from repositorios.code_katas.src.parenthetics import Node

# borde: default None values when no arguments are provided
def test_init_defaults_none():
    n = Node()
    assert n.value is None
    assert n.next_node is None
    assert n.previous_node is None

# happy path: all args provided; verify value and linkage are set correctly
def test_init_with_all_args():
    next_n = Node(2)
    prev_n = Node(0)
    n = Node(value=5, next_node=next_n, previous_node=prev_n)
    assert n.value == 5
    assert n.next_node is next_n
    assert n.previous_node is prev_n

# caso mínimo: apenas value fornecido; links devem ser None
def test_init_value_only():
    n = Node(7)
    assert n.value == 7
    assert n.next_node is None
    assert n.previous_node is None

# teste de ligação entre nós: next_node e previous_node são Node com valores esperados
def test_init_linked_nodes_values():
    next_n = Node(3)
    prev_n = Node(1)
    n = Node(value=2, next_node=next_n, previous_node=prev_n)
    assert isinstance(n.next_node, Node)
    assert isinstance(n.previous_node, Node)
    assert n.next_node.value == 3
    assert n.previous_node.value == 1
