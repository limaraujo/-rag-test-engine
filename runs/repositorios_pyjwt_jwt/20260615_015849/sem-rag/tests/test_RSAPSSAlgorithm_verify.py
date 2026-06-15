from cryptography.exceptions import InvalidSignature
from repositorios.pyjwt.jwt.algorithms import RSAPSSAlgorithm
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import hashes

from cryptography.exceptions import InvalidSignature
from repositorios.pyjwt.jwt.algorithms import RSAPSSAlgorithm

# Verifica retorno True (happy path) quando key.verify não levanta exceção
def test_rsa_pss_verify_success():
    from cryptography.hazmat.primitives import hashes

    fake_hash_algo = hashes.SHA256()

    class DummySelf:
        def __init__(self, h):
            self._h = h
        def hash_alg(self):
            return self._h

    dummy = DummySelf(fake_hash_algo)

    class FakeKey:
        def __init__(self):
            self.called = False
            self.last = None
        def verify(self, signature, message, padding_arg, hash_alg_arg):
            self.called = True
            self.last = (signature, message, padding_arg, hash_alg_arg)

    key = FakeKey()
    msg = b"hello world"
    sig = b"signature-bytes"

    result = RSAPSSAlgorithm.verify(dummy, msg, key, sig)
    assert result is True
    assert key.called

# Verifica retorno False quando key.verify levanta InvalidSignature
def test_rsa_pss_verify_invalid_signature():
    from cryptography.hazmat.primitives import hashes

    fake_hash_algo = hashes.SHA256()

    class DummySelf:
        def __init__(self, h):
            self._h = h
        def hash_alg(self):
            return self._h

    dummy = DummySelf(fake_hash_algo)

    class FakeKey:
        def verify(self, signature, message, padding_arg, hash_alg_arg):
            raise InvalidSignature

    key = FakeKey()
    msg = b"hello world"
    sig = b"signature-bytes"

    result = RSAPSSAlgorithm.verify(dummy, msg, key, sig)
    assert result is False
