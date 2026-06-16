import pytest
from repositorios.code_katas.src.sort_cards import sort_cards

# Verifica ordenação básica (happy path)
def test_sort_cards_happy_path():
    cards = ["K", "A", "3", "T"]
    assert sort_cards(cards) == ["A", "3", "T", "K"]

# Verifica que lista já ordenada permanece ordenada (idempotente)
def test_sort_cards_idempotent_when_already_sorted():
    cards = ["A", "2", "3", "T", "K"]
    assert sort_cards(cards) == ["A", "2", "3", "T", "K"]

# Verifica estabilidade com duplicatas (ordem relativa de iguais mantida)
def test_sort_cards_stability_with_duplicates():
    cards = ["Q", "A", "Q", "J", "2"]
    assert sort_cards(cards) == ["A", "2", "J", "Q", "Q"]

# Verifica exceção para entrada inválida
def test_sort_cards_raises_key_error_on_invalid():
    with pytest.raises(KeyError):
        sort_cards(["Z"])
