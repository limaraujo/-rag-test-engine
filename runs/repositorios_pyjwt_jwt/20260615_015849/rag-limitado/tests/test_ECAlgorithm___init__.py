import pytest
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.ec import SECP256R1
from repositorios.pyjwt.jwt.algorithms import ECAlgorithm

# verifica atribuição correta de hash_alg e expected_curve (cases: com curva e sem curva)
@pytest.mark.parametrize("hash_alg, expected_curve", [
    (hashes.SHA256, SECP256R1),
    (hashes.SHA512, None),
])
def test_ecalgorithm_init_assigns_fields(hash_alg, expected_curve):
    alg = ECAlgorithm(hash_alg=hash_alg, expected_curve=expected_curve)
    assert alg.hash_alg is hash_alg
    assert alg.expected_curve is expected_curve
