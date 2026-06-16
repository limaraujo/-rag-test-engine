from repositorios.code_katas.src.alt_case import to_alternating_case

# curto: happy path com string simples (mistura de maiúsculas/minúsculas)
def test_to_alternating_case_happy_path_basic():
    assert to_alternating_case("Hello") == "hELLO"

# curto: incluindo caracteres não alfabéticos mantidos (números e símbolos)
def test_to_alternating_case_with_digits_and_symbols():
    assert to_alternating_case("Hello, World! 123") == "hELLO, wORLD! 123"

# curto: suporte a caracteres unicode/acentuados
def test_to_alternating_case_unicode_characters():
    assert to_alternating_case("áBC") == "Ábc"

# curto: caso vazio (string vazia)
def test_to_alternating_case_empty_string():
    assert to_alternating_case("") == ""
