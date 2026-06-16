from cryptography.hazmat.primitives.asymmetric import padding
import pytest
from repositorios.pyjwt.jwt.algorithms import RSAAlgorithm

class DummyKey:
    def __init__(self):
        self.calls = []
    def sign(self, msg, pkcs1v15_padding, algorithm):
        self.calls.append((msg, pkcs1v15_padding, algorithm))
        return b"signature"

class FailKey:
    def sign(self, msg, pkcs1v15_padding, algorithm):
        raise ValueError("boom")

# short: happy path - forwarder uses PKCS1v15 padding and hash_alg() result, returns signature
def test_sign_forwards_arguments_and_returns_signature():
    alg = object.__new__(RSAAlgorithm)
    alg.hash_alg = lambda: "HASH"
    key = DummyKey()
    result = alg.sign(b"hello", key)
    assert result == b"signature"
    assert len(key.calls) == 1
    msg, pad, algo = key.calls[0]
    assert msg == b"hello"
    assert isinstance(pad, padding.PKCS1v15)
    assert algo == "HASH"

# short: exception propagation - key.sign raises error, sign should propagate
def test_sign_propagates_exceptions_from_key():
    alg = object.__new__(RSAAlgorithm)
    alg.hash_alg = lambda: "HASH"
    key = FailKey()
    with pytest.raises(ValueError, match="boom"):
        alg.sign(b"msg", key)
