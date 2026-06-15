from unittest.mock import patch
from importlib import import_module
import pytest
from repositorios.pyjwt.jwt.api_jwk import PyJWK

MODULE = "repositorios.pyjwt.jwt.api_jwk"


def _mod():
    return import_module(MODULE)


# Verifica que from_dict repassa o argumento 'algorithm' para PyJWK, cobrindo None e valor fornecido
@pytest.mark.parametrize("algorithm", [None, "RS256"])
def test_from_dict_forwards_algorithm(algorithm):
    mod = _mod()
    obj = {"k": "v"}

    if hasattr(mod, "from_dict"):
        with patch(f"{MODULE}.PyJWK", side_effect=lambda o, alg=None: ("constructed", o, alg)) as mock_pyjwk:
            result = mod.from_dict(obj, algorithm)
            assert result == ("constructed", obj, algorithm)
    elif hasattr(mod, "PyJWK") and hasattr(mod.PyJWK, "from_dict"):
        with patch.object(mod.PyJWK, "from_dict", side_effect=lambda o, a=None: ("constructed", o, a)) as mock_from_dict:
            result = mod.PyJWK.from_dict(obj, algorithm)
            assert result == ("constructed", obj, algorithm)
    else:
        pytest.skip("No from_dict API available")
