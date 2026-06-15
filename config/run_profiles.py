from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, Iterator, Literal

from config.settings import settings

RagMode = Literal["none", "limited", "full"]
ProfileName = Literal["sem-rag", "rag-limitado", "rag-completo", "com-cache"]

_LIMITED_OVERRIDES: dict[str, Any] = {
    "PROMPT_MAX_RAG_TOTAL_CHARS": 600,
    "PROMPT_MAX_RAG_SNIPPET_CHARS": 150,
    "RETRIEVER_TOP_K_FUNCTIONS": 1,
    "RETRIEVER_TOP_K_TESTS": 1,
    "RETRIEVER_RERANK_POOL_SIZE": 5,
}


@dataclass(frozen=True)
class RunProfile:
    """Preset de execução para comparar RAG e cache."""

    name: ProfileName
    label: str
    rag_mode: RagMode
    generation_cache_enabled: bool
    setting_overrides: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "label": self.label,
            "rag_mode": self.rag_mode,
            "generation_cache_enabled": self.generation_cache_enabled,
            "setting_overrides": self.setting_overrides,
        }


PROFILES: dict[str, RunProfile] = {
    "sem-rag": RunProfile(
        name="sem-rag",
        label="Sem RAG, sem cache",
        rag_mode="none",
        generation_cache_enabled=False,
        setting_overrides={},
    ),
    "rag-limitado": RunProfile(
        name="rag-limitado",
        label="RAG limitado (orçamento reduzido), sem cache",
        rag_mode="limited",
        generation_cache_enabled=False,
        setting_overrides=_LIMITED_OVERRIDES,
    ),
    "rag-completo": RunProfile(
        name="rag-completo",
        label="RAG completo, sem cache",
        rag_mode="full",
        generation_cache_enabled=False,
        setting_overrides={},
    ),
    "com-cache": RunProfile(
        name="com-cache",
        label="RAG completo, com cache de geração",
        rag_mode="full",
        generation_cache_enabled=True,
        setting_overrides={},
    ),
}

PROFILE_CHOICES: list[str] = list(PROFILES.keys())

_active_profile: str | None = None


def get_active_profile() -> RunProfile | None:
    if _active_profile is None:
        return None
    return PROFILES[_active_profile]


def describe_profiles() -> str:
    lines = ["Perfis disponíveis (--profile):"]
    for name in PROFILE_CHOICES:
        profile = PROFILES[name]
        lines.append(f"  {name:14} {profile.label}")
    return "\n".join(lines)


@contextmanager
def apply_run_profile(profile_name: str) -> Iterator[RunProfile]:
    """Aplica overrides do perfil e restaura settings ao sair."""
    global _active_profile

    if profile_name not in PROFILES:
        raise ValueError(f"Perfil desconhecido: {profile_name!r}")

    profile = PROFILES[profile_name]
    override_keys = ["RAG_MODE", "GENERATION_CACHE_ENABLED", *profile.setting_overrides]
    snapshot = {key: getattr(settings, key) for key in override_keys}

    settings.RAG_MODE = profile.rag_mode
    settings.GENERATION_CACHE_ENABLED = profile.generation_cache_enabled
    for key, value in profile.setting_overrides.items():
        setattr(settings, key, value)

    _active_profile = profile_name
    try:
        yield profile
    finally:
        for key, value in snapshot.items():
            setattr(settings, key, value)
        _active_profile = None
