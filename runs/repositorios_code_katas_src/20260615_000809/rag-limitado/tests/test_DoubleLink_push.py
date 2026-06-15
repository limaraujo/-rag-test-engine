from repositorios.code_katas.src.parenthetics import DoubleLink


# Test: happy path when pushing into an empty list creates a single node and sets both head and tail
def test_push_on_empty_list_creates_single_node_and_sets_head_tail_length():
    dl = DoubleLink()
    dl.push(10)
    assert dl.head is not None
    assert dl.tail is not None
    assert dl.head.value == 10
    assert dl.tail.value == 10
    assert dl.head is dl.tail
    assert dl._length == 1
    assert dl.head.next_node is None
    assert dl.head.previous_node is None


# Test: push on non-empty list updates head, links, and increments length
def test_push_on_non_empty_list_updates_head_and_links_and_increments_length():
    dl = DoubleLink()
    dl.push(1)
    dl.push(2)
    # After second push, head should be 2 and point to 1
    assert dl.head.value == 2
    assert dl.head.next_node.value == 1
    assert dl.head.next_node.previous_node is dl.head
    # Tail should remain the first element and link back to new head
    assert dl.tail.value == 1
    assert dl.tail.next_node is None
    assert dl.tail.previous_node is dl.head
    assert dl._length == 2
