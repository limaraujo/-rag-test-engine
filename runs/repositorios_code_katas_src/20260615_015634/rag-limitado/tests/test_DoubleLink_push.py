import pytest
from repositorios.code_katas.src.parenthetics import DoubleLink



# verifica o caminho feliz: push em lista vazia atualiza head, tail e length
def test_push_into_empty_list_sets_head_tail_and_length():
    dll = DoubleLink()
    dll.push(10)

    assert dll.head is not None
    assert dll.head.value == 10
    assert dll.head.next_node is None
    assert getattr(dll.head, "previous_node", None) is None
    assert dll.tail is dll.head
    assert dll._length == 1


# verifica o caminho no caso em que já existe pelo menos um nó: atualiza ponteiros corretamente
def test_push_into_non_empty_list_updates_links_and_length():
    dll = DoubleLink()
    dll.push(10)
    first = dll.head  # eventual tail antes do segundo push

    dll.push(20)  # novo nó deve se tornar head

    new_head = dll.head
    assert new_head.value == 20
    assert new_head.next_node is first
    assert first.previous_node is new_head
    assert dll.tail is first  # o tail não deve mudar ao adicionar no começo
    assert dll._length == 2

    # o antigo head (agora segundo) ainda deve apontar para None em next_node
    assert first.next_node is None
