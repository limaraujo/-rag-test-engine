import pytest
from repositorios.code_katas.src.parenthetics import DoubleLink

# happy path: inicialização sem iterable resulta em lista vazia
def test_init_without_iterable_creates_empty_list():
    dl = DoubleLink()
    assert dl._length == 0
    assert dl.head is None
    assert dl.tail is None

# happy path: inicialização com iterable não vazio popula o tamanho corretamente
def test_init_with_iterable_populates_length():
    dl = DoubleLink([1, 2, 3])
    assert dl._length == 3

# borda: iterable vazio não altera estado
def test_init_with_empty_iterable_results_in_empty():
    dl = DoubleLink([])
    assert dl._length == 0
    assert dl.head is None
    assert dl.tail is None

# exceção: não-iterável (valor inteiro) levanta TypeError durante iteração
def test_init_with_non_iterable_raises_typeerror():
    with pytest.raises(TypeError):
        DoubleLink(5)
