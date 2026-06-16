import pytest
from repositorios.code_katas.src.parenthetics import DoubleLink

def test_balanced_happy_path():
    dl = DoubleLink()
    dl.push('(')
    dl.push(')')
    assert dl.balanced() == -1

def test_balanced_unmatched_open():
    dl = DoubleLink()
    dl.push('(')
    dl.push('(')
    assert dl.balanced() == 1

def test_balanced_unmatched_closed_head():
    dl = DoubleLink()
    dl.push(')')
    assert dl.balanced() == -1

@pytest.mark.parametrize("values", [
    [],
    ['x'],
])
def test_balanced_exceptions(values):
    dl = DoubleLink()
    for v in values:
        dl.push(v)
    with pytest.raises(ValueError):
        dl.balanced()
