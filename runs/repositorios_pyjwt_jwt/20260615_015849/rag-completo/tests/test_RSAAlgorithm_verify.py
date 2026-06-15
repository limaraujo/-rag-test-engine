import pytest
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric import padding
from repositorios.pyjwt.jwt.algorithms import RSAAlgorithm

# short: happy path - key.verify does not raise InvalidSignature
def test_rsa_verify_happy_path():
    class TestableRSAAlgorithm(RSAAlgorithm):
        def __init__(self):
            pass
        def hash_alg(self):
            return None

    class DummyKey:
        def __init__(self, should_raise=False):
            self.should_raise = should_raise
            self.last_call = None
        def verify(self, sig, msg, padding_used, hash_alg):
            self.last_call = {
                "sig": sig,
                "msg": msg,
                "padding_used": padding_used,
                "hash_alg": hash_alg,
            }
            if self.should_raise:
                raise InvalidSignature()

    algo = TestableRSAAlgorithm()
    key = DummyKey(should_raise=False)
    assert algo.verify(msg=b"hello", key=key, sig=b"signature") is True
    assert isinstance(key.last_call["padding_used"], padding.PKCS1v15)

# short: branch coverage - when key.verify raises InvalidSignature, RSAAlgorithm.verify returns False
def test_rsa_verify_invalid_signature():
    class TestableRSAAlgorithm(RSAAlgorithm):
        def __init__(self):
            pass
        def hash_alg(self):
            return None

    class DummyKey:
        def __init__(self, should_raise=False):
            self.should_raise = should_raise
            self.last_call = None
        def verify(self, sig, msg, padding_used, hash_alg):
            self.last_call = {
                "sig": sig,
                "msg": msg,
                "padding_used": padding_used,
                "hash_alg": hash_alg,
            }
            if self.should_raise:
                raise InvalidSignature()

    algo = TestableRSAAlgorithm()
    key = DummyKey(should_raise=True)
    assert algo.verify(msg=b"hello", key=key, sig=b"signature") is False
    assert isinstance(key.last_call["padding_used"], padding.PKCS1v15)
