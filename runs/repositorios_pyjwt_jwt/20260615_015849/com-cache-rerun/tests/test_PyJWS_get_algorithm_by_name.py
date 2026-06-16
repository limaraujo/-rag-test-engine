import pytest
import repositorios.pyjwt.jwt.api_jws as api_jws
from repositorios.pyjwt.jwt.api_jws import PyJWS

# happy path: existing algorithm mapping is returned
def test_get_algorithm_by_name_happy_path():
    jws = PyJWS()
    jws._algorithms = {"RS256": "dummy_alg"}
    assert jws.get_algorithm_by_name("RS256") == "dummy_alg"

# border: missing key but algorithm requires cryptography (NotImplementedError cryptography message)
def test_get_algorithm_by_name_missing_key_requires_crypto(monkeypatch):
    # missing_key in _algorithms, cryptography is required for this alg
    monkeypatch.setattr(api_jws, "has_crypto", False, raising=False)
    monkeypatch.setattr(api_jws, "requires_cryptography", {"RS256"}, raising=False)

    jws = PyJWS()
    jws._algorithms = {}

    with pytest.raises(NotImplementedError) as excinfo:
        jws.get_algorithm_by_name("RS256")

    assert "cryptography" in str(excinfo.value)

# border: missing key and cryptography not a prerequisite (NotImplementedError not supported)
def test_get_algorithm_by_name_missing_key_not_supported(monkeypatch):
    # missing_key in _algorithms and cryptography not required for this alg
    monkeypatch.setattr(api_jws, "has_crypto", True, raising=False)
    monkeypatch.setattr(api_jws, "requires_cryptography", set(), raising=False)

    jws = PyJWS()
    jws._algorithms = {}

    with pytest.raises(NotImplementedError) as excinfo:
        jws.get_algorithm_by_name("RS256")

    assert "Algorithm not supported" in str(excinfo.value)
