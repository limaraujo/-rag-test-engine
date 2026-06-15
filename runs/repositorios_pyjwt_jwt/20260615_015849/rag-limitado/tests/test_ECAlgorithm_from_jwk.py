from repositorios.pyjwt.jwt.exceptions import InvalidKeyError
import base64
import json
import pytest
from cryptography.hazmat.primitives.asymmetric.ec import EllipticCurvePublicKey
from cryptography.hazmat.primitives.asymmetric import ec
from repositorios.pyjwt.jwt.algorithms import ECAlgorithm

def b64url(b: bytes) -> str:
    return base64.urlsafe_b64encode(b).rstrip(b'=').decode('ascii')

# happy path: public key path (no private key d)
# Test that a valid EC JWK without "d" yields a public key
def test_from_jwk_public_key_happy_path():
    private_key = ec.generate_private_key(ec.SECP256R1())
    public_numbers = private_key.public_key().public_numbers()
    x = public_numbers.x.to_bytes(32, 'big')
    y = public_numbers.y.to_bytes(32, 'big')
    jwk = {
        "kty": "EC",
        "crv": "P-256",
        "x": b64url(x),
        "y": b64url(y),
    }
    key = ECAlgorithm.from_jwk(jwk)
    assert isinstance(key, EllipticCurvePublicKey)

# edge case: presence of "d" with mismatched length should raise
# Test that providing an incorrect length for "d" results in InvalidKeyError
def test_from_jwk_with_d_length_mismatch_raises():
    x = b'\x01' * 32
    y = b'\x02' * 32
    d = b'\x03' * 16  # incorrect length (not equal to x/y length)
    jwk = {
        "kty": "EC",
        "crv": "P-256",
        "x": b64url(x),
        "y": b64url(y),
        "d": b64url(d),
    }
    with pytest.raises(InvalidKeyError):
        ECAlgorithm.from_jwk(jwk)

# invalid key type: should raise InvalidKeyError
def test_from_jwk_invalid_kty_raises():
    x = b'\x00' * 32
    y = b'\x00' * 32
    jwk = {
        "kty": "RSA",
        "crv": "P-256",
        "x": b64url(x),
        "y": b64url(y),
    }
    with pytest.raises(InvalidKeyError, match="Not an Elliptic curve key"):
        ECAlgorithm.from_jwk(jwk)

# edge case: coords length mismatch without d
# Test that providing x/y lengths different from the curve requirement triggers error
def test_from_jwk_coords_length_mismatch_raises():
    x = b'\x01' * 31
    y = b'\x02' * 31
    jwk = {
        "kty": "EC",
        "crv": "P-256",
        "x": b64url(x),
        "y": b64url(y),
    }
    with pytest.raises(InvalidKeyError, match="Coords should be 32 bytes for curve P-256"):
        ECAlgorithm.from_jwk(jwk)
