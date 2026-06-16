from repositorios.code_katas.src.parenthetics import Node

# verifica valores padrão quando não passamos argumentos
def test_node_default_values():
    n = Node()
    assert n.value is None
    assert n.next_node is None
    assert n.previous_node is None

# verifica atribuição de valores e referências de nós (caso feliz)
def test_node_assigns_values():
    next_node = Node(value=20)
    prev_node = Node(value=5)
    n = Node(value=10, next_node=next_node, previous_node=prev_node)
    assert n.value == 10
    assert n.next_node is next_node
    assert n.previous_node is prev_node

# verifica que tipos diferentes de nós são aceitos para links (caso de borda)
def test_node_accepts_non_node_types_for_links():
    n = Node(value="root", next_node="next", previous_node=123)
    assert n.value == "root"
    assert n.next_node == "next"
    assert n.previous_node == 123
