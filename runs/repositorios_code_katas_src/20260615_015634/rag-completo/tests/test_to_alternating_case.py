from repositorios.code_katas.src.alt_case import to_alternating_case

# happy path: troca todos os caracteres alfabéticos de minúsculo para maiúsculo
def test_to_alternating_case_basic():
    assert to_alternating_case("hello") == "HELLO"

# path com espaços/entrada mista: preserva espaços e troca nos pares restantes
def test_to_alternating_case_with_spaces():
    assert to_alternating_case("Hello World") == "hELLO wORLD"

# edge: dígitos/pontuação não são alterados
def test_to_alternating_case_with_digits_and_punctuation():
    assert to_alternating_case("ab1CD!") == "AB1cd!"

# border: string vazia retorna vazia
def test_to_alternating_case_empty_string():
    assert to_alternating_case("") == ""
