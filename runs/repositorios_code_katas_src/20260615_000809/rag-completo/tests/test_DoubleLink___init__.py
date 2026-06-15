import pytest
from repositorios.code_katas.src.parenthetics import DoubleLink

# happy path: init with list preserves length and builds proper head chain
def test_init_with_list_happy_path():
    dl = DoubleLink([1, 2, 3])
    assert dl._length == 3
    assert dl.head is not None
    assert dl.head.value == 3
    assert dl.head.next_node is not None
    assert dl.head.next_node.value == 2
    assert dl.head.next_node.next_node is not None
    assert dl.head.next_node.next_node.value == 1
    assert dl.head.next_node.next_node.next_node is None

# edge case: empty iterable results in empty list (head and tail remain None)
def test_init_with_empty_iterable_edge():
    dl = DoubleLink([])
    assert dl._length == 0
    assert dl.head is None
    assert dl.tail is None

# happy path: init with generator iterable yields correct length and head value
def test_init_with_generator_happy_path():
    dl = DoubleLink(x for x in range(4))
    assert dl._length == 4
    assert dl.head.value == 3

# exception: non-iterable input raises TypeError during iteration
def test_init_with_non_iterable_raises():
    with pytest.raises(TypeError):
        DoubleLink(5)
