import pytest
import repositorios.pyjwt.jwt.algorithms as alg_mod
from repositorios.pyjwt.jwt.algorithms import get_default_algorithms


# curto: happy path sem crypto backend; verifica apenas None/HS algorithums
def test_get_default_algorithms_without_crypto(monkeypatch):
    monkeypatch.setattr(alg_mod, "has_crypto", False)
    algs = get_default_algorithms()

    assert set(algs.keys()) == {"none", "HS256", "HS384", "HS512"}
    assert isinstance(algs["none"], alg_mod.NoneAlgorithm)
    assert isinstance(algs["HS256"], alg_mod.HMACAlgorithm)
    assert isinstance(algs["HS384"], alg_mod.HMACAlgorithm)
    assert isinstance(algs["HS512"], alg_mod.HMACAlgorithm)


# curto: caminho com crypto backend; verifica presença de entradas adicionais e tipos
def test_get_default_algorithms_with_crypto_contains_expected_types(monkeypatch):
    monkeypatch.setattr(alg_mod, "has_crypto", True)
    algs = get_default_algorithms()

    # Verifica a presença de entradas de alto nível e seus tipos
    assert "EdDSA" in algs
    assert isinstance(algs["EdDSA"], alg_mod.OKPAlgorithm)

    assert "RS256" in algs and isinstance(algs["RS256"], alg_mod.RSAAlgorithm)
    assert "PS256" in algs and isinstance(algs["PS256"], alg_mod.RSAPSSAlgorithm)
    assert "ES256" in algs and isinstance(algs["ES256"], alg_mod.ECAlgorithm)
