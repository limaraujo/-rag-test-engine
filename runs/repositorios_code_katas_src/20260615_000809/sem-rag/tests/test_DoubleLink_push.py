import pytest
from repositorios.code_katas.src.parenthetics import DoubleLink



# Teste ao empurrar para lista vazia: verifica head, tail, tamanho e ligações
def test_push_on_empty_list_sets_head_and_tail_and_length():
    dl = DoubleLink()
    dl.push(1)

    # Head e tail devem apontar para o mesmo nó
    assert dl.head is not None
    assert dl.tail is not None
    assert dl.head is dl.tail

    node = dl.head
    # Verifica valor armazenado no nó (supondo atributo value)
    assert hasattr(node, "value")
    assert node.value == 1

    # Sem next/previous no único nó
    assert node.next_node is None
    assert node.previous_node is None

    # Comprimento correto
    assert dl._length == 1


# Teste ao empurrar quando já há elementos: verifica re-conexões, head atualizado, tail preservado e comprimento
def test_push_on_non_empty_list_updates_head_and_links_and_length():
    dl = DoubleLink()
    dl.push(1)
    first_head = dl.head

    dl.push(2)
    new_head = dl.head

    # Novo head deve ter o novo valor
    assert hasattr(new_head, "value")
    assert new_head.value == 2

    # Ligações entre nós: novo_head aponta para o antigo head e este aponta de volta
    assert new_head.next_node is first_head
    assert first_head.previous_node is new_head

    # Tail permanece o último nó da lista antiga
    assert dl.tail is first_head

    # Comprimento atualizado
    assert dl._length == 2
