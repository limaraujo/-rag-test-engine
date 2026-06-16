import pytest
from repositorios.code_katas.src.trietree import Trie


# verifica caminho principal (happy path) com palavra inserida
def test_contains_happy_path_true():
    t = Trie()
    t.insert("hello")
    assert t.contains("hello") is True


# verifica branch que retorna False quando não existe a palavra
def test_contains_false_when_word_not_present():
    t = Trie()
    t.insert("hello")
    assert t.contains("world") is False


# verifica exceção TypeError para entrada não-string
def test_contains_type_error_for_non_string():
    t = Trie()
    with pytest.raises(TypeError):
        t.contains(123)


# verifica exceção KeyError quando o prefixo existe mas a palavra não foi inserida (fim não marcado)
def test_contains_keyerror_on_prefix_without_end_marker():
    t = Trie()
    t.insert("helloworld")
    with pytest.raises(KeyError):
        t.contains("hell")
