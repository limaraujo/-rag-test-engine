import pytest
from repositorios.code_katas.src.trietree import Trie

# happy path: word inserted is found by contains
def test_contains_happy_path():
    t = Trie()
    t.insert("cat")
    assert t.contains("cat") is True

# edge: path exists but end marker not present -> KeyError
def test_contains_end_marker_missing_raises_keyerror():
    t = Trie()
    t.insert("cat")
    with pytest.raises(KeyError) as exc:
        t.contains("ca")
    assert "That word has not been inserted" in str(exc.value)

# type safety: non-string input should raise TypeError
def test_contains_non_string_raises_typeerror():
    t = Trie()
    with pytest.raises(TypeError):
        t.contains(123)

# branch: first letter missing in root -> return False
def test_contains_missing_first_letter_returns_false():
    t = Trie()
    t.insert("cat")
    assert t.contains("dog") is False
