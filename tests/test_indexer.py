from pathlib import Path

from repo_ramp.indexer import build_index


def test_build_index_detects_basic_project_metadata() -> None:
    repo = Path("tests/fixtures/basic_lib")

    index = build_index(repo)

    assert index.project_name == "samplelib"
    assert "README.md" in index.readme_files
    assert "pyproject.toml" in index.config_files
    assert "samplelib" in index.package_roots


def test_build_index_detects_entry_points_from_main_blocks() -> None:
    repo = Path("tests/fixtures/basic_cli")

    index = build_index(repo)

    assert any(item["path"] == "tool_cli/cli.py" for item in index.entry_points)
    assert "typer" in index.framework_hints


def test_build_index_tracks_syntax_errors_without_crashing() -> None:
    repo = Path("tests/fixtures/syntax_error")

    index = build_index(repo)

    assert index.skipped_files == ["badpkg/broken.py"]
    assert "badpkg" in index.package_roots


def test_build_index_tracks_readme_and_docs_files() -> None:
    repo = Path("tests/fixtures/web_app")

    index = build_index(repo)

    assert "README.md" in index.readme_files
    assert "README.md" in index.documentation_files
    assert "docs/getting-started.md" in index.documentation_files


def test_build_index_surfaces_docs_in_key_file_reading_order() -> None:
    repo = Path("tests/fixtures/web_app")

    index = build_index(repo)

    assert index.key_files[:4] == [
        {"path": "pyproject.toml", "reason": "project configuration"},
        {"path": "README.md", "reason": "project overview and setup guide"},
        {"path": "docs/getting-started.md", "reason": "supplemental project documentation"},
        {"path": "webapp/main.py", "reason": "likely startup or high-value module"},
    ]
