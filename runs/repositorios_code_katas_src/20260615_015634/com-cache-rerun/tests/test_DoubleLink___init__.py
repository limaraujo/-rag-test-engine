import pytest
from repositorios.code_katas.src.parenthetics import DoubleLink

# curto: init sem iterable -> lista vazia
def test_init_no_iterable_defaults():
    ll = DoubleLink()
    assert ll._length == 0
    assert ll.head is None
    assert ll.tail is None

# curto: init com iterable -> constrói lista com head na última inserção e tail na primeira
def test_init_with_iterable_builds_correctly():
    ll = DoubleLink([1, 2, 3])
    assert ll._length == 3
    assert ll.head.value == 3
    assert ll.tail.value == 1
    # verifique ligações entre nós
    assert ll.head.next_node is not None
    assert ll.head.next_node.value == 2
    assert ll.head.next_node.next_node.value == 1
    assert ll.head.previous_node is None
    assert ll.tail.next_node is None
    assert ll.tail.previous_node.value == 2

# curto: init com não-iterável levanta TypeError
def test_init_with_non_iterable_raises_typeerror():
    with pytest.raises(TypeError):
        DoubleLink(5)
