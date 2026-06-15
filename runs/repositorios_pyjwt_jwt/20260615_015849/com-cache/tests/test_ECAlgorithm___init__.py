import pytest
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from repositorios.pyjwt.jwt.algorithms import ECAlgorithm

# happy path: verify that provided hash algorithm and curve are stored on the instance
@pytest.mark.parametrize("hash_alg, expected_curve", [
    (hashes.SHA256, ec.SECP256R1),
    (hashes.SHA512, ec.SECP384R1),
])
def test_ec_algorithm_init_sets_hash_and_curve(hash_alg, expected_curve):
    alg = ECAlgorithm(hash_alg=hash_alg, expected_curve=expected_curve)
    assert alg.hash_alg is hash_alg
    assert alg.expected_curve is expected_curve

# edge case: when expected_curve is omitted, it should default to None
def test_ec_algorithm_init_defaults_expected_curve_none():
    alg = ECAlgorithm(hash_alg=hashes.SHA256)
    assert alg.hash_alg is hashes.SHA256
    assert alg.expected_curve is None
