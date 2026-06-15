from repositorios.code_katas.src.trietree import Trie

class DummyTrie(Trie):
    def __init__(self):
        pass

class Node:
    def __init__(self, children=None):
        self.children = {} if children is None else children

# short: happy path with a single node (no children)
def test_traversal_single_node_includes_root():
    # happy path: a node with no children yields only itself
    root = Node()
    t = DummyTrie()
    assert list(t._traversal(root)) == [root]

# short: ensure '$' key is skipped and other children are traversed
def test_traversal_skips_dollar_and_includes_child():
    child = Node()
    root = Node(children={'$': Node(), 'a': child})
    t = DummyTrie()
    assert list(t._traversal(root)) == [root, child]

# short: deeper traversal order (root -> a -> b)
def test_traversal_nested_structure_orders():
    leaf = Node()
    mid = Node(children={'b': leaf})
    root = Node(children={'a': mid})
    t = DummyTrie()
    assert list(t._traversal(root)) == [root, mid, leaf]

# short: when first=True, root is not yielded
def test_traversal_first_arg_true_excludes_root():
    leaf = Node()
    mid = Node(children={'b': leaf})
    root = Node(children={'a': mid})
    t = DummyTrie()
    assert list(t._traversal(root, first=True)) == [mid, leaf]
