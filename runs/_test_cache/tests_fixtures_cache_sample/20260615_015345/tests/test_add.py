import pytest
from tests.fixtures.cache_sample.add import add



# Happy path: chamada válida retorna um resultado.
def test_add_happy_path():
    result = add(1, 2)
    assert result is not None
