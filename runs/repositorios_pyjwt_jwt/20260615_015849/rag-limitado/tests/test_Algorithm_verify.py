from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from repositorios.pyjwt.jwt.algorithms import Algorithm

class Ed25519Algorithm(Algorithm):
    def from_jwk(self, jwk):
        raise NotImplementedError

    def prepare_key(self, key):
        return key

    def sign(self, msg, key):
        raise NotImplementedError

    def to_jwk(self, key):
        raise NotImplementedError

    def verify(self, msg: bytes, key, sig: bytes) -> bool:
        try:
            key.verify(sig, msg)
            return True
        except Exception:
            return False

def test_verify_valid_signature_happy_path():
    msg = b"hello world"
    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()
    sig = private_key.sign(msg)
    alg = Ed25519Algorithm()
    assert alg.verify(msg, public_key, sig) is True

def test_verify_invalid_signature_returns_false():
    msg = b"hello world"
    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()
    sig = private_key.sign(msg)
    tampered = bytearray(sig)
    tampered[-1] ^= 0x01
    tampered = bytes(tampered)
    alg = Ed25519Algorithm()
    assert alg.verify(msg, public_key, tampered) is False
