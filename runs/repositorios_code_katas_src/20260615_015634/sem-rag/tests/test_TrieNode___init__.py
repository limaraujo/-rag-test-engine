import pytest
from collections import OrderedDict
from repositorios.code_katas.src.trietree import TrieNode

# verifica valor padrão None e children vazia (caminho feliz)
def test_init_defaults_happy_path():
    node = TrieNode()
    assert isinstance(node, TrieNode)
    assert node.value is None
    assert isinstance(node.children, OrderedDict)
    assert len(node.children) == 0

# verifica que o valor passado é armazenado corretamente
def test_init_with_value_sets_value():
    node = TrieNode(value="test")
    assert node.value == "test"
    assert isinstance(node.children, OrderedDict)
    assert len(node.children) == 0

# verifica que o atributo children é um OrderedDict e começa vazio
def test_children_is_ordered_dict_and_empty():
    node = TrieNode()
    assert isinstance(node.children, OrderedDict)
    assert list(node.children.keys()) == []
    assert len(node.children) == 0

# verifica que diferentes TrieNode possuem dicionários de filhos independentes
def test_independent_children_maps_between_instances():
    n1 = TrieNode()
    n2 = TrieNode()
    n1.children["a"] = TrieNode("child")
    assert "a" in n1.children
    assert "a" not in n2.children
    assert len(n2.children) == 0
