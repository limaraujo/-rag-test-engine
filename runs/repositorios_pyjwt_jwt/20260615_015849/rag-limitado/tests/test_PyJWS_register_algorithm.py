import pytest
import repositorios.pyjwt.jwt.api_jws as api_jws
from repositorios.pyjwt.jwt.api_jws import PyJWS

import pytest

import repositorios.pyjwt.jwt.api_jws as api_jws
from repositorios.pyjwt.jwt.api_jws import PyJWS


# short: Happy path - register a new algorithm and update internal structures
def setup_pyjwt_with_dummy_algorithm():
    class DummyAlgorithmBase:
        pass

    api_jws.Algorithm = DummyAlgorithmBase
    class DummyAlgorithmImplementation(DummyAlgorithmBase):
        pass

    py = PyJWS()
    alg = DummyAlgorithmImplementation()
    return py, alg, DummyAlgorithmBase, DummyAlgorithmImplementation


# short: Verifica caminho feliz ao registrar um novo algoritmo válido
def test_register_algorithm_happy_path_updates_internal_structures():
    py, alg, DummyAlgorithmBase, DummyAlgorithmImplementation = setup_pyjwt_with_dummy_algorithm()
    py.register_algorithm("custom-algo", alg)
    assert "custom-algo" in py._algorithms
    assert "custom-algo" in py._valid_algs
    assert py._algorithms["custom-algo"] is alg


# short: Verifica exceção ao tentar registrar o mesmo alg_id novamente
def test_register_algorithm_duplicate_raises_value_error():
    py, alg1, DummyAlgorithmBase, DummyAlgorithmImplementation = setup_pyjwt_with_dummy_algorithm()
    py.register_algorithm("duplicate", alg1)
    class DummyAlgorithmImplementation2(DummyAlgorithmBase):
        pass
    alg2 = DummyAlgorithmImplementation2()
    with pytest.raises(ValueError) as exc:
        py.register_algorithm("duplicate", alg2)
    assert "Algorithm already has a handler." in str(exc.value)


# short: Verifica exceção de tipo quando o objeto não é do tipo Algorithm
def test_register_algorithm_invalid_type_raises_type_error():
    py, _, DummyAlgorithmBase, _ = setup_pyjwt_with_dummy_algorithm()
    invalid_obj = object()
    with pytest.raises(TypeError) as exc:
        py.register_algorithm("invalid", invalid_obj)
    assert "Object is not of type `Algorithm`" in str(exc.value)
