from repositorios.pyjwt.jwt.api_jwk import PyJWK

# Verifica que from_dict passa o dict de entrada e recebe algorithm=None (caso feliz)
def test_from_dict_passes_input_and_none_algorithm(monkeypatch):
    obj = {"kty": "oct", "alg": "HS256", "kid": "test"}
    captured = {}

    orig_init = PyJWK.__init__

    def patched_init(self, obj_arg, algorithm=None):
        captured["obj"] = obj_arg
        captured["algorithm"] = algorithm
        # Não chama o __init__ original para evitar dependências de implementação
        self._jwk_data = obj_arg
        self.alg = algorithm if algorithm is not None else obj_arg.get("alg")

    monkeypatch.setattr(PyJWK, "__init__", patched_init, raising=True)
    result = PyJWK.from_dict(obj, algorithm=None)

    assert isinstance(result, PyJWK)
    assert captured["obj"] == obj
    assert captured["algorithm"] is None
    # Verifica comportamento padrão do PyJWK (alg vindo do dict) ao inicializar
    assert getattr(result, "alg", None) == obj["alg"]

# Verifica que o algoritmo explícito informado sobrescreve o alg do dict
def test_from_dict_uses_explicit_algorithm(monkeypatch):
    obj = {"kty": "oct", "alg": "HS256", "kid": "id"}
    captured = {}

    orig_init = PyJWK.__init__

    def patched_init(self, obj_arg, algorithm=None):
        captured["obj"] = obj_arg
        captured["algorithm"] = algorithm
        # Não chama o __init__ original para evitar dependências de implementação
        self._jwk_data = obj_arg
        self.alg = algorithm if algorithm is not None else obj_arg.get("alg")

    monkeypatch.setattr(PyJWK, "__init__", patched_init, raising=True)
    explicit = "RS256"
    result = PyJWK.from_dict(obj, algorithm=explicit)

    assert isinstance(result, PyJWK)
    assert captured["obj"] == obj
    assert captured["algorithm"] == explicit
    assert getattr(result, "alg", None) == explicit
