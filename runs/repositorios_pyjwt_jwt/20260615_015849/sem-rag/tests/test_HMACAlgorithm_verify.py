import pytest
from repositorios.pyjwt.jwt.algorithms import HMACAlgorithm


# Verifica path feliz: sig igual ao resultado de sign(msg, key) -> True
def test_verify_happy_path_matches_sign():
    class FakeSelf:
        def __init__(self, value):
            self._value = value
        def sign(self, msg, key):
            return self._value
    fake = FakeSelf(b"expected_signature")
    assert HMACAlgorithm.verify(fake, b"message", b"key", b"expected_signature")

# Verifica falha de correspondência: sig diferente -> False
def test_verify_false_when_signature_differs():
    class FakeSelf:
        def __init__(self, value):
            self._value = value
        def sign(self, msg, key):
            return self._value
    fake = FakeSelf(b"generated_signature")
    assert not HMACAlgorithm.verify(fake, b"message", b"key", b"different_signature")

# Verifica exceção para sig não bytes: TypeError esperada
def test_verify_raises_type_error_for_non_bytes_sig():
    class FakeSelf:
        def __init__(self, value):
            self._value = value
        def sign(self, msg, key):
            return self._value
    fake = FakeSelf(b"generated_signature")
    with pytest.raises(TypeError):
        HMACAlgorithm.verify(fake, b"message", b"key", 123)
