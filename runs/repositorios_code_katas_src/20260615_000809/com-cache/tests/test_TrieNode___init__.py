from collections import OrderedDict
import pytest
from repositorios.code_katas.src.trietree import TrieNode



# happy path: default constructor initializes value=None and empty children
def test_init_default_values_happy_path():
    node = TrieNode()
    assert node.value is None
    assert isinstance(node.children, OrderedDict)
    assert len(node.children) == 0


# happy path: provided value is stored and children remains empty
@pytest.mark.parametrize("value", [0, "val", {"a": 1}])
def test_init_with_value_sets_value_and_empty_children(value):
    # case: explicit value should be preserved, with no children yet
    node = TrieNode(value)
    assert node.value == value
    assert isinstance(node.children, OrderedDict)
    assert len(node.children) == 0


# edge/robustness: multiple instances should have independent state
def test_multiple_instances_have_independent_children():
    node1 = TrieNode()
    node2 = TrieNode(123)
    assert node1.value is None
    assert node2.value == 123
    assert isinstance(node1.children, OrderedDict)
    assert isinstance(node2.children, OrderedDict)
    assert node1.children is not node2.children
    assert len(node1.children) == 0
    assert len(node2.children) == 0
