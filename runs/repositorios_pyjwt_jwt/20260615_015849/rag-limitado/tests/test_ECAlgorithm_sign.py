import importlib
import pytest
from repositorios.pyjwt.jwt.algorithms import ECAlgorithm

alg_module = importlib.import_module("repositorios.pyjwt.jwt.algorithms")
ECAlgorithm = alg_module.ECAlgorithm

class DummySelf:
    def hash_alg(self):
        return "HASH_ALG"

def test_ec_algorithm_sign_happy_path_calls_ecdsa_and_der_conversion(monkeypatch):
    # curto: happy path - verifies ECDSA arg, key.sign usage, and der_to_raw_signature flow
    captured = {}

    def fake_ECDSA(arg):
        captured["hash_alg"] = arg
        return object()

    def fake_der_to_raw_signature(der_sig, curve):
        captured["der_sig"] = der_sig
        captured["curve"] = curve
        return b"RAW_SIGNATURE"

    monkeypatch.setattr(alg_module, "ECDSA", fake_ECDSA)
    monkeypatch.setattr(alg_module, "der_to_raw_signature", fake_der_to_raw_signature)

    class DummyKey:
        curve = "CURVE"

        def __init__(self):
            self.sign_called = False
            self.last_args = None

        def sign(self, msg, algo):
            self.sign_called = True
            self.last_args = (msg, algo)
            return b"DER_SIG"

    key = DummyKey()

    sig = ECAlgorithm.sign(DummySelf(), b"MSG", key)

    assert key.sign_called
    assert key.last_args[0] == b"MSG"
    assert captured["der_sig"] == b"DER_SIG"
    assert captured["curve"] == key.curve
    assert sig == b"RAW_SIGNATURE"
    assert captured["hash_alg"] == "HASH_ALG"

def test_ec_algorithm_sign_with_message_and_curve_pass_through(monkeypatch):
    # curto: verifica que a mensagem é passada corretamente e o retorno vem do der_to_raw_signature
    captured = {}

    def fake_ECDSA(arg):
        captured["hash_alg"] = arg
        return object()

    def fake_der_to_raw_signature(der_sig, curve):
        captured["der_sig"] = der_sig
        captured["curve"] = curve
        return b"RAW"

    monkeypatch.setattr(alg_module, "ECDSA", fake_ECDSA)
    monkeypatch.setattr(alg_module, "der_to_raw_signature", fake_der_to_raw_signature)

    class DummyKey:
        curve = "MY_CURVE"

        def __init__(self):
            self.sign_called = False
            self.last_args = None

        def sign(self, msg, algo):
            self.sign_called = True
            self.last_args = (msg, algo)
            return b"DER_SIG_V2"

    key = DummyKey()

    sig = ECAlgorithm.sign(DummySelf(), b"ANOTHER_MSG", key)

    assert key.sign_called
    assert key.last_args[0] == b"ANOTHER_MSG"
    assert captured["der_sig"] == b"DER_SIG_V2"
    assert captured["curve"] == key.curve
    assert sig == b"RAW"
