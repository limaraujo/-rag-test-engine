import pytest
from repositorios.code_katas.src.trietree import Trie

# verifica que size retorna o valor atual de _size após ajuste direto (caminho feliz)
@pytest.mark.parametrize("internal_size", [0, 1, 5, 10, 999])
def test_size_reflete_internal_counter(internal_size):
    t = Trie()
    t._size = internal_size
    assert t.size() == internal_size
