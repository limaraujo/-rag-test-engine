import pytest
from unittest.mock import Mock
from repositorios.pyjwt.jwt.exceptions import PyJWKClientError
from repositorios.pyjwt.jwt.jwks_client import PyJWKClient


# Test 1: happy path - first lookup succeeds without refresh
def test_get_signing_key_happy_path_first_try():
    # curto: confirma retorno quando a chave é encontrada no conjunto atual
    client = object.__new__(PyJWKClient)
    client.get_signing_keys = Mock(side_effect=lambda refresh=False, **kwargs: ["notfound"])
    client.match_kid = Mock(side_effect=lambda keys, kid: "SIGNING_KEY")

    signing_key = client.get_signing_key("kid-123")

    assert signing_key == "SIGNING_KEY"


# Test 2: retry path - first attempt fails, refresh and then succeeds
def test_get_signing_key_refresh_and_retry_success():
    # curto: verifica que, se não houver match na primeira leitura, o conjunto é refrescado e o segundo match funciona
    client = object.__new__(PyJWKClient)

    def fake_get_signing_keys(refresh=False, **kwargs):
        return ["notfound"] if not refresh else ["ready"]

    client.get_signing_keys = Mock(side_effect=fake_get_signing_keys)

    def fake_match_kid(keys, kid):
        return "SIGNING_KEY" if keys == ["ready"] else None

    client.match_kid = Mock(side_effect=fake_match_kid)

    signing_key = client.get_signing_key("kid-123")

    assert signing_key == "SIGNING_KEY"


# Test 3: failure after retry - raises PyJWKClientError when second lookup also fails
def test_get_signing_key_retry_failure_raises():
    # curto: confirma exceção quando nem o cache nem a recarga produzem uma chave correspondente
    client = object.__new__(PyJWKClient)

    def fake_get_signing_keys(refresh=False, **kwargs):
        return ["notfound"] if not refresh else ["stillnotfound"]

    client.get_signing_keys = Mock(side_effect=fake_get_signing_keys)
    client.match_kid = Mock(side_effect=lambda keys, kid: None)

    with pytest.raises(PyJWKClientError):
        client.get_signing_key("kid-123")
