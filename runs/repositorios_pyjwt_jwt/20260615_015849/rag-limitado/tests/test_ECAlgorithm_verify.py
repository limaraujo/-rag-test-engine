import types
from unittest.mock import patch
from cryptography.exceptions import InvalidSignature
from repositorios.pyjwt.jwt.algorithms import ECAlgorithm
from cryptography.hazmat.primitives import hashes

import types
from unittest.mock import patch
from cryptography.exceptions import InvalidSignature
from repositorios.pyjwt.jwt.algorithms import ECAlgorithm


# Helper to build an ECAlgorithm-like instance without invoking __init__
def _make_algo():
    alg = ECAlgorithm.__new__(ECAlgorithm)
    def _hash_alg(self):
        from cryptography.hazmat.primitives import hashes
        return hashes.SHA256()
    alg.hash_alg = types.MethodType(_hash_alg, alg)
    return alg

# happy path: valid input and signature verification succeeds
# happy path
def test_verify_happy_path():
    alg = _make_algo()
    class DummyKey:
        curve = "curve"
        def __init__(self):
            self.called = False
        def verify(self, der_sig, msg, signature_algorithm):
            self.called = True
    key = DummyKey()
    with patch("repositorios.pyjwt.jwt.algorithms.raw_to_der_signature", return_value=b"DER"):
        result = alg.verify(b"message", key, b"sig")
    assert result is True
    assert key.called

# edge case: raw_to_der_signature raises ValueError -> False
# invalid input
def test_verify_value_error_returns_false():
    alg = _make_algo()
    class DummyKey:
        curve = "curve"
        def verify(self, der_sig, msg, signature_algorithm):
            pass
    key = DummyKey()
    with patch("repositorios.pyjwt.jwt.algorithms.raw_to_der_signature", side_effect=ValueError()):
        result = alg.verify(b"message", key, b"sig")
    assert result is False

# edge case: public key verification raises InvalidSignature -> False
# invalid signature
def test_verify_invalid_signature_returns_false():
    alg = _make_algo()
    class DummyKey:
        curve = "curve"
        def verify(self, der_sig, msg, signature_algorithm):
            raise InvalidSignature()
    key = DummyKey()
    with patch("repositorios.pyjwt.jwt.algorithms.raw_to_der_signature", return_value=b"DER"):
        result = alg.verify(b"message", key, b"sig")
    assert result is False
