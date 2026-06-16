import pytest
from repositorios.pyjwt.jwt.api_jws import PyJWS



def _make_jws_with_alg(alg_ids):
    jws = PyJWS.__new__(PyJWS)
    jws._algorithms = {alg: object() for alg in alg_ids}
    jws._valid_algs = list(alg_ids)
    return jws


# happy path: unregister existing algorithm updates internal structures
def test_unregister_algorithm_happy_path():
    jws = _make_jws_with_alg(['HS256', 'RS256'])
    jws.unregister_algorithm('HS256')
    assert 'HS256' not in jws._algorithms
    assert 'HS256' not in jws._valid_algs
    assert 'RS256' in jws._algorithms
    assert 'RS256' in jws._valid_algs


# border case: missing_key should raise KeyError with specific message
def test_unregister_algorithm_missing_key_raises():
    jws = _make_jws_with_alg(['HS256'])
    with pytest.raises(KeyError) as exc:
        jws.unregister_algorithm('RS256')
    assert exc.value.args[0] == (
        "The specified algorithm could not be removed because it is not registered."
    )
