import pytest
from repositorios.code_katas.src.sort_cards import sort_cards

# Verifica caminho feliz: mistura de cartas resulta na ordenação correta com A valendo 0
def test_sort_cards_happy_path():
    cards = ['K', 'A', '3', '2', 'T', 'Q']
    assert sort_cards(cards) == ['A', '2', '3', 'T', 'Q', 'K']

# Verifica que entrada com carta inválida levanta KeyError
def test_sort_cards_raises_key_error_on_invalid_card():
    with pytest.raises(KeyError):
        sort_cards(['A', 'B'])

# Verifica comportamento com lista vazia
def test_sort_cards_empty_list_returns_empty():
    assert sort_cards([]) == []

# Verifica estabilidade e duplicatas: mantém ordem entre cartas com o mesmo valor
def test_sort_cards_duplicates_and_stability():
    cards = ['Q', 'A', 'Q', '2', 'A']
    assert sort_cards(cards) == ['A', 'A', '2', 'Q', 'Q']
