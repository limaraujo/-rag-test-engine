from agents.import_utils import normalize_test_imports
from schemas.context import FunctionContext


def test_normalize_test_imports_uses_full_module_path() -> None:
    context = FunctionContext(
        function_name="divide",
        qualified_name="Calculadora.divide",
        symbol_type="method",
        class_name="Calculadora",
        file_path="mockes/exemplo.py",
        module_name="mockes.exemplo",
        code="def divide(self, a, b): ...",
    )
    raw = "import pytest\nfrom exemplo import Calculadora\n\ndef test_x(): pass\n"
    fixed = normalize_test_imports(
        raw,
        module="mockes.exemplo",
        name="Calculadora",
    )
    assert "from mockes.exemplo import Calculadora" in fixed
    assert "from exemplo import" not in fixed
