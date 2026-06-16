import json
import pytest
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec  # for non-RSA key in test
from repositorios.pyjwt.jwt.algorithms import RSAAlgorithm

# happy path: verify JSON string contains RSA components for a private RSA key
def test_to_jwk_returns_json_string_with_rsa_components():
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
    result = RSAAlgorithm.to_jwk(key, as_dict=False)
    assert isinstance(result, str)
    data = json.loads(result)
    assert data.get("kty") == "RSA"
    assert "n" in data and "e" in data
    assert isinstance(data["n"], str) and isinstance(data["e"], str)
    if "d" in data:
        assert isinstance(data["d"], str)

# dictionary output: verify that as_dict=True returns a dict with RSA components
def test_to_jwk_returns_dict_when_as_dict_true():
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
    result = RSAAlgorithm.to_jwk(key, as_dict=True)
    assert isinstance(result, dict)
    assert result.get("kty") == "RSA"
    assert "n" in result and "e" in result
    assert isinstance(result["n"], str) and isinstance(result["e"], str)

# edge/exc path: non-RSA key should raise an error
def test_to_jwk_raises_with_non_rsa_key():
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
    ec_key = ec.generate_private_key(ec.SECP256R1(), backend=default_backend())
    with pytest.raises(Exception):
        RSAAlgorithm.to_jwk(ec_key)
