from unittest.mock import Mock
from repositorios.pyjwt.jwt.api_jws import PyJWS

def _make_instance():
    inst = object.__new__(PyJWS)
    inst._validate_kid = Mock()
    inst._validate_crit = Mock()
    return inst

# verifica que _validate_kid é chamado quando 'kid' está presente (caso feliz)
def test_validate_headers_calls_kid_when_kid_present():
    inst = _make_instance()
    PyJWS._validate_headers(inst, {"kid": "abc"})
    inst._validate_kid.assert_called_once_with("abc")
    assert inst._validate_crit.call_count == 0

# verifica que _validate_crit é chamado quando 'crit' está presente e encoding é False
def test_validate_headers_calls_crit_when_crit_present_and_not_encoding():
    inst = _make_instance()
    header = {"crit": {"exp": 1}}
    PyJWS._validate_headers(inst, header, encoding=False)
    inst._validate_crit.assert_called_once_with(header)
    assert inst._validate_kid.call_count == 0

# verifica que ambas as validações são chamadas quando ambas as chaves estão presentes
def test_validate_headers_calls_both_when_both_keys_present():
    inst = _make_instance()
    PyJWS._validate_headers(inst, {"kid": "kid1", "crit": {"exp": 1}})
    inst._validate_kid.assert_called_once_with("kid1")
    inst._validate_crit.assert_called_once_with({"kid": "kid1", "crit": {"exp": 1}})

# verifica que _validate_crit não é chamado quando encoding=True
def test_validate_headers_does_not_call_crit_when_encoding_true():
    inst = _make_instance()
    PyJWS._validate_headers(inst, {"crit": {"exp": 1}}, encoding=True)
    inst._validate_crit.assert_not_called()
    assert inst._validate_kid.call_count == 0
