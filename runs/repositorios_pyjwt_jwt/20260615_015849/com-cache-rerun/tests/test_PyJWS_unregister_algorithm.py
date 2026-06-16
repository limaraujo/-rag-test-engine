import pytest
from repositorios.pyjwt.jwt.api_jws import PyJWS

# curto: path feliz - remove um algoritmo existente das estruturas internas
def test_unregister_algorithm_happy_path():
    inst = PyJWS.__new__(PyJWS)
    inst._algorithms = {'alg1': object()}
    inst._valid_algs = ['alg1', 'alg2']
    inst.unregister_algorithm('alg1')
    assert 'alg1' not in inst._algorithms
    assert 'alg1' not in inst._valid_algs

# curto: exceção KeyError quando o algoritmo não está registrado
def test_unregister_algorithm_missing_key():
    inst = PyJWS.__new__(PyJWS)
    inst._algorithms = {'alg2': object()}
    inst._valid_algs = ['alg2']
    with pytest.raises(KeyError) as exc:
        inst.unregister_algorithm('alg1')
    assert "not registered" in str(exc.value)
