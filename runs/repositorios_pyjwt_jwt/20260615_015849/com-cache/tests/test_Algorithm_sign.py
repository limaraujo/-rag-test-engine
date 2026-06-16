import pytest
from repositorios.pyjwt.jwt.algorithms import Algorithm

def test_cannot_instantiate_abstract_algorithm():
    with pytest.raises(TypeError):
        Algorithm()

def test_sign_basic_happy_path():
    class SimpleSignAlgorithm(Algorithm):
        def sign(self, msg: bytes, key):
            if not isinstance(msg, (bytes, bytearray)):
                raise TypeError("msg must be bytes")
            return b"SIGN:" + msg + b":" + str(key).encode()

        def from_jwk(self, *args, **kwargs):
            return self.__class__()

        def prepare_key(self, *args, **kwargs):
            return args[0] if args else None

        def to_jwk(self, *args, **kwargs):
            return {}

        def verify(self, *args, **kwargs):
            pass

    alg = SimpleSignAlgorithm()
    msg = b"hello"
    key = "k"
    expected = b"SIGN:" + msg + b":" + b'k'
    assert alg.sign(msg, key) == expected

def test_sign_type_enforcement_raises_for_non_bytes_input():
    class TypeCheckSignAlgorithm(Algorithm):
        def sign(self, msg, key):
            if not isinstance(msg, (bytes, bytearray)):
                raise TypeError("msg must be bytes")
            return b"signature"

        def from_jwk(self, *args, **kwargs):
            return self.__class__()

        def prepare_key(self, *args, **kwargs):
            return args[0] if args else None

        def to_jwk(self, *args, **kwargs):
            return {}

        def verify(self, *args, **kwargs):
            pass

    alg = TypeCheckSignAlgorithm()
    with pytest.raises(TypeError):
        alg.sign("not-bytes", "key")

@pytest.mark.parametrize("key", [b"bytes_key", "str_key", 123])
def test_sign_handles_various_key_types(key):
    class DynAlgorithm(Algorithm):
        def sign(self, msg: bytes, key):
            if not isinstance(msg, (bytes, bytearray)):
                raise TypeError
            return b"SIGN:" + msg + b":" + str(key).encode()

        def from_jwk(self, *args, **kwargs):
            return self.__class__()

        def prepare_key(self, *args, **kwargs):
            return args[0] if args else None

        def to_jwk(self, *args, **kwargs):
            return {}

        def verify(self, *args, **kwargs):
            pass

    alg = DynAlgorithm()
    msg = b"m"
    assert alg.sign(msg, key) == b"SIGN:" + msg + b":" + str(key).encode()
