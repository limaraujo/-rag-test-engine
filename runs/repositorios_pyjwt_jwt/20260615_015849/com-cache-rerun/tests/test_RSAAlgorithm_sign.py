import pytest
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from repositorios.pyjwt.jwt.algorithms import RSAAlgorithm

class TestableRSAAlgorithm(RSAAlgorithm):
    def __init__(self, hash_alg_instance):
        self._hash_alg = hash_alg_instance

    def hash_alg(self):
        return self._hash_alg

# Verifica o caminho feliz: PKCS1v15 padding, hash SHA correta e retorno da assinatura
@pytest.mark.parametrize("hash_inst", [hashes.SHA256(), hashes.SHA384()])
def test_sign_uses_expected_padding_and_hash_and_returns_signature(hash_inst):
    class DummyRSAPrivateKey:
        def __init__(self):
            self.captured = None

        def sign(self, msg, pad, alg):
            self.captured = (msg, pad, alg)
            return b"signature-by-key"

    key = DummyRSAPrivateKey()
    algo = TestableRSAAlgorithm(hash_inst)
    msg = b"hello"

    sig = algo.sign(msg, key)

    assert sig == b"signature-by-key"
    captured_msg, captured_pad, captured_alg = key.captured
    assert captured_msg == msg
    assert isinstance(captured_pad, padding.PKCS1v15)
    assert captured_alg is hash_inst  # mesma instância passada

# Verifica propagação de exceção lançada pelo key.sign
def test_sign_propagates_exception_from_key_sign():
    class DummyRSAPrivateKeyRaise:
        def sign(self, msg, pad, alg):
            raise RuntimeError("boom")

    key = DummyRSAPrivateKeyRaise()
    algo = TestableRSAAlgorithm(hashes.SHA256())
    with pytest.raises(RuntimeError):
        algo.sign(b"data", key)
