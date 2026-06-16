import pytest
from repositorios.pyjwt.jwt.api_jwk import PyJWK
from repositorios.pyjwt.jwt.exceptions import InvalidAlgorithmError
from repositorios.pyjwt.jwt.api_jws import PyJWS

# Test 1: missing Alg in header should raise InvalidAlgorithmError
def test__verify_signature_missing_alg_raises_InvalidAlgorithmError():
    class DummySelf:
        def __init__(self):
            self.options = {}

    dummy = DummySelf()
    header = {}  # missing 'alg'
    with pytest.raises(InvalidAlgorithmError):
        PyJWS._verify_signature(
            dummy,
            signing_input=b"input",
            header=header,
            signature=b"sig",
            key="key",
            algorithms=None,
            options=None,
        )

# Test 2: alg not in allowed list should raise InvalidAlgorithmError
def test__verify_signature_alg_not_allowed_raises_InvalidAlgorithmError():
    class DummySelf:
        def __init__(self):
            self.options = {}

    dummy = DummySelf()
    header = {"alg": "HS256"}
    with pytest.raises(InvalidAlgorithmError):
        PyJWS._verify_signature(
            dummy,
            signing_input=b"input",
            header=header,
            signature=b"sig",
            key="key",
            algorithms=["RS256"],
            options=None,
        )

# Test 3: PyJWK path with mismatching header alg vs key alg should raise InvalidAlgorithmError
def test__verify_signature_pyjwk_mismatch_algorithm_raises_InvalidAlgorithmError():
    class FakePyJWK(PyJWK):
        def __init__(self):
            pass  # bypass base init

    class SimpleAlg:
        def __init__(self):
            pass
        def check_key_length(self, key):
            return None
        def verify(self, signing_input, key, signature):
            return True

    fake_key = FakePyJWK()
    fake_key.algorithm_name = "RS256"
    fake_key.Algorithm = SimpleAlg()
    fake_key.key = b"pubkey"

    dummy = type("S", (), {"options": {}})()

    header = {"alg": "HS256"}  # different from fake_key.algorithm_name
    with pytest.raises(InvalidAlgorithmError):
        PyJWS._verify_signature(
            dummy,
            signing_input=b"input",
            header=header,
            signature=b"sig",
            key=fake_key,
            algorithms=None,
            options=None,
        )

# Test 4: Non-PyJWK path where get_algorithm_by_name raises NotImplementedError -> InvalidAlgorithmError
def test__verify_signature_get_algorithm_by_name_not_implemented_raises_InvalidAlgorithmError():
    class DummyPyJWSNotImpl(PyJWS):
        def __init__(self):
            self.options = {}
        def get_algorithm_by_name(self, alg):
            raise NotImplementedError

    dummy = DummyPyJWSNotImpl()
    header = {"alg": "RS256"}
    with pytest.raises(InvalidAlgorithmError):
        PyJWS._verify_signature(
            dummy,
            signing_input=b"input",
            header=header,
            signature=b"sig",
            key="key",
            algorithms=None,
            options=None,
        )
