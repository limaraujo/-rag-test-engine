from unittest.mock import MagicMock
from repositorios.pyjwt.jwt.api_jws import PyJWS

class DummyPyJWS(PyJWS):
    def __init__(self):
        pass

# curto: verifica que o branch que valida 'kid' é chamado com o valor correto
def test_validate_headers_calls_kid_when_present():
    obj = DummyPyJWS()
    obj._validate_kid = MagicMock()
    obj._validate_crit = MagicMock()
    headers = {"kid": "my-key-id"}
    obj._validate_headers(headers)
    obj._validate_kid.assert_called_once_with("my-key-id")
    obj._validate_crit.assert_not_called()

# curto: verifica que 'crit' é validado quando presente e encoding é False
def test_validate_headers_calls_validate_crit_when_present_and_encoding_false():
    obj = DummyPyJWS()
    obj._validate_kid = MagicMock()
    obj._validate_crit = MagicMock()
    headers = {"crit": ["some", "entries"]}
    obj._validate_headers(headers)
    obj._validate_kid.assert_not_called()
    obj._validate_crit.assert_called_once_with(headers)

# curto: verifica que, quando encoding=True, 'crit' não é validado
def test_validate_headers_does_not_call_crit_when_encoding_true():
    obj = DummyPyJWS()
    obj._validate_kid = MagicMock()
    obj._validate_crit = MagicMock()
    headers = {"crit": ["not", "validated"]}
    obj._validate_headers(headers, encoding=True)
    obj._validate_kid.assert_not_called()
    obj._validate_crit.assert_not_called()

# curto: verifica que nada é chamado quando nenhum header relevante está presente
def test_validate_headers_no_effect_when_header_absent():
    obj = DummyPyJWS()
    obj._validate_kid = MagicMock()
    obj._validate_crit = MagicMock()
    headers = {"foo": "bar"}
    obj._validate_headers(headers)
    obj._validate_kid.assert_not_called()
    obj._validate_crit.assert_not_called()
