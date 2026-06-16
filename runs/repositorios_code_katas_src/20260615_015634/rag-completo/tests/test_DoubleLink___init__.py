import pytest
from repositorios.code_katas.src.parenthetics import DoubleLink

# verifica caminho feliz sem iterável: cria lista vazia (length 0, head e tail None)
def test_init_without_iterable_sets_empty():
    dl = DoubleLink()
    assert dl._length == 0
    assert dl.head is None
    assert dl.tail is None

# verifica caminho com iterable válido (lista) -> itens são adicionados na frente, ordem invertida, tamanho correto, e navegação entre nós
def test_init_with_iterable_populates_in_reverse_order():
    dl = DoubleLink([1, 2, 3])
    assert dl._length == 3
    assert dl.head.value == 3
    assert dl.tail.value == 1

    values = []
    current = dl.head
    while current:
        values.append(current.value)
        current = current.next_node
    assert values == [3, 2, 1]

# verifica exceção TypeError ao passar valor não iterável (truthy) para iterable
def test_init_with_non_iterable_raises_typeerror():
    with pytest.raises(TypeError):
        DoubleLink(5)
