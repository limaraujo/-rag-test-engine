from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from repositorios.pyjwt.jwt.algorithms import OKPAlgorithm

# happy path: private key provided, message as str
def test_okp_verify_with_private_key_and_str_message():
    alg = OKPAlgorithm()
    msg = "hello"
    private_key = Ed25519PrivateKey.generate()
    sig = private_key.sign(msg.encode("utf-8"))
    assert alg.verify(msg, private_key, sig) is True

# happy path: public key provided, message as bytes
def test_okp_verify_with_public_key_and_bytes_message():
    alg = OKPAlgorithm()
    msg = b"hello bytes"
    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()
    sig = private_key.sign(msg)
    assert alg.verify(msg, public_key, sig) is True

# negative: invalid signature should return False
def test_okp_verify_invalid_signature_returns_false():
    alg = OKPAlgorithm()
    msg = "tamper"
    private_key = Ed25519PrivateKey.generate()
    sig = private_key.sign(msg.encode("utf-8"))
    bad_sig = bytearray(sig)
    bad_sig[-1] ^= 0x01
    bad_sig = bytes(bad_sig)
    assert alg.verify(msg, private_key, bad_sig) is False
