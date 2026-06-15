import pytest
from repositorios.pyjwt.jwt.algorithms import Algorithm

def test_sign_is_abstract_method():
    assert getattr(Algorithm.sign, "__isabstractmethod__", False) is True

def test_cannot_instantiate_subclass_without_sign():
    class Incomplete(Algorithm):
        pass

    with pytest.raises(TypeError):
        Incomplete()

def test_concrete_subclass_sign_returns_bytes():
    class Concrete(Algorithm):
        def sign(self, msg: bytes, key) -> bytes:
            return b"signature"

        def from_jwk(self, jwk: dict):
            return self

        def prepare_key(self, key):
            return key

        def to_jwk(self) -> dict:
            return {}

        def verify(self, msg: bytes, signature: bytes, key) -> bool:
            return True

    obj = Concrete()
    result = obj.sign(b"msg", key="testkey")
    assert isinstance(result, (bytes, bytearray))
    assert result == b"signature"
