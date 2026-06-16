from repositorios.code_katas.src.parenthetics import DoubleLink

# verifica push em lista não vazia: adiciona no front e atualiza ligações
def test_push_on_non_empty_list():
    dl = DoubleLink()
    dl.push(1)
    old_head = dl.head
    initial_len = dl._length

    dl.push(2)
    new_head = dl.head

    assert new_head.value == 2
    assert new_head.next_node is old_head
    assert old_head.previous_node is new_head
    assert dl._length == initial_len + 1
    assert dl.tail is old_head

# verifica push em lista vazia: inicializa head/tail e incrementa comprimento
def test_push_on_empty_list():
    dl = DoubleLink()
    initial_len = dl._length

    dl.push(10)
    head = dl.head
    tail = dl.tail

    assert head is tail
    assert head.value == 10
    assert head.next_node is None
    assert head.previous_node is None
    assert dl._length == initial_len + 1
