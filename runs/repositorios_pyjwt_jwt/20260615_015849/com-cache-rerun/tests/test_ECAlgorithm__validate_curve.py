import pytest
from cryptography.hazmat.primitives.asymmetric.ec import SECP256R1, SECP384R1
from repositorios.pyjwt.jwt.exceptions import InvalidKeyError
from repositorios.pyjwt.jwt.algorithms import ECAlgorithm

# small helper to avoid importing the full implementation details
class DummyECAlgorithm(ECAlgorithm):
    def __init__(self, expected_curve):
        self.expected_curve = expected_curve

def _build_key(curve):
    class DummyKey:
        def __init__(self, curve):
            self.curve = curve
    return DummyKey(curve)

# short: happy path when no expected_curve is defined
def test_validate_curve_no_expected_curve_no_error():
    alg = DummyECAlgorithm(expected_curve=None)
    key = _build_key(SECP256R1())
    alg._validate_curve(key)

# short: mismatch between key curve and expected_curve raises InvalidKeyError
def test_validate_curve_mismatch_raises_InvalidKeyError():
    alg = DummyECAlgorithm(expected_curve=SECP256R1)
    key = _build_key(SECP384R1())
    with pytest.raises(InvalidKeyError):
        alg._validate_curve(key)

# short: matching curve does not raise
def test_validate_curve_match_no_error():
    alg = DummyECAlgorithm(expected_curve=SECP256R1)
    key = _build_key(SECP256R1())
    alg._validate_curve(key)
