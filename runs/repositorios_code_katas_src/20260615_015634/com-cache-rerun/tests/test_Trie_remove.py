import pytest
from repositorios.code_katas.src.trietree import Trie

def safe_contains(trie: Trie, word: str) -> bool:
    try:
        return trie.contains(word)
    except KeyError:
        return False

def test_remove_non_string_raises_type_error():
    t = Trie()
    with pytest.raises(TypeError):
        t.remove(123)

def test_remove_word_with_branch_removes_specific_branch_and_preserves_other():
    t = Trie()
    t.insert("abc")
    t.insert("abd")
    assert safe_contains(t, "abc")
    assert safe_contains(t, "abd")
    t.remove("abc")
    assert not safe_contains(t, "abc")
    assert safe_contains(t, "abd")

def test_remove_word_prefix_of_other_word_removes_end_marker_only():
    t = Trie()
    t.insert("an")
    t.insert("any")
    assert safe_contains(t, "an")
    assert safe_contains(t, "any")
    t.remove("an")
    assert not safe_contains(t, "an")
    assert safe_contains(t, "any")

def test_remove_word_not_in_trie_raises_keyerror():
    t = Trie()
    t.insert("hello")
    with pytest.raises(KeyError):
        t.remove("hell")
