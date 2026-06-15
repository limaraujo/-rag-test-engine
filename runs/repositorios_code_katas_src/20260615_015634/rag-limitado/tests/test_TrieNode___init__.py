from collections import OrderedDict
from repositorios.code_katas.src.trietree import TrieNode



# happy path: inicialização padrão sem valor (value=None) e children vazia
def test_default_init_sets_none_and_empty_children():
    node = TrieNode()
    assert node.value is None
    assert isinstance(node.children, OrderedDict)
    assert len(node.children) == 0


# happy path: inicialização com valor fornecido e children vazia
def test_init_with_value_sets_value_and_empty_children():
    node = TrieNode("x")
    assert node.value == "x"
    assert isinstance(node.children, OrderedDict)
    assert len(node.children) == 0


# branch/interação: dois nós independentes com containers de children separados
def test_multiple_nodes_have_independent_children():
    n1 = TrieNode("a")
    n2 = TrieNode("b")
    assert n1.value == "a"
    assert n2.value == "b"
    assert len(n1.children) == 0
    assert len(n2.children) == 0
    n1.children["c"] = TrieNode("c")
    assert "c" in n1.children
    assert "c" not in n2.children
