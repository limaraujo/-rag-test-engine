import pytest
from repositorios.pyjwt.jwt.api_jwk import PyJWKSet

class FakeKey:
    def __init__(self, kid: str):
        self.key_id = kid

def _build_jwkset_with_keys(ids):
    # Create a PyJWKSet-like instance without calling __init__
    jwkset = PyJWKSet.__new__(PyJWKSet)
    jwkset.keys = [FakeKey(k) for k in ids]
    return jwkset, jwkset.keys

# curto: happy path - retorna o PyJWK correspondente quando o kid existe
def test_getitem_returns_existing_key():
    jwkset, keys = _build_jwkset_with_keys(["kid1", "kid2"])
    result = jwkset.__getitem__("kid2")
    assert result is keys[1]

# curto: exceção KeyError quando o kid não existe
def test_getitem_raises_keyerror_for_missing_kid():
    jwkset, _ = _build_jwkset_with_keys(["existing"])
    with pytest.raises(KeyError) as exc:
        jwkset.__getitem__("missing")
    assert exc.value.args[0] == "keyset has no key for kid: missing"
