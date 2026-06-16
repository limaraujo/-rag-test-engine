import importlib
import pytest
from repositorios.pyjwt.jwt.algorithms import Algorithm

algos = importlib.import_module("repositorios.pyjwt.jwt.algorithms")

# Verifica caminho feliz: key é do tipo esperado
def test_check_crypto_key_type_happy_path_valid_key(monkeypatch):
    class DummySelf:
        pass
    dummy = DummySelf()
    dummy._crypto_key_types = (int,)
    monkeypatch.setattr(algos, "has_crypto", True, raising=False)

    # Não deve levantar exceção
    algos.Algorithm.check_crypto_key_type(dummy, 123)

# Verifica exceção InvalidKeyError quando o key não pertence à lista esperada
def test_check_crypto_key_type_invalid_key_raises_InvalidKeyError(monkeypatch):
    class DummySelf:
        pass
    dummy = DummySelf()
    dummy._crypto_key_types = (int,)
    monkeypatch.setattr(algos, "has_crypto", True, raising=False)

    with pytest.raises(algos.InvalidKeyError):
        algos.Algorithm.check_crypto_key_type(dummy, "not-an-int")

# Verifica ValueError quando criptografia ausente
def test_check_crypto_key_type_missing_crypto_library_raises_ValueError(monkeypatch):
    class DummySelf:
        pass
    dummy = DummySelf()
    dummy._crypto_key_types = (int,)
    monkeypatch.setattr(algos, "has_crypto", False, raising=False)

    with pytest.raises(ValueError):
        algos.Algorithm.check_crypto_key_type(dummy, 1)

# Verifica ValueError quando _crypto_key_types não está definido
def test_check_crypto_key_type_missing_crypto_key_types_raises_ValueError(monkeypatch):
    class DummySelf:
        pass
    dummy = DummySelf()
    dummy._crypto_key_types = None
    monkeypatch.setattr(algos, "has_crypto", True, raising=False)

    with pytest.raises(ValueError):
        algos.Algorithm.check_crypto_key_type(dummy, 1)
