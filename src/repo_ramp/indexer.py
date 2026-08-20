from __future__ import annotations

import ast
from pathlib import Path

from .models import RepositoryIndex

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python 3.10 fallback
    import tomli as tomllib


CONFIG_NAMES = {"pyproject.toml", "setup.py", "setup.cfg", "pytest.ini", "tox.ini"}
README_NAMES = {"README.md", "README.rst", "README.txt"}


def _record_framework_hint(index: RepositoryIndex, hint: str) -> None:
    if hint not in index.framework_hints:
        index.framework_hints.append(hint)


def _record_key_file(index: RepositoryIndex, path: str, reason: str) -> None:
    if not any(item["path"] == path for item in index.key_files):
        index.key_files.append({"path": path, "reason": reason})


def _analyze_python_file(root: Path, path: Path, index: RepositoryIndex) -> None:
    rel = path.relative_to(root).as_posix()

    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except SyntaxError:
        index.skipped_files.append(rel)
        return

    imports: list[str] = []
    has_main_block = False

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.append(node.module)
        elif isinstance(node, ast.If):
            test = node.test
            if (
                isinstance(test, ast.Compare)
                and isinstance(test.left, ast.Name)
                and test.left.id == "__name__"
                and len(test.ops) == 1
                and isinstance(test.ops[0], ast.Eq)
                and len(test.comparators) == 1
                and isinstance(test.comparators[0], ast.Constant)
                and test.comparators[0].value == "__main__"
            ):
                has_main_block = True

    if has_main_block:
        index.entry_points.append({"path": rel, "reason": "__main__ block"})
    elif rel.endswith(("main.py", "app.py", "cli.py", "__main__.py")):
        index.entry_points.append({"path": rel, "reason": "conventional entry-style filename"})

    if any(name.startswith("typer") for name in imports):
        _record_framework_hint(index, "typer")
    if any(name.startswith("fastapi") for name in imports):
        _record_framework_hint(index, "fastapi")

    if rel.endswith(("main.py", "app.py", "cli.py")):
        _record_key_file(index, rel, "likely startup or high-value module")


def build_index(root: Path) -> RepositoryIndex:
    index = RepositoryIndex(root=str(root.resolve()))

    for path in root.rglob("*"):
        if path.is_dir():
            continue

        rel = path.relative_to(root).as_posix()

        if path.name in README_NAMES:
            index.readme_files.append(rel)

        if path.name in CONFIG_NAMES:
            index.config_files.append(rel)
            _record_key_file(index, rel, "project configuration")

        if path.suffix == ".py":
            index.python_files.append(rel)
            _analyze_python_file(root, path, index)

            if rel.startswith("tests/") or path.name.startswith("test_") or path.name.endswith("_test.py"):
                index.test_files.append(rel)

        if path.name == "__init__.py" and path.parent != root:
            index.package_roots.append(path.parent.relative_to(root).as_posix())

    pyproject = root / "pyproject.toml"
    if pyproject.exists():
        data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
        index.project_name = data.get("project", {}).get("name")

    return index
