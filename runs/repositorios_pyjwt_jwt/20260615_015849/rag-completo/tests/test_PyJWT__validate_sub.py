import pytest
from repositorios.pyjwt.jwt.exceptions import InvalidSubjectError
from repositorios.pyjwt.jwt.api_jwt import PyJWT


# happy path: payload sem 'sub' deve retornar sem erro
def test_validate_sub_absent_no_exception():
    payload = {"iss": "issuer"}
    pyjwt = PyJWT.__new__(PyJWT)
    pyjwt._validate_sub(payload)


# exceção: 'sub' não é string levanta InvalidSubjectError
def test_validate_sub_sub_not_string_raises():
    payload = {"sub": 123}
    pyjwt = PyJWT.__new__(PyJWT)
    with pytest.raises(InvalidSubjectError) as exc:
        pyjwt._validate_sub(payload)
    assert "Subject must be a string" in str(exc.value)


# happy path: 'sub' é string e o subject coincide: não levanta
def test_validate_sub_matches_with_subject_passes():
    payload = {"sub": "alice"}
    pyjwt = PyJWT.__new__(PyJWT)
    pyjwt._validate_sub(payload, subject="alice")


# exceção: 'sub' é string mas não coincide com subject fornecido: levanta InvalidSubjectError
def test_validate_sub_mismatch_with_subject_raises():
    payload = {"sub": "alice"}
    pyjwt = PyJWT.__new__(PyJWT)
    with pytest.raises(InvalidSubjectError) as exc:
        pyjwt._validate_sub(payload, subject="bob")
    assert "Invalid subject" in str(exc.value)
