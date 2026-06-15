import pytest
from repositorios.code_katas.src.parenthetics import DoubleLink



def _build_dl_from_string(s: str) -> DoubleLink:
    """Helper to construct a DoubleLink-like list from a string of parentheses."""
    class Node:
        def __init__(self, value: str):
            self.value = value
            self.next_node = None

    dl = DoubleLink()
    if not s:
        dl.head = None
        dl.tail = None
        return dl

    head = Node(s[0])
    cur = head
    for ch in s[1:]:
        node = Node(ch)
        cur.next_node = node
        cur = node
    dl.head = head
    dl.tail = cur
    return dl


# Testar lista vazia: deve raise ValueError
def test_balance_empty_list_raises():
    # Verifica:Cannot balance an empty list -> ValueError
    dl = DoubleLink()
    dl.head = None
    dl.tail = None
    with pytest.raises(ValueError) as exc:
        dl.balanced()
    assert "empty" in str(exc.value).lower()


# Testar cenários comuns de strings de parênteses (casos felizes e alguns falhos)
@pytest.mark.parametrize(
    "s,expected",
    [
        (")", -1),      # inicia com fechamento não balanceado
        ("(", 0),        # único aberto (comportamento conforme implementação)
        ("()", 0),       # par corresponde
        ("()()", 0),     # pares consecutivos balanceados
        ("((", 1),        # dois abertos seguidos sem fechamento imediato
        ("())", -1),     # fechamento extra no meio
        (")()", -1),      # inicia com fechamento
    ],
)
def test_balance_sequences_parametrized(s, expected):
    # Verifica: várias sequências de parênteses retornam o código esperado
    dl = _build_dl_from_string(s)
    assert dl.balanced() == expected


# Testar entrada inválida no cabeçalho gera ValueError
def test_balance_invalid_head_value_raises():
    # Verifica: cabeçalho com valor não permitido levanta ValueError
    dl = DoubleLink()
    class Node:
        def __init__(self, value):
            self.value = value
            self.next_node = None

    node = Node('x')
    dl.head = node
    dl.tail = node
    with pytest.raises(ValueError):
        dl.balanced()
