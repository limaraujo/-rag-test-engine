import pytest
from repositorios.pyjwt.jwt.api_jws import PyJWS

# curto: happy path - default behavior when no algorithms whitelist is provided

# curto: branch - whitelist a single algorithm reduces available algorithms to that one
def test_init_whitelist_limits_algorithms():
    jw_default = PyJWS()
    default_keys = list(jw_default._algorithms.keys())
    assert len(default_keys) > 0
    one = default_keys[0]
    jw = PyJWS(algorithms=[one])
    assert set(jw._algorithms.keys()) == {one}
    assert jw._valid_algs == {one}

# curto: merging options - provided options should be merged into default options
def test_init_merges_custom_options():
    jw = PyJWS(options={'dummy_key': 'value', 'another': 123})
    assert isinstance(jw.options, dict)
    assert jw.options.get('dummy_key') == 'value'
    # ensure no crash and defaults still present (at least some key exists)
    assert len(jw.options) >= 1
