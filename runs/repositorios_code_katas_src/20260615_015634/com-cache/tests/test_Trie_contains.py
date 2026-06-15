import pytest
from repositorios.code_katas.src.trietree import Trie

# test: happy path - contains should return True after insertion
def test_contains_happy_path_true():
    t = Trie()
    t.insert("abc")
    assert t.contains("abc") is True

# test: missing path returns False without exception
def test_contains_false_when_path_missing():
    t = Trie()
    t.insert("abc")
    assert t.contains("abd") is False

# test: non-string input raises TypeError
def test_contains_raises_type_error_on_non_string():
    t = Trie()
    with pytest.raises(TypeError):
        t.contains(123)

# test: path exists but word not inserted ends with KeyError
def test_contains_raises_keyerror_when_word_not_inserted_but_path_exists():
    t = Trie()
    t.insert("hello")
    with pytest.raises(KeyError) as exc:
        t.contains("hell")
    assert "That word has not been inserted" in str(exc.value)
