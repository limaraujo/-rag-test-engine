import pytest
from repositorios.pyjwt.jwt.api_jwk import PyJWKSet


class FakeKey:
    def __init__(self, kid: str):
        self.key_id = kid

def test_getitem_happy_path():
    # verifique retorno da chave correta (happy path)
    instance = PyJWKSet.__new__(PyJWKSet)
    instance.keys = [FakeKey("kid1"), FakeKey("kid2"), FakeKey("kid3")]
    result = PyJWKSet.__getitem__(instance, "kid2")
    assert isinstance(result, FakeKey)
    assert result.key_id == "kid2"

def test_getitem_missing_key_raises_keyerror():
    # verifique exceção KeyError quando key_id não existe (caso borda: missing_key)
    instance = PyJWKSet.__new__(PyJWKSet)
    instance.keys = [FakeKey("kid1"), FakeKey("kid3")]
    with pytest.raises(KeyError) as excinfo:
        PyJWKSet.__getitem__(instance, "missing_kid")
    assert excinfo.value.args[0] == "keyset has no key for kid: missing_kid"
