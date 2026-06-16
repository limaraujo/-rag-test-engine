import pytest
from repositorios.pyjwt.jwt.jwk_set_cache import JWKSetCache


# Verifica inicialização básica (happy path): jwk_set_with_timestamp é None e lifespan é atribuído corretamente
def test_init_happy_path_sets_defaults():
    lifespan = 123.456
    cache = JWKSetCache(lifespan=lifespan)
    assert cache.jwk_set_with_timestamp is None
    assert cache.lifespan == lifespan

# Caso de borda: lifespans 0.0 e -1.0 são cobridos como cenários de borda
@pytest.mark.parametrize("lifespan", [0.0, -1.0])
def test_init_edge_case_zero_and_negative_lifespan(lifespan):
    cache = JWKSetCache(lifespan=lifespan)
    assert cache.jwk_set_with_timestamp is None
    assert cache.lifespan == lifespan
