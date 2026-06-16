import pytest
from repositorios.code_katas.src.parenthetics import DoubleLink

# Verifica push em lista vazia: inicializa a lista, adiciona o primeiro valor e checa head, tail e comprimento
def test_push_empty_list_initializes_head_tail_and_length():
    dl = DoubleLink()
    dl.push(10)
    assert dl.head.value == 10
    assert dl.tail.value == 10
    assert dl.head.next_node is None
    assert dl.head.previous_node is None
    assert dl._length == 1

# Verifica push em lista não vazia: adiciona segundo valor e valida encadeamento, ponteiros e comprimento
def test_push_non_empty_updates_links_and_length():
    dl = DoubleLink()
    dl.push(1)
    dl.push(2)
    # nova cabeça deve ser 2
    assert dl.head.value == 2
    # encadeamento correto: 2 -> 1
    assert dl.head.next_node.value == 1
    assert dl.head.next_node.previous_node is dl.head
    # tail deve ser o antigo head (valor 1)
    assert dl.tail.value == 1
    # comprimento deve ser 2
    assert dl._length == 2
    # o tail deve apontar para o nó anterior (head anterior)
    assert dl.tail.previous_node is dl.head

# Verifica encadeamento com três elementos: ordem correta e ponteiros entre nós
def test_push_three_elements_chain_integrity():
    dl = DoubleLink()
    for v in [1, 2, 3]:
        dl.push(v)
    # cadeia esperada: 3 -> 2 -> 1
    assert dl.head.value == 3
    assert dl.head.next_node.value == 2
    assert dl.head.next_node.next_node.value == 1
    assert dl.tail.value == 1
    # ponteiros de extremidade
    assert dl.head.previous_node is None
    assert dl.head.next_node.previous_node is dl.head
    assert dl.head.next_node.next_node.previous_node is dl.head.next_node
    assert dl.tail.next_node is None
    assert dl._length == 3
