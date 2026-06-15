import pytest
from repositorios.pyjwt.jwt.algorithms import Algorithm

# curto: happy path - check_key_length devolve None para diversos tipos de key
@pytest.mark.parametrize("key", [
    "short",
    123,
    None,
    b"",
    {"k": "v"},
    [1, 2, 3],
])
def test_check_key_length_always_none_for_various_keys(key):
    assert Algorithm.check_key_length(None, key) is None
