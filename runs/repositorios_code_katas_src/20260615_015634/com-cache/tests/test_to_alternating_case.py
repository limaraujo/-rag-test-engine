from repositorios.code_katas.src.alt_case import to_alternating_case

# curto: teste happy path com string simples (mistura de maiúsculas/minúsculas)
def test_to_alternating_case_happy_path_basic():
    assert to_alternating_case("Hello") == "hELLO"

# curto: teste com caracteres não alfabéticos preservados (números e pontuação)
def test_to_alternating_case_with_non_letters():
    assert to_alternating_case("123!abc") == "123!ABC"

# curto: caso de borda básico (string vazia)
def test_to_alternating_case_empty_string():
    assert to_alternating_case("") == ""

# curto: caso com espaços e mix de maiúsculas/minúsculas
def test_to_alternating_case_with_spaces_and_mix():
    assert to_alternating_case("aBc DeF") == "AbC dEf"
