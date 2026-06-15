import pytest
from repositorios.pyjwt.jwt.exceptions import PyJWKClientError
from repositorios.pyjwt.jwt.jwks_client import PyJWKClient



# short: test helper subclass to mock internal behavior of PyJWKClient
class TestClient(PyJWKClient):
    def __init__(self, initial_keys, refreshed_keys):
        self._initial = list(initial_keys)
        self._refreshed = list(refreshed_keys)
        self.calls = []

    def get_signing_keys(self, refresh: bool = False):
        self.calls.append(("get_signing_keys", refresh))
        return list(self._initial) if not refresh else list(self._refreshed)

    def match_kid(self, signing_keys, kid):
        for k in signing_keys:
            if k == kid + "_key":
                return k
        return None


# short: happy path - key is found in the initial JWK set
def test_get_signing_key_found_on_first_try():
    kid = "kid1"
    client = TestClient(initial_keys=["kid1_key"], refreshed_keys=[])
    signing_key = client.get_signing_key(kid)
    assert signing_key == "kid1_key"
    assert client.calls == [("get_signing_keys", False)]


# short: not found initially, refreshed set contains the key
def test_get_signing_key_refresh_and_find():
    kid = "kid2"
    client = TestClient(initial_keys=["other_key"], refreshed_keys=["kid2_key"])
    signing_key = client.get_signing_key(kid)
    assert signing_key == "kid2_key"
    assert client.calls == [
        ("get_signing_keys", False),
        ("get_signing_keys", True),
    ]


# short: not found after refresh -> raises PyJWKClientError
def test_get_signing_key_not_found_after_refresh_raises():
    kid = "kid3"
    client = TestClient(initial_keys=["other_key"], refreshed_keys=["another_key"])
    with pytest.raises(PyJWKClientError):
        client.get_signing_key(kid)
