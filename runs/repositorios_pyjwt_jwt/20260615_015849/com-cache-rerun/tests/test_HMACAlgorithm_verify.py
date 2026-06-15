import pytest
from repositorios.pyjwt.jwt.algorithms import HMACAlgorithm

# Define uma subclass que substitui sign para controle determinístico
class DummyHMAC(HMACAlgorithm):
    def __init__(self):
        pass

    def sign(self, msg: bytes, key: bytes) -> bytes:
        return b"sig"

# curto: happy path - assinatura corresponde ao resultado de sign
def test_verify_happy_path():
    h = DummyHMAC()
    assert h.verify(b"hello", b"secret", b"sig")

# curto: falha de verificação - assinatura não corresponde ao resultado de sign
def test_verify_signature_mismatch():
    h = DummyHMAC()
    assert not h.verify(b"hello", b"secret", b"notsig")
