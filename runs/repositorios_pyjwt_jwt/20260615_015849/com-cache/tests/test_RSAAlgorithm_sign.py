from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature
import pytest
from repositorios.pyjwt.jwt.algorithms import RSAAlgorithm

# test 1: happy path - verify PKCS1v15 padding and hash_alg are passed to key.sign
@pytest.mark.parametrize("msg", [b"hello", b"world"])
# verifica chamada com PKCS1v15 e hash_alg correto (happy path)
def test_rsa_sign_calls_key_with_pkcs1v15_and_hash_alg(msg):
    class DummyKey:
        def __init__(self):
            self.called_with_msg = None
            self.called_with_pad = None
            self.called_with_hash_alg = None

        def sign(self, msg_in, pad, hash_alg):
            self.called_with_msg = msg_in
            self.called_with_pad = pad
            self.called_with_hash_alg = hash_alg
            return b"signature"

    algo = RSAAlgorithm.__new__(RSAAlgorithm)
    algo.hash_alg = lambda: "HASHALG"
    key = DummyKey()
    result = algo.sign(msg, key)
    assert result == b"signature"
    assert key.called_with_msg == msg
    assert isinstance(key.called_with_pad, padding.PKCS1v15)
    assert key.called_with_hash_alg == "HASHALG"

# test 2: ensure exceptions from key.sign propagate (ValueError)
def test_rsa_sign_propagates_exception_from_key_sign():
    algo = RSAAlgorithm.__new__(RSAAlgorithm)
    algo.hash_alg = lambda: "HASHALG"

    class FailingKey:
        def sign(self, msg, pad, hash_alg):
            raise ValueError("boom")

    with pytest.raises(ValueError, match="boom"):
        algo.sign(b"msg", FailingKey())

# test 3: ensure cryptography InvalidSignature propagates through sign
def test_rsa_sign_propagates_InvalidSignature():
    algo = RSAAlgorithm.__new__(RSAAlgorithm)
    algo.hash_alg = lambda: "HASHALG"

    class KeyRaisesInvalidSignature:
        def sign(self, msg, pad, hash_alg):
            raise InvalidSignature()

    with pytest.raises(InvalidSignature):
        algo.sign(b"msg", KeyRaisesInvalidSignature())
