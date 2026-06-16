from repositorios.code_katas.src.parenthetics import Node

# Testa inicialização com valores padrão (caso de borda: defaults)
def test_init_defaults():
    n = Node()
    assert n.value is None
    assert n.next_node is None
    assert n.previous_node is None

# Testa inicialização com todos os parâmetros fornecidos
def test_init_all_parameters_set():
    next_node = Node(2)
    previous_node = Node(3)
    n = Node(value=1, next_node=next_node, previous_node=previous_node)
    assert n.value == 1
    assert n.next_node is next_node
    assert n.previous_node is previous_node

# Testa inicialização apenas com o valor informado
def test_init_only_value_sets():
    n = Node(value=10)
    assert n.value == 10
    assert n.next_node is None
    assert n.previous_node is None

# Testa que os vizinhos são Node e preservam os valores
def test_init_neighbors_are_nodes():
    left = Node('L')
    right = Node('R')
    center = Node(value='C', next_node=right, previous_node=left)
    assert isinstance(center.next_node, Node)
    assert isinstance(center.previous_node, Node)
    assert center.next_node.value == 'R'
    assert center.previous_node.value == 'L'
