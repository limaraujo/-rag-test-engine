import pytest
from unittest.mock import Mock
import importlib
from repositorios.pyjwt.jwt.api_jwk import PyJWK

api_jwk = importlib.import_module("repositorios.pyjwt.jwt.api_jwk")


# Test 1: happy path - from_json should forward to PyJWK.from_dict with parsed obj and provided algorithm
def test_from_json_forwards_arguments_and_returns_value(monkeypatch):
    PyJWK_from_dict_mock = Mock(return_value="SENTINEL")
    monkeypatch.setattr(api_jwk.PyJWK, "from_dict", PyJWK_from_dict_mock)
    data = '{"kid": "abc"}'
    alg = "RS256"
    result = api_jwk.PyJWK.from_json(data, algorithm=alg)
    assert result == "SENTINEL"
    PyJWK_from_dict_mock.assert_called_with({"kid": "abc"}, alg)


# Test 2: default behavior when algorithm is not provided should pass None for algorithm
def test_from_json_passes_none_algorithm_when_not_provided(monkeypatch):
    PyJWK_from_dict_mock = Mock(return_value="SENTINEL2")
    monkeypatch.setattr(api_jwk.PyJWK, "from_dict", PyJWK_from_dict_mock)
    data = '{"kid": "def"}'
    result = api_jwk.PyJWK.from_json(data)  # algorithm defaults to None
    assert result == "SENTINEL2"
    PyJWK_from_dict_mock.assert_called_with({"kid": "def"}, None)


# Test 3: exception propagation when PyJWK.from_dict raises an error
def test_from_json_propagates_exceptions(monkeypatch):
    PyJWK_from_dict_mock = Mock(side_effect=ValueError("bad"))
    monkeypatch.setattr(api_jwk.PyJWK, "from_dict", PyJWK_from_dict_mock)
    with pytest.raises(ValueError):
        api_jwk.PyJWK.from_json('{"foo": "bar"}')
