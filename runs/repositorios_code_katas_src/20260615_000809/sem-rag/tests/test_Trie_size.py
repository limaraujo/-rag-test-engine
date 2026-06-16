import pytest
from repositorios.code_katas.src.trietree import Trie

# short: happy path - initial Trie size is zero
def test_size_initially_zero():
    t = Trie()
    assert t.size() == 0

# short: internal state reflects through size() for various internal _size values
@pytest.mark.parametrize("internal_size", [0, 1, 3, 10])
def test_size_reflects_internal_state(internal_size):
    t = Trie()
    t._size = internal_size
    assert t.size() == internal_size
