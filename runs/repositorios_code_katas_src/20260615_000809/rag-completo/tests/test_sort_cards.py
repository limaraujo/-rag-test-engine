import pytest
from repositorios.code_katas.src.sort_cards import sort_cards

# curto: happy path - sorts a mixed deck by rank with Ace as 0

def test_sort_cards_happy_path():
    cards = ["Q", "A", "5", "K", "2"]
    assert sort_cards(cards) == ["A", "2", "5", "Q", "K"]

# curto: edge case - empty input returns empty
def test_sort_cards_empty_list():
    assert sort_cards([]) == []

# curto: error handling - invalid card raises KeyError
def test_sort_cards_invalid_card_raises():
    with pytest.raises(KeyError):
        sort_cards(["A", "B", "3"])
