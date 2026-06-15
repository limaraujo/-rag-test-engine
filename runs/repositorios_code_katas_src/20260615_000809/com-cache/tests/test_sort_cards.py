import pytest
from repositorios.code_katas.src.sort_cards import sort_cards

# Verifica ordenação correta de uma lista desalinhada com várias cartas, cobrindo múltiplos cenários (happy path via parametrização)
@pytest.mark.parametrize("cards,expected", [
    (["3","A","K","2","T","Q"], ["A","2","3","T","Q","K"]),
    (["K","Q","J","A","2","3","4","5","6","7","8","9","T"],
     ["A","2","3","4","5","6","7","8","9","T","J","Q","K"]),
    (["9","7","5","A","T","2"], ["A","2","5","7","9","T"]),
])
def test_sort_cards_happy_path(cards, expected):
    assert sort_cards(cards) == expected

# Confirma que entrada já ordenada permanece ordenada (caminho feliz adicional)
def test_sort_cards_idempotent_sorted_input():
    cards = ["A","2","3","4","5","6","7","8","9","T","J","Q","K"]
    assert sort_cards(cards) == cards

# Verifica exceção ao encontrar uma carta inválida (exceção KeyError)
def test_sort_cards_invalid_input_raises():
    with pytest.raises(KeyError):
        sort_cards(["A","Z"])

# Verifica que Ás atua como menor valor mesmo quando presente com outras cartas (caso borde)
def test_sort_cards_ace_low_edge_case():
    cards = ["K","A","Q","2"]
    assert sort_cards(cards) == ["A","2","Q","K"]
