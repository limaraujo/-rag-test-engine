from repositorios.code_katas.src.parenthetics import DoubleLink


# curto: happy path - push into empty list creates head/tail and length 1
def test_push_into_empty_list_creates_head_and_tail():
    dl = DoubleLink()
    dl.push(10)

    assert dl.head is not None
    assert dl.tail is dl.head
    assert dl.head.value == 10
    assert dl.head.next_node is None
    assert dl.head.previous_node is None
    assert dl._length == 1


# curto: branch - push into non-empty list updates links and length
def test_push_into_non_empty_updates_links_and_length():
    dl = DoubleLink()
    dl.push(10)
    dl.push(20)

    assert dl.head.value == 20
    assert dl.head.next_node.value == 10
    assert dl.head.next_node.previous_node is dl.head
    assert dl.tail.value == 10
    assert dl.tail.next_node is None
    assert dl.tail.previous_node is dl.head
    assert dl._length == 2
