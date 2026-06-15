from unittest import mock
from repositorios.pyjwt.jwt.api_jws import PyJWS


def _make_instance():
    return object.__new__(PyJWS)


# verifica que _validate_kid é chamado quando 'kid' presente (caminho feliz)
def test_validate_headers_calls_validate_kid_when_kid_present():
    inst = _make_instance()
    kid_mock = mock.Mock()
    crit_mock = mock.Mock()
    with mock.patch.object(PyJWS, "_validate_kid", kid_mock), mock.patch.object(PyJWS, "_validate_crit", crit_mock):
        PyJWS._validate_headers(inst, {"kid": "abc"})
    assert kid_mock.call_args[0][0] == "abc"
    crit_mock.assert_not_called()


# verifica que _validate_kid e _validate_crit são chamadas quando ambos presentes (encoding padrão)
def test_validate_headers_calls_both_when_keys_present_and_encoding_false():
    inst = _make_instance()
    kid_mock = mock.Mock()
    crit_mock = mock.Mock()
    header = {"kid": "k", "crit": {"crit": True}}
    with mock.patch.object(PyJWS, "_validate_kid", kid_mock), mock.patch.object(PyJWS, "_validate_crit", crit_mock):
        PyJWS._validate_headers(inst, header)
    assert kid_mock.call_args[0][0] == "k"
    assert crit_mock.call_args[0][0] == header


# verifica que _validate_crit não é chamado quando encoding=True (caso de bordo)
def test_validate_headers_crit_not_called_when_encoding_true():
    inst = _make_instance()
    kid_mock = mock.Mock()
    crit_mock = mock.Mock()
    header = {"kid": "x", "crit": {"ignored": True}}
    with mock.patch.object(PyJWS, "_validate_kid", kid_mock), mock.patch.object(PyJWS, "_validate_crit", crit_mock):
        PyJWS._validate_headers(inst, header, encoding=True)
    kid_mock.assert_called()
    crit_mock.assert_not_called()


# verifica que nenhum callback é chamado quando não há chaves relevantes (caminho sem keys)
def test_validate_headers_no_keys_calls_none():
    inst = _make_instance()
    kid_mock = mock.Mock()
    crit_mock = mock.Mock()
    header = {"typ": "JWT"}
    with mock.patch.object(PyJWS, "_validate_kid", kid_mock), mock.patch.object(PyJWS, "_validate_crit", crit_mock):
        PyJWS._validate_headers(inst, header)
    kid_mock.assert_not_called()
    crit_mock.assert_not_called()
