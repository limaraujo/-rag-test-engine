import pytest
from repositorios.code_katas.src.sort_cards import sort_cards

# Verifica ordenação correta de uma sequência misturada (happy path)
def test_happy_path_basic_sorting():
    cards = ['K', '2', 'A', '5', 'T', 'J', 'Q', '3', '4', '9', '8', '6', '7']
    expected = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
    assert sort_cards(cards) == expected

# Verifica que duplicatas são ordenadas corretamente (caso com repetições)
def test_sorting_with_duplicates():
    cards = ['3', 'A', '3', 'K', '2', 'A']
    expected = ['A', 'A', '2', '3', '3', 'K']
    assert sort_cards(cards) == expected

# Verifica lançamento de KeyError para símbolo inválido
def test_invalid_card_raises_keyerror():
    with pytest.raises(KeyError):
        sort_cards(['X'])
