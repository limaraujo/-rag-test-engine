from __future__ import annotations

import ast
from pathlib import Path


def module_name_from_path(root: Path, file_path: Path) -> str:
    relative = file_path.relative_to(root)
    parts = list(relative.parts)
    if parts[-1] == "__init__.py":
        parts = parts[:-1]
    else:
        parts[-1] = parts[-1].removesuffix(".py")
    return ".".join(parts)


def package_name(module_name: str) -> str:
    if "." not in module_name:
        return ""
    return module_name.rsplit(".", 1)[0]


class ImportResolver:
    """Resolve import and name references within a module using AST metadata."""

    def __init__(self, module_name: str, local_modules: set[str] | None = None) -> None:
        self.module_name = module_name
        self.local_modules = local_modules or set()
        self._aliases: dict[str, str] = {}

    def register_import(self, node: ast.Import) -> list[str]:
        dependencies: list[str] = []
        for alias in node.names:
            target = alias.name
            bound_name = alias.asname or alias.name.split(".", 1)[0]
            self._aliases[bound_name] = target
            dependencies.append(target)
        return dependencies

    def register_import_from(self, node: ast.ImportFrom) -> list[str]:
        base_module = self._resolve_relative_module(node.module, node.level)
        dependencies: list[str] = []

        if base_module:
            dependencies.append(base_module)

        for alias in node.names:
            if alias.name == "*":
                continue

            bound_name = alias.asname or alias.name
            if base_module:
                target = f"{base_module}.{alias.name}"
            else:
                target = alias.name

            self._aliases[bound_name] = target
            dependencies.append(target)

        return dependencies

    def resolve_name(self, name: str) -> str:
        if name in self._aliases:
            return self._aliases[name]
        return name

    def resolve_reference(self, node: ast.AST) -> str | None:
        if isinstance(node, ast.Name):
            return self.resolve_name(node.id)

        if isinstance(node, ast.Attribute):
            parent = self.resolve_reference(node.value)
            if parent:
                return f"{parent}.{node.attr}"
            return node.attr

        if isinstance(node, ast.Subscript):
            return self.resolve_reference(node.value)

        if isinstance(node, ast.Call):
            return self.resolve_reference(node.func)

        return None

    def populate_from_tree(self, tree: ast.AST) -> None:
        for node in tree.body:
            if isinstance(node, ast.Import):
                self.register_import(node)
            elif isinstance(node, ast.ImportFrom):
                self.register_import_from(node)

    @classmethod
    def from_import_strings(
        cls,
        module_name: str,
        imports: list[str],
    ) -> ImportResolver:
        resolver = cls(module_name)
        for imported in imports:
            if "." in imported:
                bound_name = imported.rsplit(".", 1)[-1]
            else:
                bound_name = imported
            resolver._aliases[bound_name] = imported
        return resolver

    def _resolve_relative_module(
        self,
        module: str | None,
        level: int,
    ) -> str | None:
        if level == 0:
            return module

        package_parts = package_name(self.module_name).split(".")
        if not package_parts or package_parts == [""]:
            package_parts = []

        if level > len(package_parts) + 1:
            return None

        parent_parts = package_parts[: len(package_parts) - level + 1]
        if module:
            return ".".join([*parent_parts, module]) if parent_parts else module
        return ".".join(parent_parts) if parent_parts else None
