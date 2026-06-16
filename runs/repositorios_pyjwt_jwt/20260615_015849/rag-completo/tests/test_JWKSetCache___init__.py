import pytest
from repositorios.pyjwt.jwt.jwk_set_cache import JWKSetCache

# happy path: ensure __init__ assigns lifespan and leaves jwk_set_with_timestamp as None
@pytest.mark.parametrize("lifespan", [0.0, 10.0, 60.5])
def test_init_sets_fields_correct(lifespan):
    cache = JWKSetCache(lifespan)
    assert cache.lifespan == lifespan
    assert cache.jwk_set_with_timestamp is None
