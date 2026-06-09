from mockes.exemplo import Calculadora
import pytest

def test_potencia_happy_path():
    """Calculates positive integer powers correctly (2^3 == 8)."""
    calc = Calculadora(nome="Calc")
    assert calc.potencia(2, 3) == 8

def test_potencia_zero_exponent():
    """Any number to the zero power returns 1 (5^0 == 1)."""
    calc = Calculadora(nome="Calc")
    assert calc.potencia(5, 0) == 1

def test_potencia_zero_base_zero_exponent():
    """0 to the 0 power follows Python semantics and returns 1."""
    calc = Calculadora(nome="Calc")
    assert calc.potencia(0, 0) == 1

def test_potencia_negative_exponent_raises():
    """Providing a negative exponent raises ValueError with an explanatory message."""
    calc = Calculadora(nome="Calc")
    with pytest.raises(ValueError) as exc:
        calc.potencia(2, -3)
    assert "Expoente negativo" in str(exc.value)

def test_potencia_negative_base_odd_and_even():
    """Negative base with odd exponent yields negative result, even exponent yields positive result."""
    calc = Calculadora(nome="Calc")
    assert calc.potencia(-2, 3) == -8  # odd exponent -> negative
    assert calc.potencia(-2, 4) == 16  # even exponent -> positive

def test_potencia_invalid_input_type_raises():
    """Non-integer inputs that cannot be exponentiated raise a TypeError."""
    calc = Calculadora(nome="Calc")
    with pytest.raises(TypeError):
        calc.potencia("2", 3)
    with pytest.raises(TypeError):
        calc.potencia(2, "3")