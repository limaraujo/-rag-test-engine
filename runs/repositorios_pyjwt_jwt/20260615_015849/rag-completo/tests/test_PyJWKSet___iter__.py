import pytest
from repositorios.pyjwt.jwt.api_jwk import PyJWKSet

# verifica que __iter__ retorna um iterador sobre a attribute keys para diferentes tipos de containers (list/tuple/vazio)
@pytest.mark.parametrize("keys", [[1, 2, 3], (1, 2, 3), [], ()])
def test_pyjwkset_iter_returns_iterator_over_keys(keys):
    obj = PyJWKSet.__new__(PyJWKSet)
    obj.keys = keys
    assert list(obj) == list(keys)
