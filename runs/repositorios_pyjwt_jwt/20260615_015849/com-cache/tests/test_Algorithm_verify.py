import pytest
from typing import Any
from cryptography.exceptions import InvalidSignature
from repositorios.pyjwt.jwt.algorithms import Algorithm

def test_verify_is_abstract_class_cannot_instantiate():
    with pytest.raises(TypeError):
        Algorithm()

def test_concrete_subclass_verify_true():
    class ConcreteAlgorithm(Algorithm):
        def from_jwk(self, jwk: dict):
            return self

        def prepare_key(self, key: Any):
            return key

        def sign(self, msg: bytes, key: Any) -> bytes:
            return b"signature"

        def to_jwk(self, key: Any) -> dict:
            return {}

        def verify(self, msg: bytes, key: Any, sig: bytes) -> bool:
            return True

    alg = ConcreteAlgorithm()
    assert alg.verify(b"message", None, b"signature") is True

def test_concrete_subclass_verify_false():
    class ConcreteAlgorithm(Algorithm):
        def from_jwk(self, jwk: dict):
            return self

        def prepare_key(self, key: Any):
            return key

        def sign(self, msg: bytes, key: Any) -> bytes:
            return b"signature"

        def to_jwk(self, key: Any) -> dict:
            return {}

        def verify(self, msg: bytes, key: Any, sig: bytes) -> bool:
            return False

    alg = ConcreteAlgorithm()
    assert alg.verify(b"message", None, b"signature") is False

def test_verify_propagates_exceptions():
    class ConcreteAlgorithm(Algorithm):
        def from_jwk(self, jwk: dict):
            return self

        def prepare_key(self, key: Any):
            return key

        def sign(self, msg: bytes, key: Any) -> bytes:
            return b"signature"

        def to_jwk(self, key: Any) -> dict:
            return {}

        def verify(self, msg: bytes, key: Any, sig: bytes) -> bool:
            raise InvalidSignature("signature invalid")

    alg = ConcreteAlgorithm()
    with pytest.raises(InvalidSignature):
        alg.verify(b"message", None, b"signature")
