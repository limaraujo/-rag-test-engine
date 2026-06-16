from __future__ import annotations

import fnmatch
import re
from dataclasses import dataclass
from pathlib import Path

# Diretórios que nunca devem ser varridos ou lidos.
SENSITIVE_DIR_NAMES: frozenset[str] = frozenset(
    {
        ".ssh",
        ".gnupg",
        ".aws",
        ".azure",
        ".gcloud",
        "secrets",
        ".secrets",
        "private",
        ".private",
    }
)

# Nomes/globs de arquivo sensível (qualquer extensão).
SENSITIVE_FILE_GLOBS: tuple[str, ...] = (
    ".env",
    ".env.*",
    "*.pem",
    "*.key",
    "*.p12",
    "*.pfx",
    "*.jks",
    "id_rsa",
    "id_rsa.*",
    "id_ed25519",
    "id_ed25519.*",
    "credentials.json",
    "secrets.toml",
    "service-account*.json",
    "*.keystore",
)

# Padrões para auditoria de segredos em arquivos versionados (sem expor valores).
_AUDIT_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("openai_api_key", re.compile(r"\bsk-[a-zA-Z0-9]{20,}\b")),
    ("bearer_token", re.compile(r"\bBearer\s+[a-zA-Z0-9._-]{20,}\b", re.IGNORECASE)),
    (
        "env_secret_assignment",
        re.compile(
            r"(?im)^(?:export\s+)?(?:[A-Z0-9_]*(?:API_KEY|TOKEN|SECRET|PASSWORD)[A-Z0-9_]*)\s*=\s*['\"]?[^\s#'\"]{8,}['\"]?"
        ),
    ),
    ("private_key_block", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
)


@dataclass(frozen=True)
class SecretRisk:
    """Risco detectado em arquivo versionado (valor nunca exposto)."""

    path: str
    risk_type: str


def is_sensitive_dir_name(name: str) -> bool:
    if name in SENSITIVE_DIR_NAMES:
        return True
    if sys_platform_casefold(name) in {d.lower() for d in SENSITIVE_DIR_NAMES}:
        return True
    return False


def sys_platform_casefold(name: str) -> str:
    return name.casefold()


def is_sensitive_file_name(name: str) -> bool:
    if name == ".env" or name.startswith(".env."):
        return True
    return any(fnmatch.fnmatch(name, pattern) for pattern in SENSITIVE_FILE_GLOBS)


def is_sensitive_path(path: Path, root: Path | None = None) -> bool:
    """True se qualquer segmento do caminho ou o nome do arquivo for sensível."""
    resolved = path.resolve()
    parts = resolved.parts
    if root is not None:
        try:
            rel = resolved.relative_to(root.resolve())
            parts = rel.parts
        except ValueError:
            parts = path.parts

    if any(is_sensitive_dir_name(part) for part in parts[:-1]):
        return True
    if parts and is_sensitive_file_name(parts[-1]):
        return True
    return False


def _is_documentation_path(path: Path) -> bool:
    name = path.name.lower()
    if name in {"readme.md", ".env.example", "env.example"}:
        return True
    parts = {part.lower() for part in path.parts}
    return "docs" in parts


def audit_file_for_secrets(path: Path) -> list[SecretRisk]:
    """Varre um arquivo em busca de padrões de segredo; não retorna valores."""
    if not path.is_file():
        return []

    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return []

    risks: list[SecretRisk] = []
    rel = path.as_posix()
    for risk_type, pattern in _AUDIT_PATTERNS:
        if pattern.search(text):
            if risk_type == "openai_api_key" and _is_placeholder_key_file(path, text):
                continue
            if risk_type == "env_secret_assignment" and _is_documentation_path(path):
                continue
            risks.append(SecretRisk(path=rel, risk_type=risk_type))
    return risks


def _is_placeholder_key_file(path: Path, text: str) -> bool:
    name = path.name.lower()
    if name in {".env.example", "env.example"}:
        return True
    if "your-key" in text.lower() or "sk-your" in text.lower():
        return True
    if "test-key" in text.lower() or "mock" in text.lower():
        return True
    return False


def audit_tracked_files(repo_root: Path, tracked_paths: list[str]) -> list[SecretRisk]:
    """Audita arquivos versionados; retorna riscos sem expor conteúdo."""
    findings: list[SecretRisk] = []
    seen: set[tuple[str, str]] = set()
    for rel in tracked_paths:
        rel_path = Path(rel)
        if rel_path.name == ".env" or rel_path.name.startswith(".env."):
            key = (rel, "tracked_env_file")
            if key not in seen:
                seen.add(key)
                findings.append(SecretRisk(path=rel, risk_type="tracked_env_file"))
            continue

        if any(is_sensitive_file_name(rel_path.name) for _ in [0]):
            if rel_path.suffix.lower() in {".pem", ".key", ".p12", ".pfx", ".jks"}:
                key = (rel, "tracked_key_file")
                if key not in seen:
                    seen.add(key)
                    findings.append(SecretRisk(path=rel, risk_type="tracked_key_file"))

        full = repo_root / rel_path
        for risk in audit_file_for_secrets(full):
            key = (risk.path, risk.risk_type)
            if key not in seen:
                seen.add(key)
                findings.append(risk)
    return findings
