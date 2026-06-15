import pytest
from repositorios.code_katas.src.trietree import Trie


# happy path: insert a new word and verify contains and size
def test_insert_happy_path():
    trie = Trie()
    trie.insert("Hello")
    assert trie.contains("hello") is True
    assert trie._size == 1

# exception: non-string input raises TypeError
def test_insert_raises_typeerror_on_non_string():
    trie = Trie()
    with pytest.raises(TypeError):
        trie.insert(123)

# branch: inserting two words with shared prefix and then duplicating
def test_insert_branching_updates_size_and_contains():
    trie = Trie()
    trie.insert("cat")
    assert trie.contains("cat") is True
    assert trie._size == 1

    trie.insert("car")
    assert trie.contains("car") is True
    assert trie._size == 2

    trie.insert("cat")  # duplicate should not increment size
    assert trie._size == 2

# boundary: empty string insertion increments once and duplicates are ignored
def test_insert_empty_string_boundary():
    trie = Trie()
    trie.insert("")
    assert trie._size == 1
    trie.insert("")
    assert trie._size == 1
