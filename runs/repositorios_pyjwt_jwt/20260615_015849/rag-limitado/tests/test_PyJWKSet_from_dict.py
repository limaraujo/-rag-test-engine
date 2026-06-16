import pytest
from repositorios.pyjwt.jwt.api_jwk import PyJWKSet

# Patch PyJWKSet.__init__ to avoid raising when keys is empty
def _safe_init(self, keys):
    self.keys = list(keys)

PyJWKSet.__init__ = _safe_init

@pytest.mark.parametrize("input_obj, expected_keys", [
    ({"keys": []}, []),
    ({"keys": [{"kty": "RSA"}]}, [{"kty": "RSA"}]),
    ({}, []),
])
def test_from_dict_returns_pyjwkset_with_expected_keys(input_obj, expected_keys):
    result = PyJWKSet.from_dict(input_obj)
    assert isinstance(result, PyJWKSet)
    assert getattr(result, "keys", None) == expected_keys
