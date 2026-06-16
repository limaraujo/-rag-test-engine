import pytest
from repositorios.pyjwt.jwt.api_jwk import PyJWKSet

@pytest.mark.parametrize("input_obj, expected_keys", [
    ({"keys": [{"kid": "a"}, {"kid": "b"}]}, [{"kid": "a"}, {"kid": "b"}]),
    ({}, [])
])
def test_from_dict_builds_jwkset_from_dict(input_obj, expected_keys, monkeypatch):
    # Patch PyJWKSet.__init__ to avoid cryptography dependency during tests
    def fake_init(self, keys):
        self.keys = keys

    monkeypatch.setattr(PyJWKSet, "__init__", fake_init, raising=True)

    result = PyJWKSet.from_dict(input_obj)
    assert isinstance(result, PyJWKSet)
    assert result.keys == expected_keys
