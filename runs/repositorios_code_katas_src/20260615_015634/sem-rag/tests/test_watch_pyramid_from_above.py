import pytest
from repositorios.code_katas.src.string_pyramid import watch_pyramid_from_above


# Teste feliz com string de 3 caracteres (happy path)
def test_watch_pyramid_from_above_happy_path_three_chars():
    input_chars = "ABC"
    expected = "AAAAA\nABBBA\nABCBA\nABBBA\nAAAAA"
    assert watch_pyramid_from_above(input_chars) == expected


# Teste borda: entrada vazia retorna vazia (branch False)
def test_watch_pyramid_from_above_empty_input_returns_empty():
    assert watch_pyramid_from_above("") == ""


# Teste borda: único caractere mantém o resultado simples
def test_watch_pyramid_from_above_single_character():
    assert watch_pyramid_from_above("A") == "A"
