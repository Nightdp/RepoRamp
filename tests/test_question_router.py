from pathlib import Path

from repo_ramp.indexer import build_index
from repo_ramp.question_router import answer_question


def test_answer_question_handles_config_lookup() -> None:
    index = build_index(Path("tests/fixtures/web_app"))

    answer = answer_question(index, "Where is the config?")

    assert "pyproject.toml" in answer


def test_answer_question_rejects_unsupported_prompts() -> None:
    index = build_index(Path("tests/fixtures/web_app"))

    answer = answer_question(index, "Refactor this project for me")

    assert "Supported questions" in answer


def test_answer_question_handles_package_layout_lookup() -> None:
    index = build_index(Path("tests/fixtures/src_layout"))

    answer = answer_question(index, "What is the package layout?")

    assert "Package roots:" in answer
    assert "src/pkgdemo" in answer


def test_answer_question_handles_startup_flow_lookup() -> None:
    index = build_index(Path("tests/fixtures/basic_cli"))

    answer = answer_question(index, "How does this project start?")

    assert "Startup flow:" in answer
    assert "tool_cli/cli.py (__main__ block)" in answer
    assert "pyproject.toml" in answer
