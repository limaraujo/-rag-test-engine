import json
import base64
import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat, PrivateFormat, NoEncryption
from repositorios.pyjwt.jwt.exceptions import InvalidKeyError
from repositorios.pyjwt.jwt.algorithms import OKPAlgorithm

import json
import base64
import pytest

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat, PrivateFormat, NoEncryption
from repositorios.pyjwt.jwt.exceptions import InvalidKeyError
from repositorios.pyjwt.jwt.algorithms import OKPAlgorithm

def b64u(b: bytes) -> str:
    return base64.urlsafe_b64encode(b).decode("ascii").rstrip("=")

# happy path: string input returns Ed25519PublicKey
def test_from_jwk_string_public_okp_ed25519():
    priv = Ed25519PrivateKey.generate()
    pub = priv.public_key()
    pub_bytes = pub.public_bytes(Encoding.Raw, PublicFormat.Raw)
    jwk = {"kty": "OKP", "crv": "Ed25519", "x": b64u(pub_bytes)}
    jwk_json = json.dumps(jwk)
    key = OKPAlgorithm.from_jwk(jwk_json)
    assert isinstance(key, Ed25519PublicKey)

# happy path: dict input with d returns Ed25519PrivateKey
def test_from_jwk_dict_private_okp_ed25519():
    priv = Ed25519PrivateKey.generate()
    d_bytes = priv.private_bytes(Encoding.Raw, PrivateFormat.Raw, NoEncryption())
    pub = priv.public_key()
    pub_bytes = pub.public_bytes(Encoding.Raw, PublicFormat.Raw)
    jwk = {"kty": "OKP", "crv": "Ed25519", "x": b64u(pub_bytes), "d": b64u(d_bytes)}
    key = OKPAlgorithm.from_jwk(jwk)
    assert isinstance(key, Ed25519PrivateKey)

# error: invalid kty raises
def test_from_jwk_invalid_kty_raises():
    priv = Ed25519PrivateKey.generate()
    pub = priv.public_key()
    pub_bytes = pub.public_bytes(Encoding.Raw, PublicFormat.Raw)
    jwk = {"kty": "RSA", "crv": "Ed25519", "x": b64u(pub_bytes)}
    with pytest.raises(InvalidKeyError):
        OKPAlgorithm.from_jwk(jwk)

# error: invalid curve raises
def test_from_jwk_invalid_curve_raises():
    priv = Ed25519PrivateKey.generate()
    pub = priv.public_key()
    pub_bytes = pub.public_bytes(Encoding.Raw, PublicFormat.Raw)
    jwk = {"kty": "OKP", "crv": "UnknownCurve", "x": b64u(pub_bytes)}
    with pytest.raises(InvalidKeyError):
        OKPAlgorithm.from_jwk(jwk)
