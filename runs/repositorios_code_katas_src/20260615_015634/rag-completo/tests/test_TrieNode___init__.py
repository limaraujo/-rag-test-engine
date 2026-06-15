from collections import OrderedDict
import pytest
from repositorios.code_katas.src.trietree import TrieNode

# happy path: inicializa com valor e verifica valor/children
def test_init_sets_value_and_empty_children_happy_path():
    node = TrieNode('x')
    assert node.value == 'x'
    assert isinstance(node.children, OrderedDict)
    assert len(node.children) == 0

# default: sem valor -> value é None
def test_init_default_none():
    node = TrieNode()
    assert node.value is None
    assert isinstance(node.children, OrderedDict)

# independência de instâncias: cada TrieNode tem seu próprio dict de filhos
def test_independent_children_dicts():
    n1 = TrieNode('a')
    n2 = TrieNode('b')
    assert n1.children is not n2.children
    assert isinstance(n1.children, OrderedDict)
    assert isinstance(n2.children, OrderedDict)

# valores distintos entre instâncias são armazenados corretamente
def test_values_are_stored_per_instance():
    n1 = TrieNode('first')
    n2 = TrieNode('second')
    assert n1.value == 'first'
    assert n1.value != n2.value
    assert n2.value == 'second'
