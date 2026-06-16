import importlib
from repositorios.pyjwt.jwt.algorithms import get_default_algorithms
from repositorios.pyjwt.jwt.algorithms import NoneAlgorithm, HMACAlgorithm
from repositorios.pyjwt.jwt.algorithms import RSAAlgorithm, OKPAlgorithm

import importlib
from repositorios.pyjwt.jwt.algorithms import get_default_algorithms


# Verifica funcionamento sem crypto (branch False)
def test_get_default_algorithms_basic_keys_without_crypto(monkeypatch):
    mod = importlib.import_module("repositorios.pyjwt.jwt.algorithms")
    monkeypatch.setattr(mod, "has_crypto", False)
    algs = mod.get_default_algorithms()

    from repositorios.pyjwt.jwt.algorithms import NoneAlgorithm, HMACAlgorithm

    assert "none" in algs
    assert isinstance(algs["none"], NoneAlgorithm)

    for key in ("HS256", "HS384", "HS512"):
        assert key in algs
        assert isinstance(algs[key], HMACAlgorithm)

    assert "RS256" not in algs


# Verifica funcionamento com crypto (branch True)
def test_get_default_algorithms_with_crypto_includes_rsa_and_okp(monkeypatch):
    mod = importlib.import_module("repositorios.pyjwt.jwt.algorithms")
    monkeypatch.setattr(mod, "has_crypto", True)
    algs = mod.get_default_algorithms()

    from repositorios.pyjwt.jwt.algorithms import RSAAlgorithm, OKPAlgorithm

    assert "RS256" in algs and isinstance(algs["RS256"], RSAAlgorithm)
    assert "EdDSA" in algs and isinstance(algs["EdDSA"], OKPAlgorithm)
