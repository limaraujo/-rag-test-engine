import pytest
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.ec import SECP256K1, SECP384R1, SECP521R1
from repositorios.pyjwt.jwt.algorithms import ECAlgorithm

import pytest

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.ec import SECP256K1, SECP384R1, SECP521R1
from repositorios.pyjwt.jwt.algorithms import ECAlgorithm

# happy path: verify attributes are stored for several valid hash/curve combos
@pytest.mark.parametrize(
    "hash_alg, expected_curve",
    [
        (hashes.SHA256, SECP256K1),
        (hashes.SHA384, SECP384R1),
        (hashes.SHA512, SECP521R1),
    ],
)
def test_ec_algorithm_init_stores_args(hash_alg, expected_curve):
    alg = ECAlgorithm(hash_alg=hash_alg, expected_curve=expected_curve)
    assert alg.hash_alg is hash_alg
    assert alg.expected_curve is expected_curve

# default: when expected_curve is omitted, ECAlgorithm stores None
def test_ec_algorithm_init_defaults_expected_curve_to_none():
    alg = ECAlgorithm(hash_alg=hashes.SHA256)
    assert alg.hash_alg is hashes.SHA256
    assert alg.expected_curve is None
