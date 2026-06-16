import pytest
from cryptography.hazmat.primitives import hashes
from repositorios.pyjwt.jwt.algorithms import RSAAlgorithm

class DummyKey:
    def __init__(self, key_size: int):
        self.key_size = key_size

# verificação: key_size abaixo do mínimo gera mensagem
def test_check_key_length_below_minimum_returns_message():
    algo = RSAAlgorithm(hashes.SHA256())
    min_size = getattr(algo, "_MIN_KEY_SIZE", None)
    assert isinstance(min_size, int)
    key = DummyKey(min_size - 1)
    result = algo.check_key_length(key)
    assert isinstance(result, str)
    assert "minimum" in result.lower() or "below" in result.lower()

# verificação: key_size igual ou acima do mínimo retorna None (caminho feliz)
def test_check_key_length_at_or_above_minimum_returns_none():
    algo = RSAAlgorithm(hashes.SHA256())
    min_size = getattr(algo, "_MIN_KEY_SIZE", None)
    assert isinstance(min_size, int)
    key = DummyKey(min_size)
    result = algo.check_key_length(key)
    assert result is None
