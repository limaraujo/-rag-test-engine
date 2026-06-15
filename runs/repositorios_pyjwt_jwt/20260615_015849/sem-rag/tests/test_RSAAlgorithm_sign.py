import pytest
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from repositorios.pyjwt.jwt.algorithms import RSAAlgorithm

# curto: happy path - verifica que key.sign é chamado com PKCS1v15 e hash vindo do hash_alg
def test_sign_happy_path_calls_key_with_expected_params():
    hash_sentinel = object()

    rsa_alg = object.__new__(RSAAlgorithm)
    rsa_alg.hash_alg = lambda: hash_sentinel

    class DummyRSAPrivateKey:
        def __init__(self):
            self.captured = None

        def sign(self, msg, padding_inst, hash_alg):
            self.captured = {
                "msg": msg,
                "padding": padding_inst,
                "hash_alg": hash_alg,
            }
            return b"signature-by-key"

    key = DummyRSAPrivateKey()
    sig = rsa_alg.sign(b"hello", key)

    assert key.captured is not None
    assert key.captured["msg"] == b"hello"
    assert isinstance(key.captured["padding"], asym_padding.PKCS1v15)
    assert key.captured["hash_alg"] is hash_sentinel
    assert sig == b"signature-by-key"

# curto: exceção propagada - verifica que ValueError lançado por key.sign não é silenciado
def test_sign_propagates_exception_from_key():
    rsa_alg = object.__new__(RSAAlgorithm)
    rsa_alg.hash_alg = lambda: object()

    class FailingKey:
        def sign(self, *args, **kwargs):
            raise ValueError("boom")

    with pytest.raises(ValueError, match="boom"):
        rsa_alg.sign(b"data", FailingKey())
