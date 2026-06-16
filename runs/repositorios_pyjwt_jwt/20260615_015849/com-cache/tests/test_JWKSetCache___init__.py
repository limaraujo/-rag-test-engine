import pytest
from repositorios.pyjwt.jwt.jwk_set_cache import JWKSetCache

# happy path: verifica que jwk_set_with_timestamp começa como None e lifespan é armazenado
def test_init_happy_path_sets_defaults_and_lifespan():
    lifespan = 42.0
    cache = JWKSetCache(lifespan)
    assert cache.jwk_set_with_timestamp is None
    assert cache.lifespan == lifespan

# edge/various: verifica armazenamento correto de diferentes valores de lifespan
@pytest.mark.parametrize("lifespan", [0.0, 1.0, 3600.5])
def test_init_stores_lifespan_for_various_values(lifespan):
    cache = JWKSetCache(lifespan)
    assert cache.lifespan == lifespan
    assert cache.jwk_set_with_timestamp is None
