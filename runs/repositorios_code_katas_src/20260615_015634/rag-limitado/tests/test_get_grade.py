import pytest
from repositorios.code_katas.src.get_grade import get_grade

# verifica várias faixas (A/B/C/D) cobrindo branches da função get_grade
@pytest.mark.parametrize(
    "s1,s2,s3,expected",
    [
        (95, 92, 94, 'A'),  # avg ~93.7 -> A
        (85, 82, 84, 'B'),  # avg ~83.7 -> B
        (75, 72, 73, 'C'),  # avg ~74 -> C
        (60, 60, 60, 'D'),  # avg 60 -> D
    ]
)
def test_get_grade_various_branches(s1, s2, s3, expected):
    # verifica branches A/B/C/D
    assert get_grade(s1, s2, s3) == expected
