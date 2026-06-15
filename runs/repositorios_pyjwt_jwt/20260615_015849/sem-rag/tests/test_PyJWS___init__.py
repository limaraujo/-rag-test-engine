import pytest
from repositorios.pyjwt.jwt.api_jws import PyJWS

# happy path: whitelist subset of algorithms and merge provided options
def test_init_with_subset_algorithms_and_merge_options(monkeypatch):
    def mock_default_algorithms():
        return {'HS256': 'a', 'RS256': 'b', 'ES256': 'c'}

    monkeypatch.setattr(
        "repositorios.pyjwt.jwt.api_jws.get_default_algorithms", mock_default_algorithms
    )
    monkeypatch.setattr(PyJWS, "_get_default_options", lambda self: {"optA": 1, "optB": 2})

    jws = PyJWS(algorithms=['HS256', 'RS256'], options={'optB': 99})

    assert set(jws._algorithms.keys()) == {'HS256', 'RS256'}
    assert jws._valid_algs == {'HS256', 'RS256'}
    assert jws.options == {'optA': 1, 'optB': 99}


# default behavior when algorithms=None and options provided by default options
def test_init_defaults_with_all_algorithms_and_no_options(monkeypatch):
    def mock_default_algorithms():
        return {'HS256': 'a', 'RS256': 'b', 'ES256': 'c'}

    monkeypatch.setattr(
        "repositorios.pyjwt.jwt.api_jws.get_default_algorithms", mock_default_algorithms
    )
    monkeypatch.setattr(PyJWS, "_get_default_options", lambda self: {"optA": 1, "optB": 2})

    jws = PyJWS()

    assert set(jws._algorithms.keys()) == {'HS256', 'RS256', 'ES256'}
    assert jws._valid_algs == {'HS256', 'RS256', 'ES256'}
    assert jws.options == {'optA': 1, 'optB': 2}


# detalhes de mesclagem de opções quando apenas opções adicionais são fornecidas
def test_init_defaults_and_additional_options(monkeypatch):
    def mock_default_algorithms():
        return {'HS256': 'a', 'RS256': 'b', 'ES256': 'c'}

    monkeypatch.setattr(
        "repositorios.pyjwt.jwt.api_jws.get_default_algorithms", mock_default_algorithms
    )
    monkeypatch.setattr(PyJWS, "_get_default_options", lambda self: {"optA": 1, "optB": 2})

    jws = PyJWS(options={'optC': 3})

    assert set(jws._algorithms.keys()) == {'HS256', 'RS256', 'ES256'}
    assert jws._valid_algs == {'HS256', 'RS256', 'ES256'}
    assert jws.options == {'optA': 1, 'optB': 2, 'optC': 3}
