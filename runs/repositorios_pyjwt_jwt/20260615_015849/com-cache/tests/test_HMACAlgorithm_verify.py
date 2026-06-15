import pytest
from repositorios.pyjwt.jwt.algorithms import HMACAlgorithm

class _TestHMAC(HMACAlgorithm):
    def __init__(self):
        pass

    def sign(self, msg: bytes, key: bytes) -> bytes:
        return b"the_signature"

# curto: verifica que verify retorna True quando sig == sign(msg, key)
def test_verify_returns_true_when_signature_matches():
    algo = _TestHMAC()
    msg = b"hello world"
    key = b"secret"
    sig = b"the_signature"
    assert algo.verify(msg, key, sig) is True

# curto: verifica que verify retorna False quando sig difere de sign(msg, key)
def test_verify_returns_false_when_signature_mismatched():
    algo = _TestHMAC()
    msg = b"hello world"
    key = b"secret"
    sig = b"different_signature"
    assert algo.verify(msg, key, sig) is False
