import pytest
from repositorios.code_katas.src.jenny import greet

# Verifica branchs: Johnny recebe saudação especial; outros nomes recebem saudação padrão
@pytest.mark.parametrize("name,expected", [
    ("Johnny", "Hello, my love!"),  # branch True
    ("Alice", "Hello, Alice!"),     # branch False
])
def test_greet(name, expected):
    assert greet(name) == expected
