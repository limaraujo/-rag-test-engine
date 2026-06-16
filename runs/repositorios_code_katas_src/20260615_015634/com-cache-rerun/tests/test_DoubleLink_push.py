from repositorios.code_katas.src.parenthetics import DoubleLink

# curto: push em lista vazia define head e tail iguais, incrementa length
def test_push_on_empty_list_sets_head_tail_and_length():
    ll = DoubleLink()
    ll.push('a')
    assert ll.head is ll.tail
    assert ll.head.value == 'a'
    assert ll._length == 1
    assert ll.head.next_node is None
    assert ll.head.previous_node is None

# curto: push em lista não-vazia atualiza links entre nodes e comprimento
def test_push_on_non_empty_list_updates_links_and_length():
    ll = DoubleLink()
    ll.push('a')
    ll.push('b')
    assert ll.head.value == 'b'
    assert ll.head.next_node.value == 'a'
    assert ll.head.next_node.previous_node is ll.head
    assert ll.tail.value == 'a'
    assert ll.tail.previous_node.value == 'b'
    assert ll._length == 2

# curto: múltiplos pushes criam cadeia reversa e atualizam comprimento
def test_push_multiple_values_builds_reverse_chain_and_length():
    ll = DoubleLink()
    for v in [1, 2, 3]:
        ll.push(v)
    assert ll.head.value == 3
    assert ll.head.next_node.value == 2
    assert ll.head.next_node.next_node.value == 1
    assert ll.tail.value == 1
    assert ll.tail.previous_node.value == 2
    assert ll._length == 3
