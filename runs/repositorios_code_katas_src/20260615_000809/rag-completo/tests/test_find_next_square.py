from repositorios.code_katas.src.next_sq import find_next_square

# verifica caminho feliz: entrada é quadrado perfeito (16 -> 25)
def test_find_next_square_happy_path():
    assert find_next_square(16) == 25

# verifica comportamento quando a entrada não é quadrado perfeito (14 -> -1)
def test_find_next_square_not_perfect():
    assert find_next_square(14) == -1

# verifica borda: entrada 0 deve retornar 1 (0 é quadrado perfeito)
def test_find_next_square_zero():
    assert find_next_square(0) == 1

# verifica outro caso de quadrado perfeito (1 -> 4)
def test_find_next_square_one():
    assert find_next_square(1) == 4
