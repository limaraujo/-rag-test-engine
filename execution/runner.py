from __future__ import annotations

import re
import subprocess
import tempfile
import time
from dataclasses import dataclass, field
from pathlib import Path

from schemas.outputs import GeneratedTest
from execution.pytest_support import (
    build_pytest_env,
    parse_pytest_counts,
    pytest_timeout_message,
    safe_test_stem,
)

# Aliases legados para compatibilidade com imports existentes.
_build_env = build_pytest_env
_parse_pytest_counts = parse_pytest_counts


@dataclass
class RunResult:
    """
    Resultado da execução de um arquivo GeneratedTest com pytest.

    Produzido por :class:`TestRunner.run` — use isso para decidir se deve
    aceitar o teste, corrigi-lo ou descartá-lo.
    """

    passed: bool
    """Verdadeiro apenas quando o pytest retorna código 0 (todos os testes passaram)."""

    exit_code: int
    """Código de saída bruto do pytest. 0 = todos passaram, 1 = alguns falharam, 2 = interrompido,
    3 = erro interno, 4 = erro de uso, 5 = nenhum teste coletado."""

    stdout: str
    stderr: str
    duration_seconds: float
    test_file: str
    """Caminho absoluto para o arquivo temporário que foi executado."""

    num_passed: int = 0
    num_failed: int = 0
    num_errors: int = 0

    @property
    def output(self) -> str:
        """stdout + stderr combinados — use isso ao enviar erros para o LLM."""
        parts = [p for p in (self.stdout, self.stderr) if p.strip()]
        return "\n".join(parts)

    @property
    def failure_summary(self) -> str:
        """
        Trecho conciso da saída de falha.

        Extrai a seção ``FAILURES`` da saída do pytest para que o agente de
        correção veja apenas o erro relevante, e não todo o log de execução.
        Limitado a 3000 caracteres para caber no contexto do LLM.
        """
        if self.passed:
            return ""

        lines = self.output.splitlines()
        failure_lines: list[str] = []
        capturing = False

        for line in lines:
            if re.match(r"=+ FAILURES =+|=+ ERRORS =+", line):
                capturing = True
            if capturing:
                failure_lines.append(line)
            # Para após a seção de resumo curto dos testes
            if capturing and re.match(r"=+ short test summary", line):
                break

        summary = "\n".join(failure_lines)
        return summary[:3000] if summary else self.output[:3000]


@dataclass
class SuiteValidationResult:
    """Resultado da validação pytest de uma pasta de testes gerados."""

    passed: bool
    exit_code: int
    stdout: str
    stderr: str
    duration_seconds: float
    tests_dir: str
    num_passed: int = 0
    num_failed: int = 0
    num_errors: int = 0

    @property
    def output(self) -> str:
        parts = [p for p in (self.stdout, self.stderr) if p.strip()]
        return "\n".join(parts)


class TestRunner:
    """
    Executa um :class:`~schemas.outputs.GeneratedTest` usando pytest em um subprocesso.

    O código do teste é escrito em um arquivo temporário descartável para que nada seja persistido
    até que o chamador salve explicitamente um teste que passou.

    Exemplo::

        runner = TestRunner()
        result = runner.run(test, pythonpath=["src/"])
        if result.passed:
            Path("tests/test_soma.py").write_text(test.full_code)
    """

    def run(
        self,
        test: GeneratedTest,
        *,
        pythonpath: list[str] | None = None,
        timeout: int = 30,
    ) -> RunResult:
        """
        Escreve *test* em um arquivo temporário e executa pytest nele.

        Args:
            test:        O teste gerado a ser executado.
            pythonpath:  Diretórios adicionados ao ``PYTHONPATH`` para que o pytest
                         encontre o módulo sob teste. Normalmente a raiz do repositório ou
                         o diretório ``src/``.
            timeout:     Tempo em segundos antes do subprocesso ser encerrado.

        Returns:
            Um :class:`RunResult` com status de sucesso/falha e saída.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / f"test_{safe_test_stem(test.target_function)}.py"
            test_file.write_text(test.full_code, encoding="utf-8")

            return self._run_pytest(
                test_file=test_file,
                extra_pythonpath=pythonpath or [],
                timeout=timeout,
            )

    def run_directory(
        self,
        tests_dir: Path,
        *,
        pythonpath: list[str] | None = None,
        rootdir: Path | None = None,
        timeout: int = 120,
    ) -> SuiteValidationResult:
        """
        Executa pytest em todos os arquivos de uma pasta de testes gerados.

        Usado pelo orquestrador para validar a suíte completa após o pipeline.
        """
        tests_dir = tests_dir.resolve()
        test_files = sorted(tests_dir.glob("test_*.py"))
        if not test_files:
            return SuiteValidationResult(
                passed=True,
                exit_code=0,
                stdout="Nenhum teste gerado para validar.",
                stderr="",
                duration_seconds=0.0,
                tests_dir=str(tests_dir),
            )

        env = build_pytest_env(pythonpath or [])
        project_root = (rootdir or tests_dir).resolve()

        cmd = [
            "python", "-m", "pytest",
            str(tests_dir),
            "-v",
            "--tb=short",
            "--rootdir", str(project_root),
        ]

        start = time.perf_counter()
        try:
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                env=env,
                cwd=str(project_root),
            )
        except subprocess.TimeoutExpired:
            return SuiteValidationResult(
                passed=False,
                exit_code=-1,
                stdout="",
                stderr=pytest_timeout_message(timeout),
                duration_seconds=float(timeout),
                tests_dir=str(tests_dir),
            )

        duration = round(time.perf_counter() - start, 3)
        num_passed, num_failed, num_errors = parse_pytest_counts(proc.stdout)

        return SuiteValidationResult(
            passed=proc.returncode == 0,
            exit_code=proc.returncode,
            stdout=proc.stdout,
            stderr=proc.stderr,
            duration_seconds=duration,
            tests_dir=str(tests_dir),
            num_passed=num_passed,
            num_failed=num_failed,
            num_errors=num_errors,
        )

    # ── Interno ──────────────────────────────────────────────────────────────

    def _run_pytest(
        self,
        test_file: Path,
        extra_pythonpath: list[str],
        timeout: int,
    ) -> RunResult:
        env = build_pytest_env(extra_pythonpath)

        cmd = [
            "python", "-m", "pytest",
            str(test_file),
            "-v",
            "--tb=short",
            "--no-header",
            "--rootdir", str(test_file.parent),
            "--noconftest",
        ]

        start = time.perf_counter()
        try:
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                env=env,
            )
        except subprocess.TimeoutExpired:
            return RunResult(
                passed=False,
                exit_code=-1,
                stdout="",
                stderr=pytest_timeout_message(timeout),
                duration_seconds=float(timeout),
                test_file=str(test_file),
            )

        duration = round(time.perf_counter() - start, 3)
        num_passed, num_failed, num_errors = parse_pytest_counts(proc.stdout)

        return RunResult(
            passed=proc.returncode == 0,
            exit_code=proc.returncode,
            stdout=proc.stdout,
            stderr=proc.stderr,
            duration_seconds=duration,
            test_file=str(test_file),
            num_passed=num_passed,
            num_failed=num_failed,
            num_errors=num_errors,
        )
