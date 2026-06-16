import json
import pytest
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
from repositorios.pyjwt.jwt.algorithms import ECAlgorithm

# short: happy path - valid EC key yields a JSON string representing a JWK with EC fields
def test_ec_algorithm_to_jwk_happy_path():
    private_key = ec.generate_private_key(ec.SECP256R1(), backend=default_backend())
    jwk_json = ECAlgorithm.to_jwk(private_key, as_dict=False)
    assert isinstance(jwk_json, str)
    data = json.loads(jwk_json)
    assert isinstance(data, dict)
    assert data.get("kty") == "EC"
    assert isinstance(data.get("crv"), str) and data["crv"]
    assert isinstance(data.get("x"), str) and data["x"]
    assert isinstance(data.get("y"), str) and data["y"]

# short: error path - non-key input should raise an exception
def test_ec_algorithm_to_jwk_invalid_input_raises():
    with pytest.raises(Exception):
        ECAlgorithm.to_jwk("notakey")
