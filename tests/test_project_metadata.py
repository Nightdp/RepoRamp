from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_pyproject_declares_release_metadata() -> None:
    pyproject = (PROJECT_ROOT / "pyproject.toml").read_text(encoding="utf-8")

    assert 'license = { file = "LICENSE" }' in pyproject
    assert "keywords = [" in pyproject
    assert "classifiers = [" in pyproject
    assert "[project.urls]" in pyproject


def test_pyproject_declares_dev_extra() -> None:
    pyproject = (PROJECT_ROOT / "pyproject.toml").read_text(encoding="utf-8")

    assert "[project.optional-dependencies]" in pyproject
    assert 'dev = ["pytest' in pyproject


def test_ci_installs_dev_extra() -> None:
    workflow = (PROJECT_ROOT / ".github" / "workflows" / "test.yml").read_text(
        encoding="utf-8"
    )

    assert 'pip install -e ".[dev]"' in workflow


def test_gitignore_covers_pytest_temp_directories() -> None:
    gitignore = (PROJECT_ROOT / ".gitignore").read_text(encoding="utf-8")

    assert "pytest-of-*/" in gitignore
