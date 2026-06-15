from collections import OrderedDict
from repositorios.code_katas.src.trietree import TrieNode


# Verifica inicialização padrão: valor=None e children vazios (caminho feliz)
def test_trienode_init_default_values():
    node = TrieNode()
    assert node.value is None
    assert isinstance(node.children, OrderedDict)
    assert len(node.children) == 0


# Verifica inicialização com valor explícito: valor é armazenado e children é vazio
def test_trienode_init_with_value():
    node = TrieNode("test")
    assert node.value == "test"
    assert isinstance(node.children, OrderedDict)
    assert len(node.children) == 0


# Verifica independência entre instâncias: alterações em um node não afetam outro
def test_trienode_instances_are_independent():
    n1 = TrieNode("a")
    n2 = TrieNode("b")
    n1.children["x"] = TrieNode("y")
    assert "x" in n1.children
    assert "x" not in n2.children
