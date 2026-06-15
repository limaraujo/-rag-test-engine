from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature
from repositorios.pyjwt.jwt.algorithms import RSAPSSAlgorithm

# Raso: testar verificação bem-sucedida quando o key.verify não levanta exceção
class DummyRSAPSS(RSAPSSAlgorithm):
    def __init__(self):
        pass

    def hash_alg(self):
        return hashes.SHA256()

def test_verify_happy_path_returns_true_when_signature_valid():
    algo = DummyRSAPSS()
    class DummyKey:
        def verify(self, sig, msg, padding, hash_alg):
            # simula verificação bem-sucedida
            return
    key = DummyKey()
    msg = b"hello"
    sig = b"signature"
    assert algo.verify(msg, key, sig) is True

# Raso: testar o caminho de exceção InvalidSignature levando a False
def test_verify_invalid_signature_returns_false():
    algo = DummyRSAPSS()
    class DummyKeyRaise:
        def verify(self, sig, msg, padding, hash_alg):
            raise InvalidSignature()
    key = DummyKeyRaise()
    msg = b"hello"
    sig = b"signature"
    assert algo.verify(msg, key, sig) is False
