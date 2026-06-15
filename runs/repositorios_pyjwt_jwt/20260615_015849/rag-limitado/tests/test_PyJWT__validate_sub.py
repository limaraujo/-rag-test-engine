import pytest
from repositorios.pyjwt.jwt.exceptions import InvalidSubjectError
from repositorios.pyjwt.jwt.api_jwt import PyJWT

def _get_pyjwt_instance():
    cls = PyJWT
    try:
        return cls()
    except Exception:
        return cls.__new__(cls)

# short: happy path - não há "sub" no payload
def test_validate_sub_missing_sub_no_exception():
    pyjwt = _get_pyjwt_instance()
    payload = {"iss": "example"}
    pyjwt._validate_sub(payload)

# short: exceção para tipo de sub inválido (não string)
def test_validate_sub_sub_not_string_raises():
    pyjwt = _get_pyjwt_instance()
    payload = {"sub": 123}
    with pytest.raises(InvalidSubjectError, match="Subject must be a string"):
        pyjwt._validate_sub(payload)

# short: branch de subject fornecido que não confere com payload
def test_validate_sub_subject_mismatch_raises():
    pyjwt = _get_pyjwt_instance()
    payload = {"sub": "user123"}
    with pytest.raises(InvalidSubjectError, match="Invalid subject"):
        pyjwt._validate_sub(payload, subject="different")

# short: branch de subject fornecido que confere com payload
def test_validate_sub_subject_match_no_exception():
    pyjwt = _get_pyjwt_instance()
    payload = {"sub": "user123"}
    pyjwt._validate_sub(payload, subject="user123")
