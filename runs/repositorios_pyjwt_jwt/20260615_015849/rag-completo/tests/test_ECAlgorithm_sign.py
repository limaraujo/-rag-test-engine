import importlib
import types
import pytest
from repositorios.pyjwt.jwt.algorithms import ECAlgorithm

import importlib
import types

import pytest
from repositorios.pyjwt.jwt.algorithms import ECAlgorithm

module = importlib.import_module("repositorios.pyjwt.jwt.algorithms")


# curto: verifica caminho feliz do sign: usa ECDSA(hash) e der_to_raw_signature
def test_ec_algorithm_sign_uses_ecdsa_and_der_to_raw_signature(monkeypatch):
    last_der_sig = {}

    class DummyECDSA:
        def __init__(self, algorithm):
            self.algorithm = algorithm

    # Patch ECDSA used inside ECAlgorithm.sign
    monkeypatch.setattr(module, "ECDSA", DummyECDSA)

    # Patch der_to_raw_signature to capture der_sig and return a sentinel
    def dummy_der_to_raw_signature(der_sig, curve):
        last_der_sig["value"] = der_sig
        return b"RAW_SIG"

    monkeypatch.setattr(module, "der_to_raw_signature", dummy_der_to_raw_signature)

    # Simple dummy key with a curve attribute; its sign method returns a fixed DER sig
    class DummyKey:
        def __init__(self, curve=None):
            self.curve = curve
            self.sign_calls = []

        def sign(self, msg, algo):
            self.sign_calls.append((msg, algo))
            return b"DER_SIG"

    dummy_key = DummyKey(curve="CURVE1")

    # Instantiate ECAlgorithm without calling __init__ to avoid constructor requirements
    algo = object.__new__(module.ECAlgorithm)

    # Bind a concrete hash_alg() returning a sentinel to the instance
    def hash_alg(self):
        return "HASH_ALG"

    algo.hash_alg = types.MethodType(hash_alg, algo)

    msg = b"hello world"
    result = algo.sign(msg, dummy_key)

    assert result == b"RAW_SIG"
    assert last_der_sig["value"] == b"DER_SIG"

    # Ensure the key.sign was called with the message and a DummyECDSA instance carrying the hash
    assert len(dummy_key.sign_calls) == 1
    called_msg, called_algo = dummy_key.sign_calls[0]
    assert called_msg == msg
    assert isinstance(called_algo, DummyECDSA)
    assert called_algo.algorithm == "HASH_ALG"
