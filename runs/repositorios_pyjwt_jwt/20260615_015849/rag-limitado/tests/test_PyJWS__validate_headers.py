from repositorios.pyjwt.jwt.api_jws import PyJWS

class DummyPyJWS(PyJWS):
    def __init__(self):
        pass

    def _validate_kid(self, kid):
        self.kid = kid
        self.kid_called = True

    def _validate_crit(self, headers):
        self.crit_headers = headers
        self.crit_called = True

# Verifica path feliz: presence of 'kid' chama _validate_kid
def test_validate_headers_calls_kid_when_kid_present():
    # curto: happy path for kid
    inst = DummyPyJWS()
    headers = {"kid": "abc123"}
    inst._validate_headers(headers, encoding=False)
    assert getattr(inst, "kid_called", False) is True
    assert inst.kid == "abc123"

# Verifica exceção de branch: quando 'crit' presente, encoding=False chama _validate_crit
def test_validate_headers_calls_crit_when_crit_present_and_not_encoding():
    # curto: branch crit com encoding False
    inst = DummyPyJWS()
    headers = {"kid": "kid1", "crit": ["a", "b"]}
    inst._validate_headers(headers, encoding=False)
    assert getattr(inst, "crit_called", False) is True
    assert inst.crit_headers is headers

# Verifica branch de borda: quando encoding=True, mesmo com 'crit', não chama _validate_crit
def test_validate_headers_does_not_call_crit_when_encoding_true():
    # borda: encoding True evita crit
    inst = DummyPyJWS()
    headers = {"crit": ["a", "b"]}
    inst._validate_headers(headers, encoding=True)
    assert getattr(inst, "crit_called", False) is False

# Verifica caminho principal com ambos headers presentes
def test_validate_headers_calls_both_kid_and_crit_when_both_present_and_not_encoding():
    # cabo: ambos presentes, encoding False
    inst = DummyPyJWS()
    headers = {"kid": "kid1", "crit": ["c"]}
    inst._validate_headers(headers, encoding=False)
    assert inst.kid_called is True
    assert inst.crit_called is True
    assert inst.kid == "kid1"
    assert inst.crit_headers == headers
