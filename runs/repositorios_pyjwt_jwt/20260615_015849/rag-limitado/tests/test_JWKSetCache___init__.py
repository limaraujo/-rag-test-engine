import pytest
from repositorios.pyjwt.jwt.jwk_set_cache import JWKSetCache

# Teste o __init__ da JWKSetCache: verifica atribuição de jwk_set_with_timestamp e lifespans para vários cenários (0.0, 1.5, 100.0, -5.0)
@pytest.mark.parametrize("lifespan", [0.0, 1.5, 100.0, -5.0])
def test_jwk_set_cache_init_sets_fields(lifespan):
    cache = JWKSetCache(lifespan)
    assert cache.jwk_set_with_timestamp is None
    assert cache.lifespan == lifespan
