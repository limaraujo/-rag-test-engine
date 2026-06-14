from __future__ import annotations

import ast
import json
import re
import subprocess
import tempfile
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path

import coverage as cov_lib

from config.settings import settings
from execution.coverage import _format_ranges
from execution.runner import RunResult, _build_env, _parse_pytest_counts
from schemas.outputs import GeneratedTest


@dataclass
class CoverageGap:
    file_path: str
    function_name: str
    uncovered_lines: list[int]


@dataclass
class _FunctionSpan:
    name: str
    start_line: int
    end_line: int


@dataclass
class CoverageAnalysisResult:
    """Resultado interno da análise coverage.py para um arquivo fonte."""

    file_path: str
    executable_lines: set[int] = field(default_factory=set)
    missing_lines: list[int] = field(default_factory=list)
    missing_branches: list[tuple[int, int]] = field(default_factory=list)
    function_spans: list[_FunctionSpan] = field(default_factory=list)


class CoverageAnalyzer:
    """
    Executa coverage.py após geração de testes e extrai lacunas estruturadas.

    Fluxo típico::

        analyzer = CoverageAnalyzer(test, source_path, target_function=qname)
        result = analyzer.run()
        if result.passed and not analyzer.meets_threshold():
            gaps = analyzer.find_gaps()
            summary = analyzer.generate_summary()
    """

    def __init__(
        self,
        test: GeneratedTest,
        source_path: str,
        *,
        target_function: str | None = None,
        pythonpath: list[str] | None = None,
        threshold: float | None = None,
        timeout: int = 30,
    ) -> None:
        self._test = test
        self._source_path = Path(source_path).resolve()
        self._target_function = target_function
        self._pythonpath = pythonpath or []
        self._threshold = (
            threshold if threshold is not None else settings.COVERAGE_THRESHOLD
        )
        self._timeout = timeout

        self._run_result: RunResult | None = None
        self._coverage: cov_lib.Coverage | None = None
        self._analysis: CoverageAnalysisResult | None = None
        self._gaps: list[CoverageGap] | None = None

    def run(self) -> RunResult:
        """Executa pytest sob coverage.py e armazena o resultado para análise."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            safe_name = re.sub(r"[^a-zA-Z0-9_]", "_", self._test.target_function)
            test_file = tmp / f"test_{safe_name}.py"
            test_file.write_text(self._test.full_code, encoding="utf-8")

            data_file = tmp / ".coverage"
            source_dir = str(self._source_path.parent)

            env = _build_env(self._pythonpath)
            cmd = [
                "python", "-m", "coverage", "run",
                "--branch",
                f"--source={source_dir}",
                f"--data-file={data_file}",
                "-m", "pytest",
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
                    timeout=self._timeout,
                    env=env,
                )
            except subprocess.TimeoutExpired:
                self._run_result = RunResult(
                    passed=False,
                    exit_code=-1,
                    stdout="",
                    stderr=f"pytest excedeu o tempo limite após {self._timeout}s",
                    duration_seconds=float(self._timeout),
                    test_file=str(test_file),
                )
                self._coverage = None
                self._analysis = None
                self._gaps = None
                return self._run_result

            duration = round(time.perf_counter() - start, 3)

            cov = cov_lib.Coverage(data_file=str(data_file), source=[source_dir])
            try:
                cov.load()
            except cov_lib.exceptions.CoverageException:
                cov = None

            num_passed, num_failed, num_errors = _parse_pytest_counts(proc.stdout)
            self._run_result = RunResult(
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
            self._coverage = cov
            self._analysis = self._analyze_file(cov) if cov else None
            self._gaps = None
            return self._run_result

    def find_gaps(self) -> list[CoverageGap]:
        """Retorna lacunas de cobertura agrupadas por função."""
        if self._gaps is not None:
            return self._gaps

        if self._analysis is None:
            self._gaps = []
            return self._gaps

        gaps: list[CoverageGap] = []
        missing = set(self._analysis.missing_lines)

        for span in self._analysis.function_spans:
            if self._target_function and span.name != self._target_function:
                continue
            uncovered = sorted(
                line for line in missing
                if span.start_line <= line <= span.end_line
            )
            if uncovered:
                gaps.append(CoverageGap(
                    file_path=str(self._source_path),
                    function_name=span.name,
                    uncovered_lines=uncovered,
                ))

        self._gaps = gaps
        return self._gaps

    def generate_summary(self) -> dict:
        """Produz JSON estruturado com métricas e lacunas de cobertura."""
        analysis = self._analysis
        gaps = self.find_gaps()

        if analysis is None:
            return {
                "source_file": str(self._source_path),
                "target_function": self._target_function,
                "line_coverage_percent": 0.0,
                "threshold_percent": self._threshold,
                "meets_threshold": False,
                "total_executable_lines": 0,
                "covered_lines": 0,
                "missing_lines": [],
                "gaps": [asdict(g) for g in gaps],
                "uncovered_branches": [],
                "uncovered_functions": [],
                "error": "coverage data unavailable",
            }

        total = len(analysis.executable_lines)
        missing = analysis.missing_lines
        covered = total - len(missing)
        percentage = round(100.0 * covered / total, 1) if total else 100.0

        uncovered_branches = self._branch_gaps(analysis)
        uncovered_functions = self._uncovered_functions(analysis)

        return {
            "source_file": str(self._source_path),
            "target_function": self._target_function,
            "line_coverage_percent": percentage,
            "threshold_percent": self._threshold,
            "meets_threshold": percentage >= self._threshold,
            "total_executable_lines": total,
            "covered_lines": covered,
            "missing_lines": missing,
            "missing_lines_formatted": _format_ranges(missing),
            "gaps": [asdict(g) for g in gaps],
            "uncovered_branches": uncovered_branches,
            "uncovered_functions": uncovered_functions,
        }

    def generate_summary_json(self, *, indent: int = 2) -> str:
        """Serializa :meth:`generate_summary` como string JSON."""
        return json.dumps(self.generate_summary(), indent=indent, ensure_ascii=False)

    def meets_threshold(self) -> bool:
        """Verdadeiro quando a cobertura de linhas atinge o threshold configurado."""
        return self.generate_summary()["meets_threshold"]

    def gaps_for_prompt(self) -> list[dict]:
        """Gaps prontos para injeção no FunctionContext."""
        return [asdict(g) for g in self.find_gaps()]

    # ── Interno ──────────────────────────────────────────────────────────────

    def _analyze_file(self, cov: cov_lib.Coverage) -> CoverageAnalysisResult | None:
        file_path = str(self._source_path)
        try:
            filename, executable, _excluded, missing, missing_branches = cov.analysis2(
                file_path
            )
        except cov_lib.exceptions.CoverageException:
            return None

        source = self._source_path.read_text(encoding="utf-8")
        spans = _index_functions(source)

        branch_arcs: list[tuple[int, int]] = []
        if isinstance(missing_branches, (list, tuple)):
            for arc in missing_branches:
                if isinstance(arc, (list, tuple)) and len(arc) >= 2:
                    branch_arcs.append((int(arc[0]), int(arc[1])))

        return CoverageAnalysisResult(
            file_path=filename,
            executable_lines=set(executable),
            missing_lines=sorted(missing),
            missing_branches=branch_arcs,
            function_spans=spans,
        )

    def _branch_gaps(self, analysis: CoverageAnalysisResult) -> list[dict]:
        if not analysis.missing_branches:
            return []

        gaps: list[dict] = []
        for from_line, to_line in analysis.missing_branches:
            fn = _function_at_line(analysis.function_spans, from_line)
            if self._target_function and fn != self._target_function:
                continue
            gaps.append({
                "file_path": str(self._source_path),
                "function_name": fn,
                "from_line": from_line,
                "to_line": to_line,
            })
        return gaps

    def _uncovered_functions(self, analysis: CoverageAnalysisResult) -> list[dict]:
        missing = set(analysis.missing_lines)
        executable = analysis.executable_lines
        uncovered: list[dict] = []

        missing_set = set(missing)
        for span in analysis.function_spans:
            if self._target_function and span.name != self._target_function:
                continue
            fn_lines = {
                line for line in executable
                if span.start_line <= line <= span.end_line
            }
            if not fn_lines:
                continue
            body_lines = {line for line in fn_lines if line > span.start_line}
            if not body_lines:
                body_lines = fn_lines
            if body_lines.isdisjoint(missing_set):
                continue
            if not (body_lines - missing_set):
                uncovered.append({
                    "file_path": str(self._source_path),
                    "function_name": span.name,
                })
        return uncovered


def _index_functions(source: str) -> list[_FunctionSpan]:
    """Mapeia funções e métodos do arquivo para intervalos de linha."""
    tree = ast.parse(source)
    spans: list[_FunctionSpan] = []

    for node in tree.body:
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
            spans.append(_FunctionSpan(
                name=node.name,
                start_line=node.lineno,
                end_line=node.end_lineno or node.lineno,
            ))
        elif isinstance(node, ast.ClassDef):
            for child in node.body:
                if isinstance(child, ast.FunctionDef | ast.AsyncFunctionDef):
                    spans.append(_FunctionSpan(
                        name=f"{node.name}.{child.name}",
                        start_line=child.lineno,
                        end_line=child.end_lineno or child.lineno,
                    ))
    return spans


def _function_at_line(spans: list[_FunctionSpan], line: int) -> str:
    for span in spans:
        if span.start_line <= line <= span.end_line:
            return span.name
    return "<module>"


def coverage_round_signature(summary: dict) -> str:
    """Assinatura estável de uma rodada de cobertura (detecta repetição idêntica)."""
    missing = tuple(summary.get("missing_lines") or [])
    gaps = tuple(
        (g.get("function_name"), tuple(g.get("uncovered_lines") or []))
        for g in summary.get("gaps") or []
    )
    pct = summary.get("line_coverage_percent")
    return f"{pct}|{missing}|{gaps}"
