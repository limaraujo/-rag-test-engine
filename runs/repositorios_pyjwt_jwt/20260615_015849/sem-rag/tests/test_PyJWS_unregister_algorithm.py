import pytest
from repositorios.pyjwt.jwt.api_jws import PyJWS



def _make_pyjws_with_state(algorithms, valid_algs):
    obj = PyJWS.__new__(PyJWS)
    obj._algorithms = dict(algorithms)
    obj._valid_algs = list(valid_algs)
    return obj


# breve: happy path - remove existing algorithm from internal structures
def test_unregister_algorithm_happy_path():
    pyjws = _make_pyjws_with_state({'HS256': object()}, ['HS256', 'RS256'])
    pyjws.unregister_algorithm('HS256')
    assert 'HS256' not in pyjws._algorithms
    assert 'HS256' not in pyjws._valid_algs
    assert pyjws._valid_algs == ['RS256']


# breve: edge case - attempting to unregister a non-registered algorithm raises KeyError
def test_unregister_algorithm_missing_key():
    pyjws = _make_pyjws_with_state({'RS256': object()}, ['RS256'])
    with pytest.raises(KeyError):
        pyjws.unregister_algorithm('HS256')
