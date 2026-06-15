import pytest
from repositorios.code_katas.src.sort_cards import sort_cards

# curto: happy path — mistura de cartas, verifica ordenação com Ás baixo

# curto: verifica ordenação básica com várias cartas incluindo A, 2, 3, T, Q, K
def test_sort_cards_happy_path_mixes_cards():
    inputs = ["K", "A", "3", "2", "T", "Q"]
    expected = ["A", "2", "3", "T", "Q", "K"]
    assert sort_cards(inputs) == expected

# curto: verifica duplicatas são ordenadas corretamente mantendo contagens
def test_sort_cards_with_duplicates():
    inputs = ["3", "3", "A", "K", "2", "2"]
    expected = ["A", "2", "2", "3", "3", "K"]
    assert sort_cards(inputs) == expected

# curto: verifica comportamento com carta inválida levanta KeyError
def test_sort_cards_raises_on_invalid_card():
    inputs = ["A", "X", "2"]
    with pytest.raises(KeyError):
        sort_cards(inputs)

# curto: verifica entrada já ordenada permanece ordenada
def test_sort_cards_already_sorted_input_stays_sorted():
    inputs = ["A", "2", "3", "4", "5"]
    expected = ["A", "2", "3", "4", "5"]
    assert sort_cards(inputs) == expected
