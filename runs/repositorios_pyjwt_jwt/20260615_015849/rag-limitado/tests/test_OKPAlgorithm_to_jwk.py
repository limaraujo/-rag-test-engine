import json
import base64
import pytest
from repositorios.pyjwt.jwt.exceptions import InvalidKeyError
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from repositorios.pyjwt.jwt.algorithms import OKPAlgorithm
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, generate_private_key

import json
import base64
import pytest

from repositorios.pyjwt.jwt.exceptions import InvalidKeyError

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from repositorios.pyjwt.jwt.algorithms import OKPAlgorithm


# Curto: happy path - chave pública Ed25519, retorno como dict
def test_to_jwk_public_ed25519_dict():
    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()

    jwk = OKPAlgorithm.to_jwk(public_key, as_dict=True)

    assert isinstance(jwk, dict)
    assert jwk.get("kty") == "OKP"
    assert jwk.get("crv") == "Ed25519"
    assert "x" in jwk and isinstance(jwk["x"], str) and jwk["x"]

    # decode para verificar tamanho (Ed25519 usa 32 bytes)
    def b64url_decode(s: str) -> bytes:
        padding = '=' * (-len(s) % 4)
        return base64.urlsafe_b64decode(s + padding)

    x_bytes = b64url_decode(jwk["x"])
    assert len(x_bytes) == 32


# Curto: happy path - chave pública Ed25519, retorno como JSON string
def test_to_jwk_public_ed25519_json():
    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()

    jwk_json = OKPAlgorithm.to_jwk(public_key, as_dict=False)

    assert isinstance(jwk_json, str)
    data = json.loads(jwk_json)
    assert data.get("kty") == "OKP"
    assert data.get("crv") == "Ed25519"
    assert "x" in data and isinstance(data["x"], str) and data["x"]


# Curto: happy path - chave privada Ed25519, retorno como dict
def test_to_jwk_private_ed25519_dict():
    private_key = Ed25519PrivateKey.generate()

    jwk = OKPAlgorithm.to_jwk(private_key, as_dict=True)

    assert isinstance(jwk, dict)
    assert jwk.get("kty") == "OKP"
    assert jwk.get("crv") == "Ed25519"
    assert "x" in jwk and isinstance(jwk["x"], str) and jwk["x"]
    assert "d" in jwk and isinstance(jwk["d"], str) and jwk["d"]

    # decode para verificar tamanho
    def b64url_decode(s: str) -> bytes:
        padding = '=' * (-len(s) % 4)
        return base64.urlsafe_b64decode(s + padding)

    x_bytes = b64url_decode(jwk["x"])
    d_bytes = b64url_decode(jwk["d"])
    assert len(x_bytes) == 32
    assert len(d_bytes) == 32


# Curto: exceção esperada - chave RSA não suportada pelo OKP
def test_to_jwk_invalid_key_raises():
    from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, generate_private_key

    rsa_private = generate_private_key(public_exponent=65537, key_size=2048)
    rsa_public = rsa_private.public_key()

    with pytest.raises(InvalidKeyError):
        OKPAlgorithm.to_jwk(rsa_public, as_dict=True)
