import pytest
from repositorios.pyjwt.jwt.algorithms import Algorithm

# curto: verifica caminho feliz - retorna None para várias entradas de chave
@pytest.mark.parametrize("key", [
    "short",
    "this_is_a_reasonably_long_key",
    b"bytes_key_example",
    None,
    12345,
])
def test_check_key_length_always_none_for_various_inputs(key):
    assert Algorithm.check_key_length(None, key) is None
