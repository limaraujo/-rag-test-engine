import base64
import json
import pytest
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat, PrivateFormat, NoEncryption
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from repositorios.pyjwt.jwt.exceptions import InvalidKeyError
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from repositorios.pyjwt.jwt.algorithms import OKPAlgorithm

import base64
import json
import pytest
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat, PrivateFormat, NoEncryption
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from repositorios.pyjwt.jwt.exceptions import InvalidKeyError
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from repositorios.pyjwt.jwt.algorithms import OKPAlgorithm


# helper
def b64u(b: bytes) -> str:
    return base64.urlsafe_b64encode(b).decode("ascii").rstrip("=")


# Test public Ed25519 key to_jwk with as_dict=True
# happy path: public key -> dict with x, kty, crv
def test_to_jwk_public_ed25519_dict():
    priv = Ed25519PrivateKey.generate()
    pub = priv.public_key()
    jwk = OKPAlgorithm.to_jwk(pub, as_dict=True)

    assert isinstance(jwk, dict)
    assert jwk["kty"] == "OKP"
    assert jwk["crv"] == "Ed25519"

    pub_bytes = pub.public_bytes(Encoding.Raw, PublicFormat.Raw)
    assert jwk["x"] == b64u(pub_bytes)


# Test public Ed25519 key to_jwk with as_dict=False (JSON string)
# happy path: public key -> json string with correct fields
def test_to_jwk_public_ed25519_json():
    priv = Ed25519PrivateKey.generate()
    pub = priv.public_key()
    jwk_json = OKPAlgorithm.to_jwk(pub, as_dict=False)
    jwk = json.loads(jwk_json)

    assert isinstance(jwk, dict)
    assert jwk["kty"] == "OKP"
    assert jwk["crv"] == "Ed25519"

    pub_bytes = pub.public_bytes(Encoding.Raw, PublicFormat.Raw)
    assert jwk["x"] == b64u(pub_bytes)


# Test private Ed25519 key to_jwk with as_dict=True
# branch for private key: includes d and x
def test_to_jwk_private_ed25519_dict():
    priv = Ed25519PrivateKey.generate()
    pub = priv.public_key()

    jwk = OKPAlgorithm.to_jwk(priv, as_dict=True)

    assert isinstance(jwk, dict)
    assert jwk["kty"] == "OKP"
    assert jwk["crv"] == "Ed25519"

    # check x
    pub_bytes = pub.public_bytes(Encoding.Raw, PublicFormat.Raw)
    assert jwk["x"] == b64u(pub_bytes)

    # check d
    priv_bytes = priv.private_bytes(Encoding.Raw, PrivateFormat.Raw, NoEncryption())
    assert jwk["d"] == b64u(priv_bytes)


# Test invalid key input raises InvalidKeyError
# edge case: object not a key should raise
def test_to_jwk_invalid_key_raises():
    class NotAKey:
        pass

    with pytest.raises(InvalidKeyError):
        OKPAlgorithm.to_jwk(NotAKey(), as_dict=True)
