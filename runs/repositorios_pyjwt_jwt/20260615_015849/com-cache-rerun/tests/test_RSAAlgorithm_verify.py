import pytest
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature
from repositorios.pyjwt.jwt.algorithms import RSAAlgorithm

def test_rsa_verify_happy_path():
    class FakeRSAPublicKey:
        def __init__(self):
            self.called = False
            self.received = None

        def verify(self, sig, msg, pad, hash_alg):
            self.called = True
            self.received = (sig, msg, pad, hash_alg)

    algo = RSAAlgorithm(hashes.SHA256)  # pass class to allow RSAAlgorithm.verify to instantiate
    key = FakeRSAPublicKey()
    msg = b"message"
    sig = b"signature"

    result = algo.verify(msg, key, sig)

    assert result is True
    assert key.called is True
    assert key.received[0] == sig
    assert key.received[1] == msg
    assert isinstance(key.received[2], padding.PKCS1v15)
    assert isinstance(key.received[3], hashes.SHA256)

def test_rsa_verify_invalid_signature():
    class FakeRSAPublicKeyRaises:
        def verify(self, sig, msg, pad, hash_alg):
            raise InvalidSignature

    algo = RSAAlgorithm(hashes.SHA256)
    key = FakeRSAPublicKeyRaises()
    msg = b"message"
    sig = b"signature"

    result = algo.verify(msg, key, sig)

    assert result is False
