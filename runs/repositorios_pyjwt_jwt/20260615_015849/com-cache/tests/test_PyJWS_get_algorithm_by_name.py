import pytest
from repositorios.pyjwt.jwt.api_jws import PyJWS

# happy path: retrieve existing algorithm from _algorithms
def test_get_algorithm_by_name_happy_path(monkeypatch):
    jws = PyJWS()
    jws._algorithms = {"RS256": "RS256-ALG"}
    assert jws.get_algorithm_by_name("RS256") == "RS256-ALG"

# missing key triggers cryptography-required NotImplementedError when alg is in requires_cryptography
def test_get_algorithm_by_name_missing_requires_crypto(monkeypatch):
    jws = PyJWS()
    jws._algorithms = {}
    monkeypatch.setattr("repositorios.pyjwt.jwt.api_jws.has_crypto", False)
    monkeypatch.setattr("repositorios.pyjwt.jwt.api_jws.requires_cryptography", {"RS256"})
    with pytest.raises(NotImplementedError) as exc:
        jws.get_algorithm_by_name("RS256")
    assert "could not be found" in str(exc.value)
    assert "Do you have cryptography installed?" in str(exc.value)

# missing key triggers generic NotImplementedError when cryptography is not required
def test_get_algorithm_by_name_missing_not_supported(monkeypatch):
    jws = PyJWS()
    jws._algorithms = {}
    monkeypatch.setattr("repositorios.pyjwt.jwt.api_jws.has_crypto", True)
    monkeypatch.setattr("repositorios.pyjwt.jwt.api_jws.requires_cryptography", set())
    with pytest.raises(NotImplementedError) as exc:
        jws.get_algorithm_by_name("RS256")
    assert str(exc.value) == "Algorithm not supported"
