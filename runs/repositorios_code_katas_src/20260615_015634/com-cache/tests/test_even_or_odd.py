from repositorios.code_katas.src.even_odd import even_or_odd

# curto: verifica o caminho verdadeiro da condição com número par
def test_even_number_returns_Even():
    assert even_or_odd(4) == "Even"

# curto: verifica o caminho falso da condição com número ímpar
def test_odd_number_returns_Odd():
    assert even_or_odd(7) == "Odd"
