import pytest
from repositorios.code_katas.src.string_pyramid import count_all_characters_of_the_pyramid

# curto: happy path com entradas não vazias de diferentes comprimentos
@pytest.mark.parametrize("characters", ["A", "ABC", "ABCD"])
def test_count_all_characters_of_the_pyramid_happy_path_various_lengths(characters):
    # Verifica cálculo correto da soma dos quadrados de números ímpares para comprimentos variados
    expected = sum((2 * i - 1) ** 2 for i in range(1, len(characters) + 1))
    assert count_all_characters_of_the_pyramid(characters) == expected

# curto: borda/condição falsy (entrada vazia) deve retornar -1
def test_count_all_characters_of_the_pyramid_empty_string_returns_minus_one():
    assert count_all_characters_of_the_pyramid("") == -1
