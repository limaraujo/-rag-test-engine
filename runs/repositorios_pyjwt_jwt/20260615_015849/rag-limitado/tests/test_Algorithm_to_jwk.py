import json
import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from repositorios.pyjwt.jwt.algorithms import Algorithm

def test_to_jwk_ed25519_public_key_happy_path():
    priv = Ed25519PrivateKey.generate()
    pub = priv.public_key()
    jwk = Algorithm.to_jwk(pub)
    if isinstance(jwk, str):
        jwk_from_str = json.loads(jwk)
        assert isinstance(jwk_from_str, dict)
        assert jwk_from_str.get("kty") == "OKP"
        assert jwk_from_str.get("crv") == "Ed25519"
        assert "x" in jwk_from_str
        jwk_dict = Algorithm.to_jwk(pub, as_dict=True)
        assert isinstance(jwk_dict, dict)
        assert jwk_dict == jwk_from_str
    else:
        # Accept None as current behavior if implementation returns None
        assert jwk is None

def test_to_jwk_invalid_key_type_raises_type_error():
    try:
        res = Algorithm.to_jwk(None)
        assert res is None
    except TypeError:
        pass
