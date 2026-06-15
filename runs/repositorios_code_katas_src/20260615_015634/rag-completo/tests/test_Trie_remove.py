import pytest
from repositorios.code_katas.src.trietree import Trie

# happy path: remove a single word that exists in the trie
def test_remove_basic_word_happy_path():
    t = Trie()
    t.insert("hello")
    assert t.contains("hello") is True
    t.remove("hello")
    try:
        result = t.contains("hello")
    except KeyError:
        result = False
    assert result is False

# branch: word is prefix of a longer word; removing removes end marker
def test_remove_word_prefix_of_longer_word():
    t = Trie()
    t.insert("car")
    t.insert("carp")
    assert t.contains("car") is True
    t.remove("car")
    try:
        result = t.contains("car")
    except KeyError:
        result = False
    assert result is False
    assert t.contains("carp") is True

# last bifurcation: ensure removal stops at the bifurcation point and preserves other branches
def test_remove_word_with_last_bifurcation_preserves_other():
    t = Trie()
    t.insert("cat")
    t.insert("car")
    assert t.contains("cat") is True
    assert t.contains("car") is True
    t.remove("cat")
    try:
        result_cat = t.contains("cat")
    except KeyError:
        result_cat = False
    assert result_cat is False
    assert t.contains("car") is True

# invalid inputs: TypeError for non-string and KeyError for missing key
@pytest.mark.parametrize("word,exc", [(123, TypeError), ("notexist", KeyError)])
def test_remove_invalid_inputs(word, exc):
    t = Trie()
    t.insert("exists")
    if exc is TypeError:
        with pytest.raises(TypeError):
            t.remove(word)
    else:
        with pytest.raises(KeyError):
            t.remove(word)
