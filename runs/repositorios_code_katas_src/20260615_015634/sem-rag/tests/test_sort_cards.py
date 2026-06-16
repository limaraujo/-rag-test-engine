import pytest
from repositorios.code_katas.src.sort_cards import sort_cards

# verifica ordenação básica (caso feliz)
def test_happy_path_basic_sort():
    cards = ["K", "A", "Q", "2"]
    assert sort_cards(cards) == ["A", "2", "Q", "K"]

# verifica ordenação completa de todos os ranks (caso feliz)
def test_all_ranks_sorted_ascending():
    cards = ["Q", "3", "A", "K", "2", "T", "J", "5", "4", "9", "6", "7", "8"]
    assert sort_cards(cards) == ["A", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K"]

# verifica erro para carta inválida (exceção)
def test_invalid_card_raises_keyerror():
    with pytest.raises(KeyError):
        sort_cards(["X"])

# verifica que A fica no início em deck misto (caso de borda)
def test_ace_lowest_in_mixed_deck():
    cards = ["A", "4", "A", "2", "K", "T", "J"]
    assert sort_cards(cards) == ["A", "A", "2", "4", "T", "J", "K"]
