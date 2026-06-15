from repositorios.pyjwt.jwt.algorithms import get_default_algorithms
from repositorios.pyjwt.jwt.api_jws import PyJWS


# curto
def test_init_defaults_preserves_all_algorithms():
    # happy path: default constructor should keep all default algorithms
    default_algos = set(get_default_algorithms().keys())
    ws = PyJWS()
    assert set(ws._algorithms.keys()) == default_algos
    assert ws._valid_algs == default_algos


# curto
def test_init_whitelist_keeps_only_requested_algorithms():
    # branch: whitelist provided; keep only requested algorithms (or none if absent)
    default_algos = set(get_default_algorithms().keys())
    subset = ['HS256']
    ws = PyJWS(algorithms=subset)
    expected_keys = set(subset) & default_algos
    assert set(ws._algorithms.keys()) == (expected_keys)
    assert ws._valid_algs == set(subset)


# curto
def test_init_merges_options_with_custom_keys():
    # happy path: options merge should include provided keys
    ws = PyJWS(options={'custom_key': 'custom_value'})
    assert ws.options.get('custom_key') == 'custom_value'
