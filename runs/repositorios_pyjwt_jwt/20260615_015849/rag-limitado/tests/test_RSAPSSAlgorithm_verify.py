import pytest
from unittest.mock import Mock, patch
from cryptography.exceptions import InvalidSignature
from repositorios.pyjwt.jwt.algorithms import RSAPSSAlgorithm

# Helper dummy subclass to bypass __init__ requirements and provide a hash algorithm
class _DummyRSAPSS(RSAPSSAlgorithm):
    def __init__(self):
        pass

    def hash_alg(self):
        class _DummyHash:
            digest_size = 32
        return _DummyHash()

# # Verifica caminho feliz: retorna True quando key.verify não levanta InvalidSignature
def test_verify_happy_path_returns_true():
    mock_key = Mock()
    mock_key.verify.return_value = None  # no exception means success

    algo = _DummyRSAPSS()

    with patch('repositorios.pyjwt.jwt.algorithms.padding.PSS') as PSS_mock, \
         patch('repositorios.pyjwt.jwt.algorithms.padding.MGF1') as MGF1_mock:
        PSS_mock.side_effect = lambda *args, **kwargs: ("PSS", kwargs)
        MGF1_mock.side_effect = lambda arg=None: ("MGF1", arg)

        result = algo.verify(b"message", mock_key, b"signature")
        assert result is True

# # Verifica exceção InvalidSignature leva a False
def test_verify_returns_false_on_invalid_signature():
    mock_key = Mock()
    mock_key.verify.side_effect = InvalidSignature

    algo = _DummyRSAPSS()

    with patch('repositorios.pyjwt.jwt.algorithms.padding.PSS') as PSS_mock, \
         patch('repositorios.pyjwt.jwt.algorithms.padding.MGF1') as MGF1_mock:
        PSS_mock.side_effect = lambda *args, **kwargs: ("PSS", kwargs)
        MGF1_mock.side_effect = lambda arg=None: ("MGF1", arg)

        result = algo.verify(b"message", mock_key, b"signature")
        assert result is False

# # Verifica propagação de exceção distinta de InvalidSignature
def test_verify_propagates_other_exceptions():
    mock_key = Mock()
    mock_key.verify.side_effect = ValueError("boom")

    algo = _DummyRSAPSS()

    with patch('repositorios.pyjwt.jwt.algorithms.padding.PSS') as PSS_mock, \
         patch('repositorios.pyjwt.jwt.algorithms.padding.MGF1') as MGF1_mock:
        PSS_mock.side_effect = lambda *args, **kwargs: ("PSS", kwargs)
        MGF1_mock.side_effect = lambda arg=None: ("MGF1", arg)

        with pytest.raises(ValueError):
            algo.verify(b"message", mock_key, b"signature")
