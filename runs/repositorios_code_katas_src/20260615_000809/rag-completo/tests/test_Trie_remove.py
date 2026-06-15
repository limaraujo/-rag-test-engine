import pytest
from repositorios.code_katas.src.trietree import Trie

# verifica remoção de ramo folha em presença de bifurcação anterior (happy path)
def test_remove_leaf_with_bifurcation():
    t = Trie()
    t.insert("cat")
    t.insert("car")
    assert t.contains("cat")
    assert t.contains("car")
    t.remove("cat")
    assert not t.contains("cat")
    assert t.contains("car")

# caminho feliz: remove apenas palavra existente sem bifurcação (apenas "hello")
def test_remove_only_word():
    t = Trie()
    t.insert("hello")
    assert t.contains("hello")
    t.remove("hello")
    assert not t.contains("hello")

# exceção KeyError ao remover palavra inexistente ('car' não inserida)
def test_remove_nonexistent_word_raises():
    t = Trie()
    t.insert("cat")
    with pytest.raises(KeyError):
        t.remove("car")

# TypeError ao passar não-string
def test_remove_invalid_type_raises_typeerror():
    t = Trie()
    with pytest.raises(TypeError):
        t.remove(123)
