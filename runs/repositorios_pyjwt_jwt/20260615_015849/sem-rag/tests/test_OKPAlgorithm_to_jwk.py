import json
import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from repositorios.pyjwt.jwt.exceptions import InvalidKeyError
from repositorios.pyjwt.jwt.algorithms import OKPAlgorithm

# happy path: verify Ed25519 public key converts to JWK for both string and dict outputs
@pytest.mark.parametrize("as_dict", [False, True])
def test_okp_to_jwk_happy_path(as_dict):
    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()
    jwk = OKPAlgorithm.to_jwk(public_key, as_dict=as_dict)
    if as_dict:
        assert isinstance(jwk, dict)
        jwk_dict = jwk
    else:
        assert isinstance(jwk, str)
        jwk_dict = json.loads(jwk)
    assert isinstance(jwk_dict, dict)
    assert jwk_dict.get("kty") == "OKP"
    assert jwk_dict.get("crv") == "Ed25519"
    assert "x" in jwk_dict and isinstance(jwk_dict["x"], str) and jwk_dict["x"]

def test_okp_to_jwk_invalid_key_type():
    with pytest.raises(InvalidKeyError):
        OKPAlgorithm.to_jwk(1234, as_dict=False)
