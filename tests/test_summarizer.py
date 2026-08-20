from pathlib import Path

from repo_ramp.indexer import build_index
from repo_ramp.summarizer import render_summary


def test_render_summary_lists_project_shape_and_entry_points() -> None:
    index = build_index(Path("tests/fixtures/src_layout"))

    output = render_summary(index)

    assert "Repository: pkgdemo" in output
    assert "Entry Points" in output
    assert "src/pkgdemo/app.py" in output
    assert "Suggested Reading Order" in output


def test_summary_mentions_tests_and_framework_hints() -> None:
    index = build_index(Path("tests/fixtures/web_app"))

    output = render_summary(index)

    assert "Tests" in output
    assert "fastapi" in output.lower()
