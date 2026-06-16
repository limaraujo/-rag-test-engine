from cryptography.hazmat.primitives.asymmetric import padding
import pytest
from repositorios.pyjwt.jwt.algorithms import RSAAlgorithm

class DummyKey:
    def __init__(self, result=b"signature", raise_exc=None):
        self.result = result
        self.raise_exc = raise_exc
        self.args = None

    def sign(self, msg, pad, hash_alg):
        self.args = (msg, pad, hash_alg)
        if self.raise_exc is not None:
            raise self.raise_exc
        return self.result

class RSAAlgorithmForTest(RSAAlgorithm):
    def __init__(self):
        pass

    def hash_alg(self):
        return "HASH"

# curto: happy path - RSAAlgorithm.sign retorna assinatura e usa PKCS1v15 com hash_alg
def test_sign_happy_path():
    key = DummyKey(result=b"sig")
    algo = RSAAlgorithmForTest()
    signature = algo.sign(b"message", key)
    assert signature == b"sig"
    assert isinstance(key.args[1], padding.PKCS1v15)
    assert key.args[2] == "HASH"

# curto: exceção propagada de key.sign - a função não a trata
def test_sign_propagates_exception_from_key_sign():
    key = DummyKey(raise_exc=ValueError("boom"))
    algo = RSAAlgorithmForTest()
    with pytest.raises(ValueError, match="boom"):
        algo.sign(b"message", key)

# curto: hash_alg é dinâmico/prototipado e deve ser passado ao key.sign
@pytest.mark.parametrize("hash_return", ["HASH1", "HASH2"])
def test_sign_uses_dynamic_hash_alg(hash_return):
    class CustomRSA(RSAAlgorithm):
        def __init__(self): 
            pass
        def hash_alg(self):
            return hash_return

    key = DummyKey(result=b"sig")
    algo = CustomRSA()
    signature = algo.sign(b"message", key)
    assert signature == b"sig"
    assert isinstance(key.args[1], padding.PKCS1v15)
    assert key.args[2] == hash_return
