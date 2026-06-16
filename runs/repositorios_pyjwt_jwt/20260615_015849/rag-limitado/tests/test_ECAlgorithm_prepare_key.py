import pytest
from types import SimpleNamespace
from repositorios.pyjwt.jwt.algorithms import ECAlgorithm
import repositorios.pyjwt.jwt.algorithms as alg

import pytest
from types import SimpleNamespace
from repositorios.pyjwt.jwt.algorithms import ECAlgorithm

# short: happy path for when input is already a recognized EC key type
def test_prepare_key_accepts_existing_crypto_key_type():
    class DummyKey:
        pass

    fake = SimpleNamespace()
    fake._crypto_key_types = (DummyKey,)
    validated = {"called": False, "arg": None}

    def _validate_curve(key):
        validated["called"] = True
        validated["arg"] = key

    fake._validate_curve = _validate_curve
    fake.check_crypto_key_type = lambda k: None

    key = DummyKey()
    res = ECAlgorithm.prepare_key(fake, key)

    assert res is key
    assert validated["called"] is True
    assert validated["arg"] is key

# short: ensures TypeError is raised for input types that are not PEM-formatted keys
def test_prepare_key_invalid_input_type_raises():
    class DummyKey:
        pass

    fake = SimpleNamespace()
    fake._crypto_key_types = (DummyKey,)
    fake.check_crypto_key_type = lambda k: None

    with pytest.raises(TypeError):
        ECAlgorithm.prepare_key(fake, 123)

# short: loading and validating a PEM-formatted public key path
def test_prepare_key_loads_public_pem_key(monkeypatch):
    class DummyPublicKey:
        pass

    key_bytes = b"not-ssh-or-ecdsa"

    fake = SimpleNamespace()
    fake._crypto_key_types = ()  # no first-branch match
    captured = {"checked": False, "validated": False}

    def check_crypto_type(k):
        captured["checked"] = True
        assert k is DummyPublicKey

    fake.check_crypto_key_type = check_crypto_type

    def _validate_curve(k):
        captured["validated"] = True
        assert k is DummyPublicKey

    fake._validate_curve = _validate_curve

    import repositorios.pyjwt.jwt.algorithms as alg

    def fake_load_pem_public_key(data):
        assert data == key_bytes
        return DummyPublicKey

    monkeypatch.setattr(alg, "load_pem_public_key", fake_load_pem_public_key)
    monkeypatch.setattr(alg, "force_bytes", lambda k: k)

    res = ECAlgorithm.prepare_key(fake, key_bytes)

    assert res is DummyPublicKey
    assert captured["checked"] is True
    assert captured["validated"] is True
