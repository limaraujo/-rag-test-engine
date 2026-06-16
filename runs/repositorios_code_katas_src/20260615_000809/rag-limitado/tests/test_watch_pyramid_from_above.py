import pytest
from repositorios.code_katas.src.string_pyramid import watch_pyramid_from_above

# Verifica caminho principal (ABC) e casos de borda (A, "", None) com um único test parametrizado
@pytest.mark.parametrize("input_chars, expected", [
    ("ABC", "AAAAA\nABBBA\nABCBA\nABBBA\nAAAAA"),
    ("A", "A"),
    ("", ""),
    (None, None),
])
def test_watch_pyramid_from_above_various_inputs(input_chars, expected):
    assert watch_pyramid_from_above(input_chars) == expected
