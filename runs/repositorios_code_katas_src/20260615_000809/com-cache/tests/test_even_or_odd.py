from repositorios.code_katas.src.even_odd import even_or_odd

# curto: happy path — retorna 'Even' para número par (caso simples)
def test_even_number_returns_Even():
    assert even_or_odd(4) == "Even"

# curto: branch alternativo — retorna 'Odd' para número ímpar
def test_odd_number_returns_Odd():
    assert even_or_odd(3) == "Odd"
