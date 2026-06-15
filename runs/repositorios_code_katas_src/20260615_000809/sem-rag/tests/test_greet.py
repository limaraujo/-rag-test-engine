import pytest
from repositorios.code_katas.src.jenny import greet


# Testa o caminho Johnny (caso especial): retorna o cumprimento especial
def test_greet_johnny_special():
    assert greet("Johnny") == "Hello, my love!"

# Testa o caminho não Johnny com cenários equivalentes usando parametrização
@pytest.mark.parametrize("name,expected", [
    ("Alice", "Hello, Alice!"),
    ("Bob", "Hello, Bob!"),
    (123, "Hello, 123!")
])
def test_greet_other_names(name, expected):
    assert greet(name) == expected
