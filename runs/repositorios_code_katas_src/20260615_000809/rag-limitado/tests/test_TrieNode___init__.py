from collections import OrderedDict
from repositorios.code_katas.src.trietree import TrieNode

# verifica valor padrão None e inicializa as children como OrderedDict (caso happy path)
def test_trienode_init_default_values():
    node = TrieNode()
    assert node.value is None
    assert isinstance(node.children, OrderedDict)
    assert len(node.children) == 0

# verifica que o valor passado é armazenado corretamente (caso happy path com valor)
def test_trienode_init_with_value():
    node = TrieNode(value="A")
    assert node.value == "A"
    assert isinstance(node.children, OrderedDict)

# verifica que cada instancia tem seu próprio dicionário de children (branch/isolamento de instâncias)
def test_trienode_init_independency_of_children():
    node1 = TrieNode()
    node2 = TrieNode()
    assert node1.children is not node2.children
    assert len(node1.children) == 0
    assert len(node2.children) == 0
