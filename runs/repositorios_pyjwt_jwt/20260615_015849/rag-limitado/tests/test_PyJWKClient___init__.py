import importlib
import pytest
from repositorios.pyjwt.jwt.jwks_client import PyJWKClient


# Helper to load the target module to patch its internals per test
def _load_module():
    return importlib.import_module("repositorios.pyjwt.jwt.jwks_client")


# test 1: happy path with both caches enabled and positive lifespan
# verifies proper initialization, JWKSetCache creation, and lru_cache wrapping
def test_init_happy_path_with_caches(monkeypatch):
    mod = _load_module()

    class DummyJWKSetCache:
        def __init__(self, lifespan):
            self.lifespan = lifespan

    def spy_lru_cache(maxsize=None):
        def decorator(func):
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            wrapper._spy_maxsize = maxsize
            wrapper._spy = True
            return wrapper
        return decorator

    monkeypatch.setattr(mod, "JWKSetCache", DummyJWKSetCache)
    monkeypatch.setattr(mod, "lru_cache", spy_lru_cache)

    PyJWKClient = mod.PyJWKClient
    client = PyJWKClient(
        "https://example.com/.well-known/jwks.json",
        cache_keys=True,
        max_cached_keys=8,
        cache_jwk_set=True,
        lifespan=120
    )

    assert client.uri == "https://example.com/.well-known/jwks.json"
    assert client.jwk_set_cache is not None
    assert isinstance(client.jwk_set_cache, DummyJWKSetCache)
    assert client.jwk_set_cache.lifespan == 120
    assert getattr(client.get_signing_key, "_spy", False) is True
    assert getattr(client.get_signing_key, "_spy_maxsize", None) == 8


# test 2: invalid scheme should raise PyJWKClientError
def test_init_invalid_scheme_raises(monkeypatch):
    mod = _load_module()
    PyJWKClient = mod.PyJWKClient
    with pytest.raises(mod.PyJWKClientError) as excinfo:
        PyJWKClient("ftp://example.com/jwks", cache_jwk_set=False)
    assert "Invalid JWKS URI scheme" in str(excinfo.value)


# test 3: invalid lifespan when cache_jwk_set is enabled should raise PyJWKClientError
def test_init_invalid_lifespan_raises(monkeypatch):
    mod = _load_module()

    class DummyJWKSetCache:
        def __init__(self, lifespan):
            self.lifespan = lifespan

    monkeypatch.setattr(mod, "JWKSetCache", DummyJWKSetCache)

    PyJWKClient = mod.PyJWKClient
    with pytest.raises(mod.PyJWKClientError) as excinfo:
        PyJWKClient("https://example.com/jwks", cache_jwk_set=True, lifespan=0)

    assert "Lifespan must be greater than 0" in str(excinfo.value)


# test 4: when cache_jwk_set is disabled, jwk_set_cache should be None
def test_init_cache_jwk_set_disabled_no_cache_created(monkeypatch):
    mod = _load_module()

    class DummyJWKSetCache:
        def __init__(self, lifespan):
            self.lifespan = lifespan

    # lru_cache is patched but should not be exercised when cache_jwk_set=False
    def spy_lru_cache(maxsize=None):
        def decorator(func):
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            wrapper._spy_maxsize = maxsize
            wrapper._spy = True
            return wrapper
        return decorator

    monkeypatch.setattr(mod, "JWKSetCache", DummyJWKSetCache)
    monkeypatch.setattr(mod, "lru_cache", spy_lru_cache)

    PyJWKClient = mod.PyJWKClient
    client = PyJWKClient("https://example.com/jwks", cache_keys=True, max_cached_keys=5, cache_jwk_set=False)

    assert client.jwk_set_cache is None
    assert isinstance(client, PyJWKClient)
