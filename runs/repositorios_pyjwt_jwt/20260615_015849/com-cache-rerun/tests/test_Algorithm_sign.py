import pytest
from typing import Any
from repositorios.pyjwt.jwt.algorithms import Algorithm

# Verifica que Algorithm.sign é abstractmethod (caso de base, não instanciável)
def test_sign_is_abstractmethod():
    assert getattr(Algorithm.sign, "__isabstractmethod__", False) is True

# Verifica que não se pode instanciar a classe abstrata Algorithm
def test_cannot_instantiate_abstract_class():
    with pytest.raises(TypeError):
        Algorithm()

# Verifica que uma subclasse concreta pode implementar sign e retornar bytes
def test_concrete_subclass_can_sign():
    class ConcreteAlgorithm(Algorithm):
        def sign(self, msg: bytes, key: Any) -> bytes:
            return b"sig:" + msg + b":" + str(key).encode()

        @classmethod
        def from_jwk(cls, jwk: Any) -> "ConcreteAlgorithm":
            return cls()

        def prepare_key(self, key: Any) -> Any:
            return key

        def to_jwk(self) -> Any:
            return {}

        def verify(self, *args, **kwargs) -> bool:
            return True

    alg = ConcreteAlgorithm()
    result = alg.sign(b"hello", 42)
    assert isinstance(result, (bytes, bytearray))
    assert result.startswith(b"sig:") and b"hello" in result
