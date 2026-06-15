import pytest
from repositorios.code_katas.src.sort_cards import sort_cards

# feliz caminho: ordena uma lista mista de cartas pela hierarquia correta
def test_sort_cards_happy_path():
    cards = ['3', 'A', 'K', '2', 'T']
    assert sort_cards(cards) == ['A', '2', '3', 'T', 'K']

# bordas: entradas vazias e de tamanho único
@pytest.mark.parametrize("cards, expected", [
    ([], []),
    (['A'], ['A']),
])
def test_sort_cards_empty_and_single(cards, expected):
    assert sort_cards(cards) == expected

# exceção: entradas com carta inválida geram KeyError
def test_sort_cards_invalid_card_raises_keyerror():
    with pytest.raises(KeyError):
        sort_cards(['A', 'X'])
