from repositorios.code_katas.src.trietree import Trie

def test_traversal_happy_path_returns_all_characters():
    t = Trie()
    t.insert("apple")
    t.insert("app")
    t.insert("ape")
    results = list(t.traversal())
    assert set(results) == {"a", "p", "l", "e"}

def test_traversal_with_start_prefix_ap():
    t = Trie()
    t.insert("apple")
    t.insert("app")
    t.insert("ape")
    t.insert("banana")
    results = list(t.traversal("ap"))
    assert set(results) == {"p", "l", "e"}

def test_traversal_with_missing_start_returns_empty():
    t = Trie()
    t.insert("apple")
    t.insert("app")
    results = list(t.traversal("xyz") or [])
    assert results == []
