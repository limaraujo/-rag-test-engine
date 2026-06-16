from repositorios.code_katas.src.get_grade import get_grade

# Verifica A: média >= 90 (happy path)
def test_get_grade_A():
    assert get_grade(95, 92, 90) == 'A'

# Verifica B: média entre 80 e 89
def test_get_grade_B():
    assert get_grade(80, 80, 80) == 'B'

# Verifica C: média entre 70 e 79
def test_get_grade_C():
    assert get_grade(70, 70, 70) == 'C'

# Verifica D: média entre 60 e 69
def test_get_grade_D():
    assert get_grade(60, 60, 60) == 'D'
