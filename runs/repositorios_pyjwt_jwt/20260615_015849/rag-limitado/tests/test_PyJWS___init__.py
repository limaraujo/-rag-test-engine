import repositorios.pyjwt.jwt.api_jws as api_jws
from repositorios.pyjwt.jwt.api_jws import PyJWS

# Verifica caminho feliz: algoritmo padrão sem filtros (algorithms=None)
def test_pyjws_default_keeps_all_algorithms(monkeypatch):
    dummy_algos = {'HS256': object(), 'RS256': object(), 'EdDSA': object()}
    monkeypatch.setattr(api_jws, 'get_default_algorithms', lambda: dummy_algos, raising=True)
    monkeypatch.setattr(api_jws.PyJWS, '_get_default_options', lambda self: {'default': 0}, raising=False)

    token = api_jws.PyJWS(algorithms=None)

    assert set(token._algorithms.keys()) == set(dummy_algos.keys())

# Verifica branch de filtragem: algoritmos fornecidos reduzem whitelist
def test_pyjws_prunes_unused_algorithms(monkeypatch):
    dummy_algos = {'HS256': object(), 'RS256': object(), 'ES256': object()}
    monkeypatch.setattr(api_jws, 'get_default_algorithms', lambda: dummy_algos, raising=True)

    token = api_jws.PyJWS(algorithms=['HS256'])

    assert set(token._algorithms.keys()) == {'HS256'}

# Verifica branch de merge de opções: options substitui defaults corretamente
def test_pyjws_options_merge_overrides_defaults(monkeypatch):
    dummy_algos = {'HS256': object()}
    monkeypatch.setattr(api_jws, 'get_default_algorithms', lambda: dummy_algos, raising=True)
    monkeypatch.setattr(api_jws.PyJWS, '_get_default_options', lambda self: {'default': 0, 'keep': True}, raising=False)

    token = api_jws.PyJWS(options={'default': 5, 'extra': 7})

    assert token.options == {'default': 5, 'keep': True, 'extra': 7}

# Verifica borda: algoritmos vazios resultam em dicionário de algoritmos vazio
def test_pyjws_empty_algorithms_results(monkeypatch):
    dummy_algos = {'A': object(), 'B': object()}
    monkeypatch.setattr(api_jws, 'get_default_algorithms', lambda: dummy_algos, raising=True)

    token = api_jws.PyJWS(algorithms=[])

    assert token._algorithms == {}
