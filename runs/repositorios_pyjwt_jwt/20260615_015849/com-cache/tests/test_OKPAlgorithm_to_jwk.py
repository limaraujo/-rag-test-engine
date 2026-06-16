import json
import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from repositorios.pyjwt.jwt.algorithms import OKPAlgorithm

# happy path: Ed25519 private key yields JWK with kty, crv and x fields
def test_to_jwk_okp_ed25519_happy_path():
    key = Ed25519PrivateKey.generate()
    alg = OKPAlgorithm()
    jwk_str = alg.to_jwk(key)
    jwk = json.loads(jwk_str)
    assert jwk.get("kty") == "OKP"
    assert jwk.get("crv") == "Ed25519"
    assert "x" in jwk

# exception path: non-OKP RSA key raises an error
def test_to_jwk_invalid_key_raises():
    rsa_key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
    alg = OKPAlgorithm()
    with pytest.raises(Exception):
        alg.to_jwk(rsa_key)
