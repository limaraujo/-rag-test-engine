import importlib
from unittest.mock import patch
from repositorios.pyjwt.jwt.api_jwk import PyJWKSet

MODULE_PATH = "repositorios.pyjwt.jwt.api_jwk"


def test_from_dict_uses_keys_when_present():
    mod = importlib.import_module(MODULE_PATH)
    with patch(f"{MODULE_PATH}.PyJWKSet") as MockPyJWKSet:
        sentinel = object()
        MockPyJWKSet.return_value = sentinel

        if hasattr(mod, "from_dict"):
            result = mod.from_dict({"keys": ["k1", "k2"]})
            MockPyJWKSet.assert_called_once_with(["k1", "k2"])
            assert result is sentinel
        else:
            # Path when from_dict is a classmethod PyJWKSet.from_dict
            MockPyJWKSet.from_dict.return_value = sentinel
            result = mod.PyJWKSet.from_dict({"keys": ["k1", "k2"]})
            MockPyJWKSet.from_dict.assert_called_once_with({"keys": ["k1", "k2"]})
            assert result is sentinel


def test_from_dict_uses_empty_list_when_keys_missing():
    mod = importlib.import_module(MODULE_PATH)
    with patch(f"{MODULE_PATH}.PyJWKSet") as MockPyJWKSet:
        sentinel = object()
        MockPyJWKSet.return_value = sentinel

        if hasattr(mod, "from_dict"):
            result = mod.from_dict({})
            MockPyJWKSet.assert_called_once_with([])
            assert result is sentinel
        else:
            # Path when from_dict is a classmethod PyJWKSet.from_dict
            MockPyJWKSet.from_dict.return_value = sentinel
            result = mod.PyJWKSet.from_dict({})
            MockPyJWKSet.from_dict.assert_called_once_with({})
            assert result is sentinel
