from datetime import timedelta
import pytest
from unittest.mock import MagicMock
from repositorios.pyjwt.jwt.api_jwt import PyJWT
from datetime import timedelta as _td

from datetime import timedelta
import pytest
from unittest.mock import MagicMock
from repositorios.pyjwt.jwt.api_jwt import PyJWT


# short: happy path - all claims present and all verifications enabled
def test_happy_path_calls_all_validators_when_claims_present_and_flags_true():
    # arrange
    cls = PyJWT
    inst = object.__new__(cls)

    inst._validate_required_claims = MagicMock()
    inst._validate_iat = MagicMock()
    inst._validate_nbf = MagicMock()
    inst._validate_exp = MagicMock()
    inst._validate_iss = MagicMock()
    inst._validate_aud = MagicMock()
    inst._validate_sub = MagicMock()
    inst._validate_jti = MagicMock()

    payload = {
        "iat": 0,
        "nbf": 0,
        "exp": 9999999999,
        "iss": "issuer",
        "aud": "audience",
        "sub": "subject",
        "jti": "jwt-id",
    }

    options = {
        "require": [],
        "verify_iat": True,
        "verify_nbf": True,
        "verify_exp": True,
        "verify_iss": True,
        "verify_aud": True,
        "verify_sub": True,
        "verify_jti": True,
        "strict_aud": False,
        "enforce_minimum_key_length": False,
        "verify_signature": True,
    }

    # act
    inst._validate_claims(payload, options, audience="audience", issuer="issuer", subject="subject", leeway=0)

    # assert
    assert inst._validate_required_claims.called
    assert inst._validate_iat.called
    assert inst._validate_nbf.called
    assert inst._validate_exp.called
    assert inst._validate_iss.called
    assert inst._validate_aud.called
    assert inst._validate_sub.called
    assert inst._validate_jti.called

# short: invalid audience type should raise TypeError
def test_invalid_audience_type_raises_type_error():
    cls = PyJWT
    inst = object.__new__(cls)

    inst._validate_required_claims = MagicMock()
    inst._validate_iat = MagicMock()
    inst._validate_nbf = MagicMock()
    inst._validate_exp = MagicMock()
    inst._validate_iss = MagicMock()
    inst._validate_aud = MagicMock()
    inst._validate_sub = MagicMock()
    inst._validate_jti = MagicMock()

    payload = {"iat": 0}
    options = {
        "require": [],
        "verify_iat": True,
        "verify_nbf": False,
        "verify_exp": False,
        "verify_iss": False,
        "verify_aud": False,
        "verify_sub": False,
        "verify_jti": False,
        "strict_aud": False,
        "enforce_minimum_key_length": False,
    }

    with pytest.raises(TypeError):
        inst._validate_claims(payload, options, audience=123)

# short: exp not present but verify_exp is True should not call _validate_exp
def test_no_exp_called_when_exp_missing():
    cls = PyJWT
    inst = object.__new__(cls)

    inst._validate_required_claims = MagicMock()
    inst._validate_iat = MagicMock()
    inst._validate_nbf = MagicMock()
    inst._validate_exp = MagicMock()
    inst._validate_iss = MagicMock()
    inst._validate_aud = MagicMock()
    inst._validate_sub = MagicMock()
    inst._validate_jti = MagicMock()

    payload = {"iat": 0}  # no 'exp'
    options = {
        "require": [],
        "verify_iat": True,
        "verify_nbf": False,
        "verify_exp": True,  # should be ignored since 'exp' not present
        "verify_iss": False,
        "verify_aud": False,
        "verify_sub": False,
        "verify_jti": False,
        "strict_aud": False,
        "enforce_minimum_key_length": False,
    }

    inst._validate_claims(payload, options, audience=None, issuer=None, subject=None, leeway=0)

    assert inst._validate_exp.call_count == 0

# short: timedelta leeway should be converted and passed to iat
def test_leeway_timedelta_converted_and_passed_to_iat():
    cls = PyJWT
    inst = object.__new__(cls)

    inst._validate_required_claims = MagicMock()
    inst._validate_iat = MagicMock()
    inst._validate_nbf = MagicMock()
    inst._validate_exp = MagicMock()
    inst._validate_iss = MagicMock()
    inst._validate_aud = MagicMock()
    inst._validate_sub = MagicMock()
    inst._validate_jti = MagicMock()

    payload = {"iat": 0}
    options = {
        "require": [],
        "verify_iat": True,
        "verify_nbf": False,
        "verify_exp": False,
        "verify_iss": False,
        "verify_aud": False,
        "verify_sub": False,
        "verify_jti": False,
        "strict_aud": False,
        "enforce_minimum_key_length": False,
    }

    from datetime import timedelta as _td
    leeway = _td(seconds=5)

    inst._validate_claims(payload, options, audience=None, issuer=None, subject=None, leeway=leeway)

    # iat was called and leeway should be 5.0
    assert inst._validate_iat.called
    call_args = inst._validate_iat.call_args
    assert call_args is not None
    assert len(call_args[0]) >= 3
    assert isinstance(call_args[0][1], float)
    assert call_args[0][2] == 5.0
