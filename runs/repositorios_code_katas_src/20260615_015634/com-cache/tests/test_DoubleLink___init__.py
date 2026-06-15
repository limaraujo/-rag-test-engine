import pytest
from repositorios.code_katas.src.parenthetics import DoubleLink

# happy path: no iterable provided -> empty list
def test_init_no_iterable_defaults():
    ll = DoubleLink()
    assert ll._length == 0
    assert ll.head is None
    assert ll.tail is None

# happy path: iterable provided -> pushes values to front, order reversed
def test_init_with_list_populates_front():
    ll = DoubleLink([1, 2, 3])
    assert ll._length == 3
    assert ll.head.value == 3
    assert ll.tail.value == 1
    # traverse from head to tail to verify order
    values = []
    node = ll.head
    while node:
        values.append(node.value)
        node = node.next_node
    assert values == [3, 2, 1]

# edge case: non-iterable passed where iterable is expected -> TypeError raised
def test_init_with_non_iterable_raises_type_error():
    with pytest.raises(TypeError):
        DoubleLink(1)

# edge case: empty iterable should not raise and produce an empty list
def test_init_with_empty_iterable_results_in_empty():
    ll = DoubleLink([])
    assert ll._length == 0
    assert ll.head is None
    assert ll.tail is None
