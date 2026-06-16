import pytest
from repositorios.code_katas.src.parenthetics import DoubleLink

class Node:
    def __init__(self, value, next_node=None):
        self.value = value
        self.next_node = next_node
    def __eq__(self, other):
        if isinstance(other, Node):
            return self is other
        if isinstance(other, str):
            return self.value == other
        return False

def build_list(values):
    head = None
    tail = None
    for v in values:
        node = Node(v)
        if head is None:
            head = tail = node
        else:
            tail.next_node = node
            tail = node
    dl = DoubleLink()
    dl.head = head
    dl.tail = tail
    return dl

# Verifica retorno 0 para parênteses simples balanced (happy path)
def test_balanced_happy_path_simple_pair():
    dl = build_list(['(', ')'])
    assert dl.balanced() == 0

# Verifica retorno 1 quando há parêntese aberto não fechando (caso de borda)
def test_balanced_unmatched_open_returns_one():
    dl = build_list(['('])
    assert dl.balanced() == 1

# Verifica retorno -1 quando há parêntese fechado não correspondido no início (caso de borda)
def test_balanced_unmatched_closed_returns_minus_one():
    dl = build_list([')'])
    assert dl.balanced() == -1

# Verifica ValueError para entrada inválida (caso invalid_input)
def test_balanced_invalid_input_raises_value_error():
    with pytest.raises(ValueError):
        dl = build_list(['x'])
        dl.balanced()
