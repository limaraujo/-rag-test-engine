import pytest
from types import SimpleNamespace
from repositorios.pyjwt.jwt.api_jwk import PyJWKSet

# curto: happy path - encontra e retorna a chave correspondente ao kid presente
def test_getitem_returns_matching_key():
    jwks = PyJWKSet.__new__(PyJWKSet)
    matching_key = SimpleNamespace(key_id="kid-1")
    jwks.keys = [matching_key, SimpleNamespace(key_id="kid-2")]
    assert jwks.__getitem__("kid-1") is matching_key

# curto: missing key - lança KeyError quando o kid não existe no conjunto
def test_getitem_missing_key_raises_keyerror():
    jwks = PyJWKSet.__new__(PyJWKSet)
    jwks.keys = [SimpleNamespace(key_id="a"), SimpleNamespace(key_id="b")]
    with pytest.raises(KeyError) as exc:
        jwks.__getitem__("c")
    assert "keyset has no key for kid: c" in str(exc.value)
