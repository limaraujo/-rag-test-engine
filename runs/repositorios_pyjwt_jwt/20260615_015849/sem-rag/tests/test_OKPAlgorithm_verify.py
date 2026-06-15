import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from repositorios.pyjwt.jwt.algorithms import OKPAlgorithm

# curto: happy path using a public key provided as the key argument
def test_okp_verify_with_public_key_happy_path():
    alg = OKPAlgorithm()
    msg = "hello"
    private_key = Ed25519PrivateKey.generate()
    signature = private_key.sign(msg.encode("utf-8"))
    public_key = private_key.public_key()
    assert alg.verify(msg, public_key, signature) is True

# curto: happy path using a private key provided as the key argument
def test_okp_verify_with_private_key_happy_path():
    alg = OKPAlgorithm()
    msg = "hello"
    private_key = Ed25519PrivateKey.generate()
    signature = private_key.sign(msg.encode("utf-8"))
    assert alg.verify(msg, private_key, signature) is True

# curto: invalid signature should result in False
def test_okp_verify_invalid_signature_returns_false():
    alg = OKPAlgorithm()
    private_key = Ed25519PrivateKey.generate()
    msg = "danger"
    signature = private_key.sign(msg.encode("utf-8"))
    # tamper the signature
    tampered = bytearray(signature)
    tampered[-1] = (tampered[-1] + 1) % 256
    tampered_signature = bytes(tampered)
    public_key = private_key.public_key()
    assert alg.verify(msg, public_key, tampered_signature) is False
