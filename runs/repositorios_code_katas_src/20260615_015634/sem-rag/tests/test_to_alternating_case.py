from repositorios.code_katas.src.alt_case import to_alternating_case

# Teste feliz: swap de letras mantendo espaços e pontuação
def test_to_alternating_case_happy_path():
    s = "Hello World!"
    assert to_alternating_case(s) == "hELLO wORLD!"

# Teste de borda: string vazia deve retornar vazia
def test_to_alternating_case_empty_string():
    assert to_alternating_case("") == ""

# Teste com dígitos/pontuação: apenas letras devem ser swapadas
def test_to_alternating_case_digits_and_punctuation():
    s = "123abcXYZ!"
    assert to_alternating_case(s) == "123ABCxyz!"

# Teste com Unicode: caracteres não-ASCII também possuem swap de caso
def test_to_alternating_case_unicode_characters():
    s = "ábÇ1"
    assert to_alternating_case(s) == "ÁBç1"
