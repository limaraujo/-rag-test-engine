import base64
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat, PrivateFormat, NoEncryption
from repositorios.pyjwt.jwt.algorithms import OKPAlgorithm

import base64

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat, PrivateFormat, NoEncryption
from repositorios.pyjwt.jwt.algorithms import OKPAlgorithm



def _base64url_decode(data: str) -> bytes:
    padding = '=' * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


# curto: happy path - Ed25519 public key to_jwk returns OKP JWK with x, kty, crv
def test_okp_to_jwk_ed25519_public_key_happy_path():
    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()

    jwk = OKPAlgorithm.to_jwk(public_key, True)

    assert isinstance(jwk, dict)
    assert jwk.get("kty") == "OKP"
    assert jwk.get("crv") == "Ed25519"
    assert "x" in jwk

    x_decoded = _base64url_decode(jwk["x"])
    public_bytes = public_key.public_bytes(Encoding.Raw, PublicFormat.Raw)
    assert x_decoded == public_bytes


# curto: private key - to_jwk includes d and x, with d matching private key and x matching public key
def test_okp_to_jwk_ed25519_private_key_includes_d_and_x():
    private_key = Ed25519PrivateKey.generate()

    jwk = OKPAlgorithm.to_jwk(private_key, True)

    assert "d" in jwk
    d_decoded = _base64url_decode(jwk["d"])
    private_bytes = private_key.private_bytes(Encoding.Raw, PrivateFormat.Raw, NoEncryption())
    assert d_decoded == private_bytes

    assert "x" in jwk
    x_decoded = _base64url_decode(jwk["x"])
    public_bytes = private_key.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)
    assert x_decoded == public_bytes
