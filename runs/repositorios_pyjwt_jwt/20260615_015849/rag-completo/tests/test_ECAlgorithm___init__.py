from repositorios.pyjwt.jwt.algorithms import ECAlgorithm

def test_init_explicit_values_stores_hash_and_curve():
    # short: happy path - explicit hash_alg and expected_curve are stored
    hash_alg = object()
    expected_curve = type('DummyCurve', (), {})  # dummy curve type
    inst = object.__new__(ECAlgorithm)
    ECAlgorithm.__init__(inst, hash_alg, expected_curve)
    assert inst.hash_alg is hash_alg
    assert inst.expected_curve is expected_curve

def test_init_defaults_expected_curve_none_when_not_provided():
    # short: default path - expected_curve defaults to None
    hash_alg = object()
    inst = object.__new__(ECAlgorithm)
    ECAlgorithm.__init__(inst, hash_alg)
    assert inst.hash_alg is hash_alg
    assert inst.expected_curve is None
