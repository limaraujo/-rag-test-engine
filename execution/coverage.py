from __future__ import annotations

import re
import time
import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

from execution.runner import RunResult, _build_env, _parse_pytest_counts
from schemas.outputs import GeneratedTest


@dataclass
class CoverageReport:
    """
    Estatísticas de cobertura de linhas para um único módulo de código-fonte.

    Produzido por :class:`CoverageRunner.run_with_coverage` após analisar a
    saída do terminal do ``pytest-cov``.

    Exemplo::

        report = CoverageReport(
            module="calc",
            total_lines=20,
            covered_lines=17,
            missing_lines=[8, 12, 15],
        )
        print(f"{report.percentage}% coberto")   # "85.0% coberto"
        print(report.missing_lines)              # [8, 12, 15]
    """

    module: str
    total_lines: int
    covered_lines: int
    missing_lines: list[int] = field(default_factory=list)

    @property
    def percentage(self) -> float:
        """Percentual de cobertura, 0.0 – 100.0."""
        if self.total_lines == 0:
            return 100.0
        return round(100.0 * self.covered_lines / self.total_lines, 1)

    @property
    def is_complete(self) -> bool:
        """Verdadeiro quando todas as linhas executáveis estão cobertas."""
        return len(self.missing_lines) == 0 and self.total_lines > 0

    def uncovered_hint(self) -> str:
        """
        Lista legível por humanos das linhas não cobertas — útil como dica para prompt de LLM.

        Exemplo: "Linhas não cobertas: 8, 12, 15-17"
        """
        if not self.missing_lines:
            return "Todas as linhas cobertas."
        return "Linhas não cobertas: " + _format_ranges(self.missing_lines)


class CoverageRunner:
    """
    Variante de :class:`~execution.runner.TestRunner` que também coleta
    cobertura de linhas via ``pytest-cov``.

    Requer que ``pytest-cov`` esteja instalado (``uv add pytest-cov``).

    Exemplo::

        runner = CoverageRunner()
        result, report = runner.run_with_coverage(
            test,
            source_path="src/calc.py",
            pythonpath=["src/"],
        )
        if result.passed:
            print(f"Cobertura: {report.percentage}%")
            if not report.is_complete:
                print(report.uncovered_hint())
    """

    def run_with_coverage(
        self,
        test: GeneratedTest,
        source_path: str,
        *,
        pythonpath: list[str] | None = None,
        timeout: int = 30,
    ) -> tuple[RunResult, CoverageReport | None]:
        """
        Executa *test* com ``--cov`` e retorna resultado + relatório de cobertura.

        Args:
            test:        O teste gerado a ser executado.
            source_path: O arquivo de código-fonte para medir a cobertura.
                         Deve ser importável dado o *pythonpath* fornecido.
            pythonpath:  Diretórios adicionados ao ``PYTHONPATH`` antes da execução.
            timeout:     Tempo em segundos antes do subprocesso ser encerrado.

        Returns:
            ``(RunResult, CoverageReport | None)`` — a cobertura é ``None`` quando
            pytest-cov não está instalado ou a saída não pode ser analisada.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            safe_name = re.sub(r"[^a-zA-Z0-9_]", "_", test.target_function)
            test_file = Path(tmpdir) / f"test_{safe_name}.py"
            test_file.write_text(test.full_code, encoding="utf-8")

            result = self._run_pytest_cov(
                test_file=test_file,
                source_path=Path(source_path),
                extra_pythonpath=pythonpath or [],
                timeout=timeout,
            )

            coverage = parse_coverage_output(result.stdout, source_path)
            return result, coverage

    # ── Interno ──────────────────────────────────────────────────────────────

    def _run_pytest_cov(
        self,
        test_file: Path,
        source_path: Path,
        extra_pythonpath: list[str],
        timeout: int,
    ) -> RunResult:
        env = _build_env(extra_pythonpath)
        module_stem = source_path.stem  # "calc.py" → "calc"

        cmd = [
            "python", "-m", "pytest",
            str(test_file),
            f"--cov={module_stem}",
            "--cov-report=term-missing",
            "--tb=short",
            "--no-header",
        ]

        start = time.perf_counter()
        try:
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                env=env,
                cwd=str(source_path.parent.resolve()),
            )
        except subprocess.TimeoutExpired:
            return RunResult(
                passed=False,
                exit_code=-1,
                stdout="",
                stderr=f"pytest excedeu o tempo limite após {timeout}s",
                duration_seconds=float(timeout),
                test_file=str(test_file),
            )

        duration = round(time.perf_counter() - start, 3)
        num_passed, num_failed, num_errors = _parse_pytest_counts(proc.stdout)

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


# ── Helpers de parsing ─────────────────────────────────────────────────────────

def parse_coverage_output(output: str, source_path: str) -> CoverageReport | None:
    """
    Analisa a saída do terminal do ``pytest-cov`` e retorna um :class:`CoverageReport`.

    Lida com o formato padrão ``term-missing``::

        Name        Stmts   Miss  Cover   Missing
        ------------------------------------------
        calc.py        15      3    80%   8, 12-14
        ------------------------------------------
        TOTAL          15      3    80%

    Retorna ``None`` quando a linha do módulo não pode ser encontrada (ex: pytest-cov
    não instalado ou o arquivo fonte não foi importado durante a execução).
    """
    stem = Path(source_path).stem
    filename = Path(source_path).name

    for line in output.splitlines():
        # Corresponde a "calc.py   15   3   80%   8, 12-14"
        # ou              "calc      15   3   80%"
        if not (filename in line or (stem in line and "%" in line)):
            continue

        parts = line.split()
        if len(parts) < 4:
            continue

        try:
            stmts = int(parts[1])
            miss = int(parts[2])
        except ValueError:
            continue

        missing_lines: list[int] = []
        if len(parts) > 4:
            raw_missing = " ".join(parts[4:])
            missing_lines = _parse_missing_ranges(raw_missing)

        return CoverageReport(
            module=stem,
            total_lines=stmts,
            covered_lines=stmts - miss,
            missing_lines=missing_lines,
        )

    return None


def _parse_missing_ranges(text: str) -> list[int]:
    """
    Expande uma string de linhas faltantes do pytest-cov em uma lista ordenada de inteiros.

    Exemplos::

        "8, 12-14, 22"  →  [8, 12, 13, 14, 22]
        "30-32"         →  [30, 31, 32]
    """
    lines: list[int] = []
    for part in re.split(r"[,\s]+", text.strip()):
        if not part:
            continue
        if "-" in part:
            try:
                start, end = part.split("-", 1)
                lines.extend(range(int(start), int(end) + 1))
            except ValueError:
                pass
        else:
            digits = re.sub(r"[^\d]", "", part)
            if digits:
                lines.append(int(digits))
    return sorted(set(lines))


def _format_ranges(line_numbers: list[int]) -> str:
    """
    Comprime uma lista ordenada de inteiros em uma string compacta de intervalos.

    Exemplo: [8, 12, 13, 14, 22] → "8, 12-14, 22"
    """
    if not line_numbers:
        return ""
    sorted_lines = sorted(set(line_numbers))
    parts: list[str] = []
    start = end = sorted_lines[0]

    for n in sorted_lines[1:]:
        if n == end + 1:
            end = n
        else:
            parts.append(str(start) if start == end else f"{start}-{end}")
            start = end = n
    parts.append(str(start) if start == end else f"{start}-{end}")
    return ", ".join(parts)