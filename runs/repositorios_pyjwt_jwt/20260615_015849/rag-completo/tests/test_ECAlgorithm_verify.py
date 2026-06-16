import importlib
from cryptography.exceptions import InvalidSignature
import pytest
from repositorios.pyjwt.jwt.algorithms import ECAlgorithm
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import hashes

import importlib
from cryptography.exceptions import InvalidSignature
import pytest
from repositorios.pyjwt.jwt.algorithms import ECAlgorithm

def test_verify_returns_false_on_invalid_raw_signature_input(monkeypatch):
    mod = importlib.import_module("repositorios.pyjwt.jwt.algorithms")

    class DummyAlgo(mod.ECAlgorithm):
        def __init__(self):
            pass

        def hash_alg(self):
            from cryptography.hazmat.primitives import hashes
            return hashes.SHA256()

    alg = DummyAlgo()

    def raise_value_error(sig, curve):
        raise ValueError("invalid raw signature")

    monkeypatch.setattr(mod, "raw_to_der_signature", raise_value_error)

    class DummyKey:
        curve = object()

    key = DummyKey()
    assert alg.verify(b"msg", key, b"sig") is False

def test_verify_returns_true_on_public_key_success(monkeypatch):
    mod = importlib.import_module("repositorios.pyjwt.jwt.algorithms")

    class DummyAlgo(mod.ECAlgorithm):
        def __init__(self):
            pass

        def hash_alg(self):
            from cryptography.hazmat.primitives import hashes
            return hashes.SHA256()

    alg = DummyAlgo()

    def to_der(sig, curve):
        return b"der"

    monkeypatch.setattr(mod, "raw_to_der_signature", to_der)

    class PublicKeyMock:
        curve = object()

        def __init__(self):
            self.verify_called = False

        def verify(self, der_sig, msg, algo):
            self.verify_called = True

    pk = PublicKeyMock()

    assert alg.verify(b"msg", pk, b"sig") is True
    assert pk.verify_called is True

def test_verify_returns_false_on_invalid_signature(monkeypatch):
    mod = importlib.import_module("repositorios.pyjwt.jwt.algorithms")

    class DummyAlgo(mod.ECAlgorithm):
        def __init__(self):
            pass

        def hash_alg(self):
            from cryptography.hazmat.primitives import hashes
            return hashes.SHA256()

    alg = DummyAlgo()

    def to_der(sig, curve):
        return b"der"

    monkeypatch.setattr(mod, "raw_to_der_signature", to_der)

    class PublicKeyMock:
        curve = object()

        def verify(self, der_sig, msg, algo):
            raise InvalidSignature()

    pk = PublicKeyMock()

    assert alg.verify(b"msg", pk, b"sig") is False

def test_verify_private_key_branch_success(monkeypatch):
    mod = importlib.import_module("repositorios.pyjwt.jwt.algorithms")

    class DummyAlgo(mod.ECAlgorithm):
        def __init__(self):
            pass

        def hash_alg(self):
            from cryptography.hazmat.primitives import hashes
            return hashes.SHA256()

    alg = DummyAlgo()

    class DummyPrivateKey:
        curve = object()

        def __init__(self, pub):
            self._pub = pub

        def public_key(self):
            return self._pub

    class DummyPublicKey:
        def __init__(self):
            self.verify_called = False

        def verify(self, der_sig, msg, algo):
            self.verify_called = True

    monkeypatch.setattr(mod, "EllipticCurvePrivateKey", DummyPrivateKey)

    pub = DummyPublicKey()
    private_key = DummyPrivateKey(pub)

    def to_der(sig, curve):
        return b"der"

    monkeypatch.setattr(mod, "raw_to_der_signature", to_der)

    assert alg.verify(b"msg", private_key, b"sig") is True
    assert pub.verify_called is True
