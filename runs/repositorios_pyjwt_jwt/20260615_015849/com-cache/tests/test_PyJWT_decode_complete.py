from unittest.mock import patch
import pytest
from repositorios.pyjwt.jwt.api_jwt import PyJWT

class FakeJWS:
    def decode_complete(self, jwt_token, key=None, algorithms=None, options=None, detached_payload=None):
        return {"header": {"alg": "HS256"}, "signature": "sig"}

def test_decode_complete_happy_path():
    pyjwt = PyJWT()
    pyjwt._jws = FakeJWS()
    with patch.object(pyjwt, "_decode_payload", return_value={"sub": "user"}) as mock_decode_payload, \
         patch.object(pyjwt, "_validate_claims") as mock_validate_claims, \
         patch.object(pyjwt, "_merge_options", return_value={}) as mock_merge_options:
        result = pyjwt.decode_complete("dummy_token", key="secret", algorithms=["HS256"])
        assert result["header"] == {"alg": "HS256"}
        assert result["signature"] == "sig"
        assert result["payload"] == {"sub": "user"}
        mock_decode_payload.assert_called_once()
        mock_validate_claims.assert_called_once()
        mock_merge_options.assert_called_once()

def test_decode_complete_warn_on_verify_mismatch():
    pyjwt = PyJWT()
    pyjwt._jws = FakeJWS()
    with patch.object(pyjwt, "_decode_payload", return_value={"sub": "user"}), \
         patch.object(pyjwt, "_validate_claims"), \
         patch.object(pyjwt, "_merge_options", return_value={}):

        with pytest.warns(DeprecationWarning):
            result = pyjwt.decode_complete("dummy_token", key="secret", algorithms=["HS256"], verify=False)
        assert result["header"] == {"alg": "HS256"}
        assert result["payload"] == {"sub": "user"}

def test_decode_complete_warn_on_extra_kwargs():
    pyjwt = PyJWT()
    pyjwt._jws = FakeJWS()
    with patch.object(pyjwt, "_decode_payload", return_value={"sub": "user"}), \
         patch.object(pyjwt, "_validate_claims"), \
         patch.object(pyjwt, "_merge_options", return_value={}):
        with pytest.warns(Warning):
            result = pyjwt.decode_complete("dummy_token", key="secret", algorithms=["HS256"], extra="value")
        assert result["header"] == {"alg": "HS256"}
        assert result["payload"] == {"sub": "user"}
