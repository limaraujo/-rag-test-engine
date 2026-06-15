from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from repositorios.pyjwt.jwt.algorithms import OKPAlgorithm

# happy path: verify with private key, msg as str, sig as bytes
def test_okp_verify_happy_path_with_private_key():
    private_key = Ed25519PrivateKey.generate()
    msg = "hello world"
    sig = private_key.sign(msg.encode("utf-8"))
    algo = OKPAlgorithm()
    assert algo.verify(msg, private_key, sig) is True

# invalid signature should return False (wrong msg for given sig)
def test_okp_verify_invalid_signature_returns_false():
    private_key = Ed25519PrivateKey.generate()
    sig = private_key.sign(b"original message")
    wrong_msg = "different message"
    algo = OKPAlgorithm()
    assert algo.verify(wrong_msg, private_key, sig) is False

# verify using public key input (branch where key is not private) should succeed
def test_okp_verify_with_public_key_input():
    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()
    msg = "verify with public key"
    sig = private_key.sign(msg.encode("utf-8"))
    algo = OKPAlgorithm()
    assert algo.verify(msg, public_key, sig) is True

# bytes inputs: msg and sig provided as bytes
def test_okp_verify_bytes_inputs():
    private_key = Ed25519PrivateKey.generate()
    msg_bytes = b"binary data"
    sig_bytes = private_key.sign(msg_bytes)
    algo = OKPAlgorithm()
    assert algo.verify(msg_bytes, private_key, sig_bytes) is True
