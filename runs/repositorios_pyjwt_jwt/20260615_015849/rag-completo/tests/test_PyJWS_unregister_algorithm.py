import pytest
from repositorios.pyjwt.jwt.api_jws import PyJWS

# curto: happy path - remove um algoritmo existente de _algorithms e _valid_algs
def test_unregister_algorithm_happy_path():
    pyjws = PyJWS.__new__(PyJWS)
    pyjws._algorithms = {'HS256': object(), 'RS256': object()}
    pyjws._valid_algs = ['HS256', 'RS256']

    pyjws.unregister_algorithm('HS256')

    assert 'HS256' not in pyjws._algorithms
    assert 'HS256' not in pyjws._valid_algs
    assert 'RS256' in pyjws._algorithms

# curto: border case - ocorre KeyError quando o algoritmo não está registrado
def test_unregister_algorithm_missing_key_raises():
    pyjws = PyJWS.__new__(PyJWS)
    pyjws._algorithms = {'RS256': object()}
    pyjws._valid_algs = ['RS256']

    with pytest.raises(KeyError):
        pyjws.unregister_algorithm('HS256')
