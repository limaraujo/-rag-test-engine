import pytest
from repositorios.code_katas.src.jenny import greet

# Verifica greet para Johnny (branch quando name == "Johnny") e para outros nomes (caminho padrão) usando parametrização
@pytest.mark.parametrize("name,expected", [
    ("Johnny", "Hello, my love!"),
    ("Alice", "Hello, Alice!")
])
def test_greet_various_names(name, expected):
    assert greet(name) == expected
