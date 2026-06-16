import importlib
import pytest
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from repositorios.pyjwt.jwt.algorithms import Algorithm

alg_module = importlib.import_module("repositorios.pyjwt.jwt.algorithms")


def test_compute_hash_digest_with_hash_algorithm_type_happy_path():
    alg_module.has_crypto = True

    class DummyAlgorithm(alg_module.Algorithm):
        def __init__(self):
            self.hash_alg = hashes.SHA256

        def from_jwk(self, *args, **kwargs):  # type: ignore
            raise NotImplementedError

        def prepare_key(self, *args, **kwargs):  # type: ignore
            pass

        def sign(self, *args, **kwargs):  # type: ignore
            raise NotImplementedError

        def to_jwk(self, *args, **kwargs):  # type: ignore
            raise NotImplementedError

        def verify(self, *args, **kwargs):  # type: ignore
            raise NotImplementedError

    obj = DummyAlgorithm()
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(b"hello")
    expected = digest.finalize()
    assert obj.compute_hash_digest(b"hello") == expected


def test_compute_hash_digest_with_non_hash_class_else_path():
    alg_module.has_crypto = True

    class FakeNonHash:
        def __init__(self, data):
            self._data = data

        def digest(self):
            return b"ELSE"

    class DummyAlgorithm(alg_module.Algorithm):
        def __init__(self):
            self.hash_alg = FakeNonHash

        def from_jwk(self, *args, **kwargs):  # type: ignore
            raise NotImplementedError

        def prepare_key(self, *args, **kwargs):  # type: ignore
            pass

        def sign(self, *args, **kwargs):  # type: ignore
            raise NotImplementedError

        def to_jwk(self, *args, **kwargs):  # type: ignore
            raise NotImplementedError

        def verify(self, *args, **kwargs):  # type: ignore
            raise NotImplementedError

    obj = DummyAlgorithm()
    assert obj.compute_hash_digest(b"data") == b"ELSE"


def test_compute_hash_digest_raises_not_implemented_when_hash_alg_missing():
    alg_module.has_crypto = True

    class DummyAlgorithm(alg_module.Algorithm):
        def __init__(self):
            pass  # intentionally without hash_alg

        def from_jwk(self, *args, **kwargs):  # type: ignore
            raise NotImplementedError

        def prepare_key(self, *args, **kwargs):  # type: ignore
            pass

        def sign(self, *args, **kwargs):  # type: ignore
            raise NotImplementedError

        def to_jwk(self, *args, **kwargs):  # type: ignore
            raise NotImplementedError

        def verify(self, *args, **kwargs):  # type: ignore
            raise NotImplementedError

    obj = DummyAlgorithm()
    with pytest.raises(NotImplementedError):
        obj.compute_hash_digest(b"any")
