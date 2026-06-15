import json
import base64
import pytest
from repositorios.pyjwt.jwt.exceptions import InvalidKeyError
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey, Ed25519PrivateKey
from repositorios.pyjwt.jwt.algorithms import OKPAlgorithm

import json
import base64
import pytest

from repositorios.pyjwt.jwt.exceptions import InvalidKeyError
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey, Ed25519PrivateKey
from repositorios.pyjwt.jwt.algorithms import OKPAlgorithm

def _b64url(b: bytes) -> str:
    return base64.urlsafe_b64encode(b).decode("ascii").rstrip("=")

# Verifica: caminho feliz para Ed25519 PublicKey sem parâmetro d
def test_from_jwk_okp_ed25519_public_happy_path():
    x = bytes([1] * 32)
    jwk = json.dumps({"kty": "OKP", "crv": "Ed25519", "x": _b64url(x)})
    key = OKPAlgorithm.from_jwk(jwk)
    assert isinstance(key, Ed25519PublicKey)

# Verifica: caminho com d presente resulta em Ed25519PrivateKey
def test_from_jwk_okp_ed25519_private_with_d():
    d = bytes([2] * 32)
    x = bytes([3] * 32)
    jwk = json.dumps({
        "kty": "OKP",
        "crv": "Ed25519",
        "x": _b64url(x),
        "d": _b64url(d)
    })
    key = OKPAlgorithm.from_jwk(jwk)
    assert isinstance(key, Ed25519PrivateKey)

# Verifica: kty inválido levanta InvalidKeyError
def test_from_jwk_invalid_kty_raises():
    jwk = json.dumps({"kty": "RSA", "crv": "Ed25519", "x": _b64url(bytes([1]*32))})
    with pytest.raises(InvalidKeyError):
        OKPAlgorithm.from_jwk(jwk)

# Verifica: ausência de x levanta InvalidKeyError com mensagem esperada
def test_from_jwk_missing_x_param_raises():
    jwk = json.dumps({"kty": "OKP", "crv": "Ed25519"})
    with pytest.raises(InvalidKeyError) as exc:
        OKPAlgorithm.from_jwk(jwk)
    assert 'OKP should have "x" parameter' in str(exc.value)
