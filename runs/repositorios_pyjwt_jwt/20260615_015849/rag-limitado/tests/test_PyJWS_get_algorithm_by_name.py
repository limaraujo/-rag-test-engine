import pytest
import repositorios.pyjwt.jwt.api_jws as api_jws
from repositorios.pyjwt.jwt.api_jws import PyJWS

# happy path: algorithm exists in _algorithms
def test_get_algorithm_by_name_happy_path():
    # Verifica retorno do algoritmo existente no dicionário de algoritmos
    jws = PyJWS()
    jws._algorithms = {'RS256': 'RS256_Algorithm'}
    assert jws.get_algorithm_by_name('RS256') == 'RS256_Algorithm'

# missing algorithm with cryptography required and cryptography not installed
def test_get_algorithm_by_name_missing_requires_crypto_raises(monkeypatch):
    # Verifica NotImplementedError com mensagem sobre cryptography ausente
    jws = PyJWS()
    jws._algorithms = {}
    monkeypatch.setattr(api_jws, 'has_crypto', False)
    monkeypatch.setattr(api_jws, 'requires_cryptography', {'RS256'})
    with pytest.raises(NotImplementedError) as excinfo:
        jws.get_algorithm_by_name('RS256')
    assert "cryptography installed" in str(excinfo.value)

# missing algorithm when cryptography not required for this alg
def test_get_algorithm_by_name_missing_not_supported(monkeypatch):
    # Verifica NotImplementedError genérico quando algoritmo não suportado
    jws = PyJWS()
    jws._algorithms = {}
    monkeypatch.setattr(api_jws, 'has_crypto', False)
    monkeypatch.setattr(api_jws, 'requires_cryptography', {'HS256'})
    with pytest.raises(NotImplementedError) as excinfo:
        jws.get_algorithm_by_name('RS256')
    assert "Algorithm not supported" in str(excinfo.value)
