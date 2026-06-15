from repositorios.pyjwt.jwt.exceptions import InvalidSubjectError
import pytest
from repositorios.pyjwt.jwt.api_jwt import PyJWT

# Verifica caminho: quando não há chave "sub" no payload, não houve erro (happy path)
def test_validate_sub_no_sub_key_no_exception():
    jwt = PyJWT()
    payload = {"foo": "bar"}
    jwt._validate_sub(payload, subject=None)

# Verifica exceção: "sub" presente mas não é string
def test_validate_sub_sub_not_string_raises():
    jwt = PyJWT()
    payload = {"sub": 123}
    with pytest.raises(InvalidSubjectError):
        jwt._validate_sub(payload, subject=None)

# Verifica caminho: "sub" é string e igual ao subject fornecido (caminho feliz com subject fornecido)
def test_validate_sub_sub_matches_subject_provided():
    jwt = PyJWT()
    payload = {"sub": "alice"}
    jwt._validate_sub(payload, subject="alice")

# Verifica exceção: "sub" é string, mas difere do subject fornecido
def test_validate_sub_sub_mismatch_with_provided_subject_raises():
    jwt = PyJWT()
    payload = {"sub": "alice"}
    with pytest.raises(InvalidSubjectError):
        jwt._validate_sub(payload, subject="bob")
