import pytest
from repositorios.pyjwt.jwt.api_jwk import PyJWKSet


# helper mock JWK-like object with required attribute
class _MockJWK:
    def __init__(self, kid: str):
        self.key_id = kid

def _make_set(keys):
    # Create an instance without calling __init__ to manually set 'keys'
    s = PyJWKSet.__new__(PyJWKSet)
    s.keys = keys
    return s

# short: happy path - key with matching kid is returned
def test_getitem_happy_path_returns_matching_jwk():
    # Verifica retorno do item existente pelo kid (caminho feliz)
    found = _MockJWK("kid-2")
    other1 = _MockJWK("kid-1")
    other2 = _MockJWK("kid-3")
    pwks = _make_set([other1, found, other2])

    result = pwks.__getitem__("kid-2")

    assert result is found
    assert result.key_id == "kid-2"

# short: edge case - missing key raises KeyError
def test_getitem_missing_key_raises_KeyError():
    # Verifica exceção KeyError quando o kid não existe (caso de borda)
    pwks = _make_set([_MockJWK("a"), _MockJWK("b")])

    with pytest.raises(KeyError) as exc:
        pwks.__getitem__("missing-kid")

    assert "keyset has no key for kid: missing-kid" in str(exc.value)
