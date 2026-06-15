from repositorios.pyjwt.jwt.api_jws import PyJWS

# happy path: _valid_algs é uma lista; verifica a ordem e retorno como lista
def test_get_algorithms_happy_path_list():
    inst = object.__new__(PyJWS)
    inst._valid_algs = ["HS256", "RS256"]
    result = inst.get_algorithms()
    assert result == ["HS256", "RS256"]
    assert isinstance(result, list)

# happy path: _valid_algs é um tuple; verifica conversão para lista preservando a ordem
def test_get_algorithms_happy_path_tuple():
    inst = object.__new__(PyJWS)
    inst._valid_algs = ("HS256", "RS256")
    result = inst.get_algorithms()
    assert result == ["HS256", "RS256"]
    assert isinstance(result, list)

# borda: _valid_algs é um set; verifica retorno como lista e cobertura de conteúdo
def test_get_algorithms_with_set():
    inst = object.__new__(PyJWS)
    algs = {"HS256", "RS256"}
    inst._valid_algs = algs
    result = inst.get_algorithms()
    assert isinstance(result, list)
    assert set(result) == algs
    assert len(result) == len(algs)
