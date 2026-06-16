import pytest
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.ec import SECP256R1
from repositorios.pyjwt.jwt.algorithms import ECAlgorithm

# Verifica inicialização correta com hash_alg e curva padrão (None)
def test_init_sets_hash_alg_and_default_curve():
    alg = ECAlgorithm(hash_alg=hashes.SHA256)
    assert alg.hash_alg is hashes.SHA256
    assert alg.expected_curve is None

# Verifica inicialização correta com hash_alg e curva esperada fornecida
def test_init_sets_hash_alg_and_expected_curve():
    alg = ECAlgorithm(hash_alg=hashes.SHA384, expected_curve=SECP256R1)
    assert alg.hash_alg is hashes.SHA384
    assert alg.expected_curve is SECP256R1
