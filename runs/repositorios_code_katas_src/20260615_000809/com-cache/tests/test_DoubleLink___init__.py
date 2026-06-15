import pytest
from repositorios.code_katas.src.parenthetics import DoubleLink

# Verifica o caminho feliz: inicialização sem iterable mantém lista vazia
def test_init_without_iterable_empty_list():
    dl = DoubleLink()
    assert dl.head is None
    assert dl.tail is None
    assert dl._length == 0

# Verifica caminho feliz com iterable não-vazio: itens são adicionados no front (ordem invertida)
def test_init_with_iterable_pushes_values_in_front_order():
    dl = DoubleLink([1, 2, 3])
    assert dl._length == 3
    assert dl.head.value == 3
    assert dl.head.next_node.value == 2
    assert dl.head.next_node.next_node.value == 1
    assert dl.tail.value == 1
    assert dl.tail.next_node is None
    assert dl.tail.previous_node.value == 2

# Verifica exceção TypeError quando iterable fornecido não é iterável
def test_init_with_non_iterable_raises_typeerror():
    with pytest.raises(TypeError):
        DoubleLink(123)

# Verifica comportamento com iterable vazia explícito
def test_init_with_empty_iterable_results_no_items():
    dl = DoubleLink([])
    assert dl.head is None
    assert dl.tail is None
    assert dl._length == 0
