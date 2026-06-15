from repositorios.code_katas.src.parenthetics import DoubleLink

# happy path: push into an empty doubly linked list initializes head and tail correctly
def test_push_into_empty_list():
    dl = DoubleLink()
    dl.push(10)
    assert dl.head.value == 10
    assert dl.tail.value == 10
    assert dl.head.previous_node is None
    assert dl.head.next_node is None
    assert dl._length == 1

# happy path: pushing onto a non-empty list updates head, maintains links, and increments length
def test_push_into_non_empty_list_updates_pointers_and_length():
    dl = DoubleLink()
    dl.push(1)
    dl.push(2)
    # New head should be the most recently pushed value
    assert dl.head.value == 2
    # New head should point to the previous head
    assert dl.head.next_node.value == 1
    assert dl.head.next_node.previous_node is dl.head
    # Tail should be the first pushed value and remain terminal
    assert dl.tail.value == 1
    assert dl.tail.next_node is None
    assert dl._length == 2
