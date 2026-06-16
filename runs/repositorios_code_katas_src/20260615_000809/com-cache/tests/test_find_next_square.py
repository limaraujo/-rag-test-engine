from repositorios.code_katas.src.next_sq import find_next_square

# curto: happy path — quadrado perfeito (16) retorna o próximo quadrado (25)
def test_find_next_square_happy_path():
    assert find_next_square(16) == 25

# curto: caso não é quadrado perfeito (15) retorna -1
def test_find_next_square_not_perfect():
    assert find_next_square(15) == -1

# curto: borda: 0 é quadrado perfeito, retorna 1
def test_find_next_square_zero():
    assert find_next_square(0) == 1
