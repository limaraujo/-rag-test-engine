import pytest
from repositorios.code_katas.src.parenthetics import DoubleLink

# happy path: sem iterable fornecido, confirma valores padrão
def test_init_without_iterable_sets_defaults():
    dl = DoubleLink()
    assert dl._length == 0
    assert dl.head is None
    assert dl.tail is None

# happy path com iterable: popula a lista e verifica head/tail e tamanho
def test_init_with_iterable_populates_and_sets_head_tail():
    dl = DoubleLink([1, 2, 3])
    assert dl._length == 3
    assert dl.head is not None
    assert dl.tail is not None
    # head deve conter o último valor empurrado (3)
    assert getattr(dl.head, "value", None) == 3
    # tail deve conter o primeiro valor inserido (1)
    assert getattr(dl.tail, "value", None) == 1

# exceção esperada: entrada não iterável porém truthy aciona TypeError durante iteração
def test_init_with_non_iterable_raises_typeerror():
    with pytest.raises(TypeError):
        DoubleLink(5)
