import json
import base64
import pytest
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
from repositorios.pyjwt.jwt.algorithms import ECAlgorithm

def _b64url_to_int(s: str) -> int:
    padding = '=' * ((4 - len(s) % 4) % 4)
    return int.from_bytes(base64.urlsafe_b64decode(s + padding), 'big')

# curto - happy path: P-256 (SECP256R1) retorna kty/crv/x/y corretos e coerentes
def test_to_jwk_happy_path_secp256r1():
    private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
    public_key = private_key.public_key()
    jwk_json = ECAlgorithm.to_jwk(public_key)
    jwk = json.loads(jwk_json)

    assert jwk.get("kty") == "EC"
    assert jwk.get("crv") == "P-256"
    x = _b64url_to_int(jwk["x"])
    y = _b64url_to_int(jwk["y"])
    nums = private_key.private_numbers().public_numbers
    assert x == nums.x
    assert y == nums.y

# curto - happy path: secp256k1 (SECP256K1) retorna kty/crv/x/y corretos e coerentes
def test_to_jwk_happy_path_secp256k1():
    private_key = ec.generate_private_key(ec.SECP256K1(), default_backend())
    public_key = private_key.public_key()
    jwk_json = ECAlgorithm.to_jwk(public_key)
    jwk = json.loads(jwk_json)

    assert jwk.get("kty") == "EC"
    assert jwk.get("crv") == "secp256k1"
    x = _b64url_to_int(jwk["x"])
    y = _b64url_to_int(jwk["y"])
    nums = private_key.private_numbers().public_numbers
    assert x == nums.x
    assert y == nums.y

# curto - exceção/lista de erro: chave inválida levanta exceção esperada
def test_to_jwk_invalid_key_raises():
    with pytest.raises(Exception):
        ECAlgorithm.to_jwk("not-a-key")
