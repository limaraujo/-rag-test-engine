import pytest
from repositorios.code_katas.src.parenthetics import DoubleLink


# verifica caminho principal: inicialização vazia (happy path)
def test_doublelink_init_empty_happy_path():
    dl = DoubleLink()
    assert dl._length == 0
    assert dl.head is None
    assert dl.tail is None

# verifica caminho principal: inicialização com iterável não vazio
def test_doublelink_init_with_non_empty_iterable():
    dl = DoubleLink(iterable=[1, 2, 3])
    assert dl._length == 3
    assert dl.head is not None
    assert dl.tail is not None

# verifica caminho alternativo: iterável vazio não altera o estado
def test_doublelink_init_with_empty_iterable():
    dl = DoubleLink(iterable=[])
    assert dl._length == 0
    assert dl.head is None
    assert dl.tail is None

# verifica exceção: iterável não iterável deve levantar TypeError
def test_doublelink_init_with_non_iterable_raises_typeerror():
    with pytest.raises(TypeError):
        DoubleLink(iterable=5)
