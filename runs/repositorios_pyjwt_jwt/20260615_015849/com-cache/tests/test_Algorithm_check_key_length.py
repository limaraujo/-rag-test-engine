import pytest
from repositorios.pyjwt.jwt.algorithms import Algorithm

class MinimalAlgorithm(Algorithm):
    @classmethod
    def from_jwk(cls, jwk):
        raise NotImplementedError

    def prepare_key(self, key):
        raise NotImplementedError

    def sign(self, *args, **kwargs):
        raise NotImplementedError

    def to_jwk(self):
        raise NotImplementedError

    def verify(self, *args, **kwargs):
        raise NotImplementedError

def test_check_key_length_various_inputs_returns_none():
    for key in [None, "", "a", "short", "a" * 10, 123, b"bytes", 2**20]:
        alg = MinimalAlgorithm()
        assert alg.check_key_length(key) is None

def test_check_key_length_bound_to_instance_returns_none():
    alg = MinimalAlgorithm()
    assert callable(alg.check_key_length)
    assert alg.check_key_length("sample-key") is None
