import pytest
from repositorios.pyjwt.jwt.algorithms import Algorithm

# Teste curto: verifica que check_key_length retorna None para várias entradas de chave (comportamento atual)
@pytest.mark.parametrize("key", [None, "", "a", 123, b"bytes", {"a": 1}])
def test_check_key_length_returns_none_for_various_keys(key):
    assert Algorithm.check_key_length(None, key) is None
