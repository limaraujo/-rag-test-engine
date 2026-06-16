import pytest
from repositorios.pyjwt.jwt.jwk_set_cache import JWKSetCache

# Verifica o caminho feliz de __init__: lifespan é armazenado e jwk_set_with_timestamp inicia None
@pytest.mark.parametrize("lifespan", [0.0, 1.5, 3600.0, float('inf')])
def test_jwk_set_cache_init_happy_path_sets_lifespan_and_none_field(lifespan):
    cache = JWKSetCache(lifespan)
    assert cache.lifespan == lifespan
    assert cache.jwk_set_with_timestamp is None
