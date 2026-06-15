from repositorios.pyjwt.jwt.api_jws import PyJWS


def _make_pyjws_with_algs(algs):
    obj = object.__new__(PyJWS)
    obj._valid_algs = algs
    return obj


# teste1: happy path com lista de algs não vazia
def test_get_algorithms_happy_path():
    jws = _make_pyjws_with_algs(("RS256", "HS256", "ES256"))
    assert jws.get_algorithms() == ["RS256", "HS256", "ES256"]


# teste2: caminho borda - lista vazia
def test_get_algorithms_empty():
    jws = _make_pyjws_with_algs(())
    assert jws.get_algorithms() == []


# teste3: retorna uma nova lista, não referência interna (imutabilidade do retorno)
def test_get_algorithms_returns_copy():
    jws = _make_pyjws_with_algs(["RS256", "HS256"])
    result1 = jws.get_algorithms()
    # modifica o estado interno após a chamada
    jws._valid_algs.append("ES256")
    result2 = jws.get_algorithms()
    assert result1 == ["RS256", "HS256"]
    assert result2 == ["RS256", "HS256", "ES256"]
    assert result1 is not result2


# teste4: preserva a ordem proveniente da entrada
def test_get_algorithms_preserves_input_order():
    algs = ("A1", "A2", "A3")
    jws = _make_pyjws_with_algs(algs)
    assert jws.get_algorithms() == ["A1", "A2", "A3"]
