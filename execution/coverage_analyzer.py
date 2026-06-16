from __future__ import annotations

import ast
import json
import subprocess
import tempfile
import time
from dataclasses import asdict, dataclass, field, replace
from pathlib import Path

import coverage as cov_lib

from config.settings import settings
from parsers.source.text_utils import read_source_text
from execution.coverage_format import format_ranges
from execution.pytest_support import (
    build_pytest_env,
    parse_pytest_counts,
    pytest_timeout_message,
    safe_test_stem,
)
from execution.runner import RunResult
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
    missing_branch_lines: list[int] = field(default_factory=list)
    branch_total: int = 0
    branch_missing: int = 0
    arc_possibilities: set[tuple[int, int]] = field(default_factory=set)
    arcs_executed: set[tuple[int, int]] = field(default_factory=set)
    function_spans: list[_FunctionSpan] = field(default_factory=list)


class CoverageAnalyzer:
    """
    Executa pytest-cov após geração de testes e extrai lacunas estruturadas.

    Com ``target_function``, ``line_coverage_percent``, ``missing_lines`` e
    ``branch_coverage_percent`` limitam-se ao símbolo alvo (função, método ou
    classe). Sem alvo, a métrica de linhas cobre o arquivo inteiro.

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
        """Executa pytest com pytest-cov (--cov-branch) e carrega o .coverage gerado."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            test_file = tmp / f"test_{safe_test_stem(self._test.target_function)}.py"
            test_file.write_text(self._test.full_code, encoding="utf-8")

            data_file = tmp / ".coverage"
            source_dir = str(self._source_path.parent)

            env = build_pytest_env(self._pythonpath)
            env["COVERAGE_FILE"] = str(data_file)

            cmd = [
                "python", "-m", "pytest",
                str(test_file),
                f"--cov={source_dir}",
                "--cov-branch",
                "--cov-report=",
                "-v",
                "--tb=short",
                "--no-header",
                "--rootdir", str(tmp),
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
                    cwd=str(tmp),
                )
            except subprocess.TimeoutExpired:
                self._run_result = RunResult(
                    passed=False,
                    exit_code=-1,
                    stdout="",
                    stderr=pytest_timeout_message(self._timeout),
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

            num_passed, num_failed, num_errors = parse_pytest_counts(proc.stdout)
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
                "branch_coverage_percent": 0.0,
                "threshold_percent": self._threshold,
                "meets_threshold": False,
                "total_executable_lines": 0,
                "covered_lines": 0,
                "total_branches": 0,
                "covered_branches": 0,
                "missing_branches_count": 0,
                "missing_lines": [],
                "gaps": [asdict(g) for g in gaps],
                "uncovered_branches": [],
                "uncovered_functions": [],
                "error": "coverage data unavailable",
            }

        total, covered, percentage, missing = _line_stats(
            analysis,
            self._target_function,
        )

        branch_total, branch_missing, branch_covered, branch_percentage, scoped_missing_lines = (
            _branch_stats(analysis, self._target_function)
        )
        if scoped_missing_lines is not None:
            analysis = replace(
                analysis,
                missing_branch_lines=scoped_missing_lines,
            )

        uncovered_branches = self._branch_gaps(analysis)
        uncovered_functions = self._uncovered_functions(analysis)

        return {
            "source_file": str(self._source_path),
            "target_function": self._target_function,
            "line_coverage_percent": percentage,
            "branch_coverage_percent": branch_percentage,
            "threshold_percent": self._threshold,
            "meets_threshold": percentage >= self._threshold,
            "total_executable_lines": total,
            "covered_lines": covered,
            "total_branches": branch_total,
            "covered_branches": branch_covered,
            "missing_branches_count": branch_missing,
            "missing_lines": missing,
            "missing_lines_formatted": format_ranges(missing),
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
        source = read_source_text(self._source_path)
        spans = _index_functions(source)

        try:
            analysis = cov._analyze(file_path)
        except cov_lib.exceptions.CoverageException:
            return self._analyze_file_legacy(cov, file_path, spans)

        numbers = analysis.numbers
        missing_branch_lines = sorted(int(line) for line in analysis.missing_branch_arcs())
        branch_arcs = [
            (line, line)
            for line in missing_branch_lines
        ]

        return CoverageAnalysisResult(
            file_path=file_path,
            executable_lines=set(analysis.statements),
            missing_lines=sorted(analysis.missing),
            missing_branches=branch_arcs,
            missing_branch_lines=missing_branch_lines,
            branch_total=numbers.n_branches,
            branch_missing=numbers.n_missing_branches,
            arc_possibilities=set(analysis.arc_possibilities_set),
            arcs_executed=set(analysis.arcs_executed_set),
            function_spans=spans,
        )

    def _analyze_file_legacy(
        self,
        cov: cov_lib.Coverage,
        file_path: str,
        spans: list[_FunctionSpan],
    ) -> CoverageAnalysisResult | None:
        try:
            filename, executable, _excluded, missing, missing_branches = cov.analysis2(
                file_path
            )
        except cov_lib.exceptions.CoverageException:
            return None

        branch_arcs: list[tuple[int, int]] = []
        missing_branch_lines: list[int] = []
        if isinstance(missing_branches, (list, tuple)):
            for arc in missing_branches:
                if isinstance(arc, (list, tuple)) and len(arc) >= 2:
                    branch_arcs.append((int(arc[0]), int(arc[1])))
        elif isinstance(missing_branches, str) and missing_branches.isdigit():
            line = int(missing_branches)
            missing_branch_lines = [line]
            branch_arcs = [(line, line)]

        return CoverageAnalysisResult(
            file_path=filename,
            executable_lines=set(executable),
            missing_lines=sorted(missing),
            missing_branches=branch_arcs,
            missing_branch_lines=missing_branch_lines,
            function_spans=spans,
        )

    def _branch_gaps(self, analysis: CoverageAnalysisResult) -> list[dict]:
        branch_lines = analysis.missing_branch_lines
        if not branch_lines and analysis.missing_branches:
            branch_lines = sorted({from_line for from_line, _ in analysis.missing_branches})
        if not branch_lines:
            return []

        gaps: list[dict] = []
        for line in branch_lines:
            fn = _function_at_line(analysis.function_spans, line)
            if self._target_function and fn != self._target_function:
                continue
            gaps.append({
                "file_path": str(self._source_path),
                "function_name": fn,
                "from_line": line,
                "to_line": line,
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


def _span_for_function(
    spans: list[_FunctionSpan],
    target_function: str | None,
) -> _FunctionSpan | None:
    if not target_function:
        return None
    for span in spans:
        if span.name == target_function:
            return span
    return None


def _line_stats(
    analysis: CoverageAnalysisResult,
    target_function: str | None,
) -> tuple[int, int, float, list[int]]:
    """
    Calcula cobertura de linhas.

    Com ``target_function``, limita às linhas executáveis do símbolo alvo
    (função, método ou classe). Sem alvo, usa o arquivo inteiro.
    """
    executable = analysis.executable_lines
    missing_set = set(analysis.missing_lines)

    span = _span_for_function(analysis.function_spans, target_function)
    if span is not None:
        scoped = _executable_lines_for_span(analysis, span)
        if not scoped:
            return 0, 0, 100.0, []
        scoped_missing = sorted(scoped & missing_set)
        covered = len(scoped) - len(scoped_missing)
        percentage = round(100.0 * covered / len(scoped), 1)
        return len(scoped), covered, percentage, scoped_missing

    total = len(executable)
    missing = analysis.missing_lines
    covered = total - len(missing)
    percentage = round(100.0 * covered / total, 1) if total else 100.0
    return total, covered, percentage, missing


def _executable_lines_for_span(
    analysis: CoverageAnalysisResult,
    span: _FunctionSpan,
) -> set[int]:
    return {
        line for line in analysis.executable_lines
        if span.start_line <= line <= span.end_line
    }


def _branch_stats(
    analysis: CoverageAnalysisResult,
    target_function: str | None,
) -> tuple[int, int, int, float, list[int] | None]:
    """
    Calcula cobertura de branches a partir dos dados do pytest-cov/coverage.py.

    Com ``target_function``, limita aos arcos de branch dentro desse símbolo
    (ignora branches de outras funções no mesmo arquivo).
    """
    if analysis.arc_possibilities:
        span = _span_for_function(analysis.function_spans, target_function)
        if span is not None:
            body_lines = {
                line for line in analysis.executable_lines
                if span.start_line < line <= span.end_line
            }
            exits = [
                arc for arc in analysis.arc_possibilities
                if arc[0] in body_lines and arc[0] > 0 and arc[1] > 0
            ]
            total = len(exits)
            missing = sum(1 for arc in exits if arc not in analysis.arcs_executed)
            covered = max(total - missing, 0)
            percentage = round(100.0 * covered / total, 1) if total else 100.0
            missing_lines = sorted(set(analysis.missing_branch_lines) & body_lines)
            return total, missing, covered, percentage, missing_lines

    total = analysis.branch_total
    missing = analysis.branch_missing
    covered = max(total - missing, 0)
    percentage = round(100.0 * covered / total, 1) if total else 100.0
    return total, missing, covered, percentage, None


def _index_functions(source: str) -> list[_FunctionSpan]:
    """Mapeia funções, métodos e classes do arquivo para intervalos de linha."""
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
            spans.append(_FunctionSpan(
                name=node.name,
                start_line=node.lineno,
                end_line=node.end_lineno or node.lineno,
            ))
            for child in node.body:
                if isinstance(child, ast.FunctionDef | ast.AsyncFunctionDef):
                    spans.append(_FunctionSpan(
                        name=f"{node.name}.{child.name}",
                        start_line=child.lineno,
                        end_line=child.end_lineno or child.lineno,
                    ))
    return spans


def _function_at_line(spans: list[_FunctionSpan], line: int) -> str:
    matches = [
        span for span in spans
        if span.start_line <= line <= span.end_line
    ]
    if not matches:
        return "<module>"
    # Prefer the innermost span (e.g. Class.method over Class).
    return min(matches, key=lambda span: (span.end_line - span.start_line, span.name)).name


def coverage_round_signature(summary: dict) -> str:
    """Assinatura estável de uma rodada de cobertura (detecta repetição idêntica)."""
    missing = tuple(summary.get("missing_lines") or [])
    gaps = tuple(
        (g.get("function_name"), tuple(g.get("uncovered_lines") or []))
        for g in summary.get("gaps") or []
    )
    branches = tuple(
        (b.get("function_name"), b.get("from_line"), b.get("to_line"))
        for b in summary.get("uncovered_branches") or []
    )
    pct = summary.get("line_coverage_percent")
    branch_pct = summary.get("branch_coverage_percent")
    return f"{pct}|{branch_pct}|{missing}|{gaps}|{branches}"
