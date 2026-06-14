from __future__ import annotations

import re

from llm.base import BaseLLM
from llm.call_logger import get_call_logger
from llm.models import LLMRequest, LLMResponse


def _extract_field(prompt: str, field: str) -> str | None:
    match = re.search(rf"^{field}:\s*(.+)$", prompt, re.MULTILINE)
    return match.group(1).strip() if match else None


def _extract_code_block(prompt: str) -> str:
    match = re.search(r"```python\n(.*?)```", prompt, re.DOTALL)
    return match.group(1).strip() if match else ""


def _module_from_path(file_path: str) -> str:
    stem = file_path.replace("\\", "/").split("/")[-1]
    return stem.removesuffix(".py")


def _build_mock_test(user_prompt: str) -> str:
    qname = _extract_field(user_prompt, "nome") or "target"
    file_path = _extract_field(user_prompt, "arquivo") or "module.py"
    class_name = _extract_field(user_prompt, "classe")
    source = _extract_code_block(user_prompt)

    module = _module_from_path(file_path)
    simple_name = qname.split(".")[-1]

    if class_name or "." in qname:
        cls = class_name or qname.rsplit(".", 1)[0]
        import_line = f"from {module} import {cls}"
        setup = f"    instance = {cls}()\n"
        invoke = f"instance.{simple_name}"
    else:
        import_line = f"from {module} import {simple_name}"
        setup = ""
        invoke = simple_name

    raises_block = ""
    if "raise " in source:
        raises_block = f"""

def test_{simple_name}_raises():
{setup}    with pytest.raises(Exception):
        {invoke}(0, 0)
"""

    return f"""import pytest

{import_line}


def test_{simple_name}_happy_path():
{setup}    result = {invoke}(1, 2)
    assert result is not None
{raises_block}""".strip()


class MockLLM(BaseLLM):
    """LLM local que gera testes mínimos sem chamar a API OpenAI."""

    def __init__(self) -> None:
        self.model = "mock-offline"

    def generate(self, request: LLMRequest) -> LLMResponse:
        if "Arquivo de teste falho" in request.user_prompt:
            code_match = re.search(
                r"## Arquivo de teste falho\n```python\n(.*?)```",
                request.user_prompt,
                re.DOTALL,
            )
            code = code_match.group(1).strip() if code_match else ""
            if code and "def test_offline_smoke" not in code:
                code += "\n\ndef test_offline_smoke():\n    assert True\n"
            response = LLMResponse(
                content=code or _build_mock_test(request.user_prompt),
                model=self.model,
            )
        else:
            response = LLMResponse(
                content=_build_mock_test(request.user_prompt),
                model=self.model,
            )
        get_call_logger().log_llm(request, response, model=self.model)
        return response
