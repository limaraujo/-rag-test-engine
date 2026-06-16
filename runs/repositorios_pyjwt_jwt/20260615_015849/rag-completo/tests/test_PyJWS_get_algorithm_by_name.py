import pytest
from repositorios.pyjwt.jwt.api_jws import PyJWS



class DummyAlgorithm:
    pass


# happy path: existing algorithm returned from internal _algorithms mapping
def test_get_algorithm_by_name_happy_path(monkeypatch):
    jws = PyJWS()
    alg = DummyAlgorithm()
    jws._algorithms = {"RS256": alg}
    assert jws.get_algorithm_by_name("RS256") is alg


# exception path: cryptography is required but not installed
def test_get_algorithm_by_name_requires_crypto_not_installed(monkeypatch):
    monkeypatch.setattr("repositorios.pyjwt.jwt.api_jws.has_crypto", False)
    monkeypatch.setattr(
        "repositorios.pyjwt.jwt.api_jws.requires_cryptography", {"RS256"}
    )
    jws = PyJWS()
    jws._algorithms = {}
    with pytest.raises(NotImplementedError) as exc:
        jws.get_algorithm_by_name("RS256")
    assert "cryptography" in str(exc.value)


# exception path: algorithm not supported when not in cryptography requirements
def test_get_algorithm_by_name_not_supported_without_cryptography_requirement(monkeypatch):
    monkeypatch.setattr("repositorios.pyjwt.jwt.api_jws.has_crypto", False)
    monkeypatch.setattr("repositorios.pyjwt.jwt.api_jws.requires_cryptography", set())
    jws = PyJWS()
    jws._algorithms = {}
    with pytest.raises(NotImplementedError) as exc:
        jws.get_algorithm_by_name("RS256")
    assert "Algorithm not supported" in str(exc.value)


# exception path: when cryptography is available, still not supported
def test_get_algorithm_by_name_not_supported_even_if_crypto_available(monkeypatch):
    monkeypatch.setattr("repositorios.pyjwt.jwt.api_jws.has_crypto", True)
    monkeypatch.setattr(
        "repositorios.pyjwt.jwt.api_jws.requires_cryptography", {"RS256"}
    )
    jws = PyJWS()
    jws._algorithms = {}
    with pytest.raises(NotImplementedError) as exc:
        jws.get_algorithm_by_name("RS256")
    assert "Algorithm not supported" in str(exc.value)
