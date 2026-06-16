import importlib
import pytest
from repositorios.pyjwt.jwt.jwks_client import PyJWKClient

# Assuming the target module uses these symbols

class DummyCache:
    def __init__(self, value):
        self._value = value
    def get(self):
        return self._value

def test_get_jwk_set_uses_cache_when_available_and_not_refresh(monkeypatch):
    # small, focused test: use cache data and no refresh
    module = importlib.import_module("repositorios.pyjwt.jwt.jwks_client")

    # Prepare a dummy cache that returns dict data
    cached_data = {"keys": []}
    cache = DummyCache(cached_data)

    # Prepare to capture the data passed to PyJWKSet.from_dict
    captured = {}
    def fake_from_dict(cls, data):
        captured["data"] = data
        return "JWKS_OBJECT"

    monkeypatch.setattr(module.PyJWKSet, "from_dict", classmethod(fake_from_dict), raising=True)

    # Create an instance without calling __init__
    inst = PyJWKClient.__new__(PyJWKClient)
    inst.jwk_set_cache = cache
    def never_called():
        raise AssertionError("fetch_data should not be called in this test")
    inst.fetch_data = never_called

    result = inst.get_jwk_set(refresh=False)

    assert result == "JWKS_OBJECT"
    assert captured["data"] is cached_data

def test_get_jwk_set_fetches_when_cache_missing(monkeypatch):
    # small test: no cache data, fetch_data provides dict
    module = importlib.import_module("repositorios.pyjwt.jwt.jwks_client")

    cache = DummyCache(None)

    data_from_fetch = {"keys": [{"kty": "RSA"}]}
    def fake_fetch_data():
        return data_from_fetch

    captured = {}
    def fake_from_dict(cls, data):
        captured["data"] = data
        return "JWKS_OBJECT"

    monkeypatch.setattr(module.PyJWKSet, "from_dict", classmethod(fake_from_dict), raising=True)

    inst = PyJWKClient.__new__(PyJWKClient)
    inst.jwk_set_cache = cache
    inst.fetch_data = fake_fetch_data

    result = inst.get_jwk_set(refresh=False)

    assert result == "JWKS_OBJECT"
    assert captured["data"] is data_from_fetch

def test_get_jwk_set_raises_on_non_json_object(monkeypatch):
    # small test: fetch_data returns non-dict -> raise PyJWKClientError
    module = importlib.import_module("repositorios.pyjwt.jwt.jwks_client")

    cache = DummyCache(None)

    def fake_fetch_data():
        return "not-a-dict"

    def fake_from_dict(cls, data):
        return "JWKS_OBJECT"

    monkeypatch.setattr(module.PyJWKSet, "from_dict", classmethod(fake_from_dict), raising=True)

    inst = PyJWKClient.__new__(PyJWKClient)
    inst.jwk_set_cache = cache
    inst.fetch_data = fake_fetch_data

    with pytest.raises(Exception) as excinfo:
        inst.get_jwk_set(refresh=False)

    assert "The JWKS endpoint did not return a JSON object" in str(excinfo.value)

def test_get_jwk_set_refresh_bypasses_cache(monkeypatch):
    # small test: when refresh=True, data should come from fetch_data even if cache has data
    module = importlib.import_module("repositorios.pyjwt.jwt.jwks_client")

    cached_data = {"keys": []}
    cache = DummyCache(cached_data)

    data_from_fetch = {"keys": [{"kty": "EC"}]}
    def fake_fetch_data():
        return data_from_fetch

    captured = {}
    def fake_from_dict(cls, data):
        captured["data"] = data
        return "JWKS_OBJECT"

    monkeypatch.setattr(module.PyJWKSet, "from_dict", classmethod(fake_from_dict), raising=True)

    inst = PyJWKClient.__new__(PyJWKClient)
    inst.jwk_set_cache = cache
    inst.fetch_data = fake_fetch_data

    result = inst.get_jwk_set(refresh=True)

    assert result == "JWKS_OBJECT"
    assert captured["data"] is data_from_fetch
