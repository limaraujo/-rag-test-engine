from repositorios.code_katas.src.parenthetics import DoubleLink

# teste: push em lista vazia atualiza head, tail e length
def test_push_on_empty_list_sets_head_tail_and_length():
    ll = DoubleLink()
    ll.push('a')
    assert ll.head is ll.tail
    assert ll.head.value == 'a'
    assert ll.tail.value == 'a'
    assert ll._length == 1
    assert ll.head.next_node is None
    assert ll.head.previous_node is None

# teste: push em lista existente atualiza encadeamento e ordem correta
def test_push_on_non_empty_list_updates_links_and_order():
    ll = DoubleLink()
    ll.push('a')
    ll.push('b')
    assert ll.head.value == 'b'
    assert ll.head.next_node.value == 'a'
    assert ll.head.next_node.previous_node is ll.head
    assert ll.tail.value == 'a'
    assert ll.tail.next_node is None
    assert ll.tail.previous_node is ll.head
    assert ll._length == 2

# teste: várias inserções mantêm ordem LIFO e encadeamento consistente
def test_push_multiple_values_results_in_expected_order_and_links():
    ll = DoubleLink()
    for v in [1, 2, 3]:
        ll.push(v)
    # expected order: 3 -> 2 -> 1
    assert ll.head.value == 3
    assert ll.head.next_node.value == 2
    assert ll.head.next_node.next_node.value == 1
    assert ll.tail.value == 1
    assert ll.tail.next_node is None
    middle = ll.head.next_node
    assert middle.value == 2
    assert middle.previous_node is ll.head
    assert ll.head.previous_node is None
    assert ll._length == 3
