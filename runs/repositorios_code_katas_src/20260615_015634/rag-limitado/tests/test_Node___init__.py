from repositorios.code_katas.src.parenthetics import Node

# curto: happy path; cria Node sem argumentos e verifica valores padrão None
def test_node_defaults():
    node = Node()
    assert node.value is None
    assert node.next_node is None
    assert node.previous_node is None

# curto: happy path; inicializa com valores explícitos e valida atributos
def test_node_explicit_values():
    node = Node(value=5, next_node="next", previous_node="prev")
    assert node.value == 5
    assert node.next_node == "next"
    assert node.previous_node == "prev"

# curto: verify mutabilidade; atributos podem ser reatribuídos após criação
def test_node_mutability_after_init():
    node1 = Node()
    node2 = Node(value="v")
    node1.next_node = node2
    node2.previous_node = node1
    assert node1.next_node is node2
    assert node2.previous_node is node1

# curto: verifica encadeamento simples entre duas nós usando atributos
def test_node_chain_linkage():
    head = Node(value=1)
    tail = Node(value=2)
    head.next_node = tail
    tail.previous_node = head
    assert head.next_node is tail
    assert tail.previous_node is head
    assert head.value == 1
    assert tail.value == 2
