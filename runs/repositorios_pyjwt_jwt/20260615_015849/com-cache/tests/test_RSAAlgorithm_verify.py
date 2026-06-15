import pytest
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from repositorios.pyjwt.jwt.algorithms import RSAAlgorithm

class DummyRSAPublicKey:
    def __init__(self, behavior="ok"):
        self.behavior = behavior
        self.called = False

    def verify(self, sig, msg, padding_alg, hash_alg):
        self.called = True
        if self.behavior == "ok":
            return
        if self.behavior == "invalid":
            raise InvalidSignature()
        if self.behavior == "other":
            raise ValueError("boom")


# Test 1: happy path - assinatura válida não levanta exceção, retorna True
def test_verify_happy_path():
    rsa_alg = RSAAlgorithm(hash_alg=lambda: hashes.SHA256())
    key = DummyRSAPublicKey("ok")
    assert rsa_alg.verify(b"msg", key, b"sig") is True


# Test 2: assinatura inválida - InvalidSignature é capturada e resulta em False
def test_verify_invalid_signature():
    rsa_alg = RSAAlgorithm(hash_alg=lambda: hashes.SHA256())
    key = DummyRSAPublicKey("invalid")
    assert rsa_alg.verify(b"msg", key, b"sig") is False


# Test 3: exceção diferente de InvalidSignature deve propagarse
def test_verify_propagates_other_exception():
    rsa_alg = RSAAlgorithm(hash_alg=lambda: hashes.SHA256())
    key = DummyRSAPublicKey("other")
    with pytest.raises(ValueError):
        rsa_alg.verify(b"msg", key, b"sig")
