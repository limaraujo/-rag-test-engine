import pytest
from repositorios.code_katas.src.trietree import Trie


# happy path: word inserted, contains returns True
def test_contains_happy_path():
    t = Trie()
    t.insert("cat")
    assert t.contains("cat") is True

# branch: non-string input raises TypeError
def test_contains_raises_TypeError_on_non_string():
    t = Trie()
    with pytest.raises(TypeError) as exc:
        t.contains(123)
    assert str(exc.value) == "Word must be a string"

# case de borda: path exists for prefix but next letter missing -> False
def test_contains_returns_false_when_path_partial():
    t = Trie()
    t.insert("cat")
    assert t.contains("cb") is False

# branch: path exists for entire string but no terminal marker -> KeyError
def test_contains_raises_KeyError_when_no_terminal_marker():
    t = Trie()
    t.insert("cat")
    t.insert("car")
    with pytest.raises(KeyError) as exc:
        t.contains("ca")
    assert "That word has not been inserted" in str(exc.value)
