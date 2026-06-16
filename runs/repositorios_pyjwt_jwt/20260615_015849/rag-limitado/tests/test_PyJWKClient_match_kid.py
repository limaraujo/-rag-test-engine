from types import SimpleNamespace
import repositorios.pyjwt.jwt.jwks_client as jwks_module
from repositorios.pyjwt.jwt.jwks_client import PyJWKClient

from types import SimpleNamespace

import repositorios.pyjwt.jwt.jwks_client as jwks_module
from repositorios.pyjwt.jwt.jwks_client import PyJWKClient


def _match_kid(signing_keys, kid):
    # try staticmethod on PyJWKClient, fallback to module-level function if needed
    if hasattr(jwks_module.PyJWKClient, "match_kid"):
        return jwks_module.PyJWKClient.match_kid(signing_keys, kid)
    else:
        return getattr(jwks_module, "match_kid")(signing_keys, kid)


# Verifica happy path: encontra o key com kid correspondente entre várias chaves
def test_match_kid_finds_matching_key():
    k1 = SimpleNamespace(key_id="abc")
    k2 = SimpleNamespace(key_id="def")
    signing_keys = [k1, k2]
    assert _match_kid(signing_keys, "def") is k2


# Verifica retorna a primeira correspondência quando múltiplas chaves compartilham o mesmo kid
def test_match_kid_returns_first_matching_key():
    k1 = SimpleNamespace(key_id="x")
    k2 = SimpleNamespace(key_id="y")
    k3 = SimpleNamespace(key_id="x")
    signing_keys = [k1, k2, k3]
    assert _match_kid(signing_keys, "x") is k1


# Verifica caso em que nenhum key com o kid informado é encontrado (retorna None)
def test_match_kid_returns_none_when_not_found():
    k1 = SimpleNamespace(key_id="foo")
    signing_keys = [k1]
    assert _match_kid(signing_keys, "bar") is None
