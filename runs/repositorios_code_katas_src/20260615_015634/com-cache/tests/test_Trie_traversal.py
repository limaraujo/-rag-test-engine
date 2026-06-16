from repositorios.code_katas.src.trietree import Trie

def _collect_all_words(trie: Trie):
    results = []

    def dfs(node, prefix: str):
        if '$' in node.children:
            results.append(prefix)
        for ch, child in node.children.items():
            if ch == '$':
                continue
            dfs(child, prefix + ch)

    dfs(trie.root, "")
    return results

def _collect_words_with_prefix(trie: Trie, prefix: str):
    current = trie.root
    for ch in prefix:
        if ch in current.children:
            current = current.children[ch]
        else:
            return []
    results = []

    def dfs(node, acc):
        if '$' in node.children:
            results.append(acc)
        for ch, child in node.children.items():
            if ch == '$':
                continue
            dfs(child, acc + ch)

    dfs(current, prefix)
    return results

def test_traversal_happy_path_no_prefix():
    t = Trie()
    words = ["cat", "car", "cart", "dog", "dot"]
    for w in words:
        t.insert(w)
    result = _collect_all_words(t)
    assert set(result) == set(words)

def test_traversal_with_prefix_ca():
    t = Trie()
    words = ["cat", "car", "cart", "dog", "dot"]
    for w in words:
        t.insert(w)
    result = _collect_words_with_prefix(t, "ca")
    assert set(result) == {"cat", "car", "cart"}

def test_traversal_with_nonexistent_prefix():
    t = Trie()
    for w in ["cat", "car", "cart", "dog", "dot"]:
        t.insert(w)
    result = _collect_words_with_prefix(t, "z")
    assert result == []
