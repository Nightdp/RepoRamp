from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python 3.10 fallback
    import tomli as tomllib


def test_project_metadata_uses_repo_ramp_names() -> None:
    data = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))

    assert data["project"]["name"] == "repo-ramp"
    assert data["project"]["scripts"]["reporamp"] == "repo_ramp.cli:app"
