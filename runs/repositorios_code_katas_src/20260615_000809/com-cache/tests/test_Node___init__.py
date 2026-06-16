from repositorios.code_katas.src.parenthetics import Node

# Verifica o caminho feliz: valores default None
def test_node_init_default_values():
    n = Node()
    assert n.value is None
    assert n.next_node is None
    assert n.previous_node is None

# Verifica que __init__ atribui parâmetros fornecidos (caso feliz)
def test_node_init_sets_provided_values():
    n = Node(value=10, next_node=None, previous_node=None)
    assert n.value == 10
    assert n.next_node is None
    assert n.previous_node is None

# Verifica que __init__ aceita encadeamento de nós
def test_node_init_with_links():
    prev = Node(value=1)
    nxt = Node(value=3)
    mid = Node(value=2, next_node=nxt, previous_node=prev)
    assert mid.value == 2
    assert mid.next_node is nxt
    assert mid.previous_node is prev

# Verifica que valores explícitos, incluindo None, são preservados
def test_node_init_explicit_none_values():
    n = Node(value=None, next_node=None, previous_node=None)
    assert n.value is None
    assert n.next_node is None
    assert n.previous_node is None
