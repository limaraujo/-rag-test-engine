from repositorios.pyjwt.jwt import algorithms as alg
from cryptography.exceptions import InvalidSignature
from repositorios.pyjwt.jwt.algorithms import ECAlgorithm

# Helper to construct an ECAlgorithm instance without calling __init__
def _make_instance():
    inst = object.__new__(alg.ECAlgorithm)
    inst.hash_alg = lambda: "hash"
    return inst

# Verifica: valida input inválido levanta ValueError em raw_to_der_signature -> False
def test_verify_invalid_input_false(monkeypatch):
    class DummyKey:
        curve = "curve"

    def _raise(sig, curve):
        raise ValueError()

    monkeypatch.setattr(alg, "raw_to_der_signature", _raise)
    inst = _make_instance()
    key = DummyKey()
    assert inst.verify(b"msg", key, b"sig") is False

# Verifica: caminho com chave pública válida (happy path) -> True
def test_verify_public_key_path_true(monkeypatch):
    class DummyPublicKey:
        curve = "curve"
        def verify(self, der_sig, msg, algo):
            return None

    monkeypatch.setattr(alg, "raw_to_der_signature", lambda sig, curve: b"der")
    monkeypatch.setattr(alg, "ECDSA", lambda algo: "ECDSA")
    key = DummyPublicKey()
    inst = _make_instance()
    assert inst.verify(b"msg", key, b"sig") is True

# Verifica: caminho com chave pública que lança InvalidSignature -> False
def test_verify_public_key_path_invalid_signature(monkeypatch):
    class DummyPublicKey:
        curve = "curve"
        def verify(self, der_sig, msg, algo):
            raise InvalidSignature()

    monkeypatch.setattr(alg, "raw_to_der_signature", lambda sig, curve: b"der")
    monkeypatch.setattr(alg, "ECDSA", lambda algo: "ECDSA")
    key = DummyPublicKey()
    inst = _make_instance()
    assert inst.verify(b"msg", key, b"sig") is False

# Verifica: branch de PrivateKey onde é obtido o public_key -> True
def test_verify_private_key_path_true(monkeypatch):
    class DummyBase:
        pass
    monkeypatch.setattr(alg, "EllipticCurvePrivateKey", DummyBase)

    class DummyPublicKey:
        curve = "curve"
        def verify(self, der_sig, msg, algo):
            return None

    class DummyPrivateKey(DummyBase):
        def __init__(self, curve, pub):
            self.curve = curve
            self._pub = pub
        def public_key(self):
            return self._pub

    pub = DummyPublicKey()
    priv = DummyPrivateKey("curve", pub)

    monkeypatch.setattr(alg, "raw_to_der_signature", lambda sig, curve: b"der")
    monkeypatch.setattr(alg, "ECDSA", lambda algo: "ECDSA")

    inst = _make_instance()
    assert inst.verify(b"msg", priv, b"sig") is True
