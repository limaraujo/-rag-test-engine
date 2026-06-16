import pytest
from repositorios.code_katas.src.trietree import Trie

# test: happy path - contains should return True after insertion
def test_contains_happy_path_true():
    t = Trie()
    t.insert("abc")
    assert t.contains("abc") is True

# test: non-string input raises TypeError
def test_contains_non_string_raises_typeerror():
    t = Trie()
    with pytest.raises(TypeError):
        t.contains(123)

# test: unknown path at first character returns False
def test_contains_unknown_first_character_returns_false():
    t = Trie()
    t.insert("abc")
    assert t.contains("z") is False

# test: path exists but no terminal marker raises KeyError
def test_contains_prefix_without_terminal_raises_keyerror():
    t = Trie()
    t.insert("abc")
    with pytest.raises(KeyError):
        t.contains("ab")
