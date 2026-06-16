from repositorios.pyjwt.jwt.jwks_client import PyJWKClient

class _KeyStub:
    def __init__(self, kid: str):
        self.key_id = kid

# happy path: retorna a chave cujo key_id corresponde ao kid fornecido
def test_match_kid_happy_path_returns_matching_key():
    keys = [_KeyStub("a"), _KeyStub("b"), _KeyStub("c")]
    result = PyJWKClient.match_kid(keys, "b")
    assert result is keys[1]

# não encontra correspondência: retorna None quando nenhum key_id bate
def test_match_kid_none_when_no_match():
    keys = [_KeyStub("x"), _KeyStub("y")]
    result = PyJWKClient.match_kid(keys, "z")
    assert result is None

# duplicatas: retorna a primeira chave correspondente entre duplicates
def test_match_kid_first_duplicate_returned():
    k1 = _KeyStub("dup")
    k2 = _KeyStub("dup")
    keys = [k1, k2, _KeyStub("other")]
    result = PyJWKClient.match_kid(keys, "dup")
    assert result is k1

# aresta: lista vazia deve retornar None
def test_match_kid_empty_list_returns_none():
    keys = []
    result = PyJWKClient.match_kid(keys, "anything")
    assert result is None
