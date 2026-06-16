import pytest
from repositorios.pyjwt.jwt.api_jwk import PyJWKSet

class _DummyKey:
    def __init__(self, kid: str):
        self.key_id = kid

def _make_set(keys):
    s = PyJWKSet.__new__(PyJWKSet)
    s.keys = keys
    return s

# curto: happy path - retorna a chave com key_id igual ao kid fornecido
def test_getitem_returns_matching_key():
    k1 = _DummyKey("kid1")
    k2 = _DummyKey("kid2")
    s = _make_set([k1, k2])
    assert s["kid2"] is k2

# curto: borda - levanta KeyError quando o kid não existe na keyset
def test_getitem_raises_keyerror_when_missing():
    s = _make_set([_DummyKey("kid1")])
    with pytest.raises(KeyError, match="keyset has no key for kid: missing"):
        _ = s["missing"]
