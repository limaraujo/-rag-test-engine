import pytest
from repositorios.code_katas.src.jenny import greet

# Verifica branch: Johnny recebe saudação especial; outros nomes recebem saudação normal
@pytest.mark.parametrize("name,expected", [
    ("Johnny", "Hello, my love!"),
    ("Alice", "Hello, Alice!"),
])
def test_greet_variants(name, expected):
    assert greet(name) == expected
