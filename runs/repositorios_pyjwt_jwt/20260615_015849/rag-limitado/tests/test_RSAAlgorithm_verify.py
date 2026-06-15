from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature
from repositorios.pyjwt.jwt.algorithms import RSAAlgorithm

class FakeRSAPublicKey:
    def __init__(self, should_raise: bool):
        self.should_raise = should_raise
        self.calls = []

    def verify(self, sig, msg, pad, hash_alg):
        self.calls.append((sig, msg, pad, hash_alg))
        if self.should_raise:
            raise InvalidSignature()
        return None

def _make_algo():
    algo = object.__new__(RSAAlgorithm)
    algo.hash_alg = lambda: "HASH"
    return algo

# short: happy path - returns True when no InvalidSignature is raised
def test_verify_happy_path():
    algo = _make_algo()
    key = FakeRSAPublicKey(should_raise=False)
    msg = b"hello"
    sig = b"signature"

    assert algo.verify(msg, key, sig) is True
    sig_arg, msg_arg, pad_arg, hash_alg_arg = key.calls[0]
    assert msg_arg == msg
    assert sig_arg == sig
    assert pad_arg.__class__.__name__ == "PKCS1v15"
    assert hash_alg_arg == "HASH"

# short: invalid signature path - returns False when InvalidSignature is raised
def test_verify_invalid_signature_returns_false():
    algo = _make_algo()
    key = FakeRSAPublicKey(should_raise=True)
    msg = b"hello"
    sig = b"signature"

    assert algo.verify(msg, key, sig) is False
    sig_arg, msg_arg, pad_arg, hash_alg_arg = key.calls[0]
    assert msg_arg == msg
    assert sig_arg == sig
    assert pad_arg.__class__.__name__ == "PKCS1v15"
    assert hash_alg_arg == "HASH"
