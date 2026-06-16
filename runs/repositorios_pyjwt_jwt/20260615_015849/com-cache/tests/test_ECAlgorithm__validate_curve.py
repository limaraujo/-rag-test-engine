from repositorios.pyjwt.jwt.exceptions import InvalidKeyError
from cryptography.hazmat.primitives.asymmetric.ec import SECP256K1, SECP256R1
import pytest
from repositorios.pyjwt.jwt.algorithms import ECAlgorithm

class DummyKey:
    def __init__(self, curve):
        self.curve = curve

# curto: happy path when expected_curve is None => no exception
def test__validate_curve_no_expected_curve_allows_any_key():
    # Verifica caminho feliz: não há curva esperada, função não levanta
    alg = object.__new__(ECAlgorithm)
    alg.expected_curve = None
    key = DummyKey(SECP256K1())
    ECAlgorithm._validate_curve(alg, key)

# curto: exception raised when key.curve does not match expected_curve
def test__validate_curve_raises_on_mismatch():
    # Cenário: key.curve é SECP256K1, esperado SECP256R1
    alg = object.__new__(ECAlgorithm)
    alg.expected_curve = SECP256R1
    key = DummyKey(SECP256K1())
    with pytest.raises(InvalidKeyError) as exc:
        ECAlgorithm._validate_curve(alg, key)
    assert "The key's curve 'secp256k1' does not match the expected curve 'secp256r1' for this algorithm" in str(exc.value)

# curto: no exception when key.curve matches expected_curve
def test__validate_curve_passes_when_match():
    # Cenário: key.curve corresponde à curva esperada
    alg = object.__new__(ECAlgorithm)
    alg.expected_curve = SECP256R1
    key = DummyKey(SECP256R1())
    ECAlgorithm._validate_curve(alg, key)
