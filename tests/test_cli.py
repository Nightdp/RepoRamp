import json
import os
import subprocess
import sys
from pathlib import Path

from typer.testing import CliRunner

from repo_ramp.cli import app


runner = CliRunner()
PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_root_version_option_prints_version() -> None:
    result = runner.invoke(app, ["--version"])

    assert result.exit_code == 0
    assert result.stdout == "RepoRamp 0.1.0\n"


def test_module_entrypoint_prints_version() -> None:
    env = os.environ.copy()
    existing_pythonpath = env.get("PYTHONPATH")
    env["PYTHONPATH"] = (
        f"src{os.pathsep}{existing_pythonpath}" if existing_pythonpath else "src"
    )

    result = subprocess.run(
        [sys.executable, "-m", "repo_ramp", "--version"],
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT,
        env=env,
        check=False,
    )

    assert result.returncode == 0
    assert result.stdout == "RepoRamp 0.1.0\n"


def test_summary_command_is_registered() -> None:
    result = runner.invoke(app, ["summary", "--help"])
    assert result.exit_code == 0
    assert "Summarize a Python repository" in result.stdout


def test_files_command_lists_key_files() -> None:
    result = runner.invoke(app, ["files", "tests/fixtures/web_app"])

    assert result.exit_code == 0
    assert "webapp/main.py" in result.stdout
    assert "pyproject.toml" in result.stdout


def test_files_command_supports_json_output() -> None:
    result = runner.invoke(app, ["files", "tests/fixtures/web_app", "--json"])

    assert result.exit_code == 0

    payload = json.loads(result.stdout)

    assert payload[0]["path"] == "pyproject.toml"
    assert payload[0]["reason"] == "project configuration"
    assert payload[1]["path"] == "webapp/main.py"


def test_files_command_can_write_output_to_file(tmp_path) -> None:
    output_path = tmp_path / "files.txt"

    result = runner.invoke(
        app,
        ["files", "tests/fixtures/web_app", "--output", str(output_path)],
    )

    assert result.exit_code == 0
    assert result.stdout == f"Wrote files report to {output_path}\n"

    rendered = output_path.read_text(encoding="utf-8")

    assert "pyproject.toml: project configuration" in rendered
    assert "webapp/main.py: likely startup or high-value module" in rendered


def test_ask_command_supports_json_output() -> None:
    result = runner.invoke(
        app,
        ["ask", "tests/fixtures/basic_cli", "How does this project start?", "--json"],
    )

    assert result.exit_code == 0

    payload = json.loads(result.stdout)

    assert payload["question"] == "How does this project start?"
    assert payload["match_type"] == "startup_flow"
    assert "tool_cli/cli.py (__main__ block)" in payload["answer"]


def test_ask_command_json_output_marks_unsupported_questions() -> None:
    result = runner.invoke(
        app,
        ["ask", "tests/fixtures/web_app", "Refactor this project for me", "--json"],
    )

    assert result.exit_code == 0

    payload = json.loads(result.stdout)

    assert payload["match_type"] == "unsupported"
    assert "Supported questions" in payload["answer"]


def test_ask_command_can_write_json_output_to_file(tmp_path) -> None:
    output_path = tmp_path / "answer.json"

    result = runner.invoke(
        app,
        [
            "ask",
            "tests/fixtures/basic_cli",
            "How does this project start?",
            "--json",
            "--output",
            str(output_path),
        ],
    )

    assert result.exit_code == 0
    assert result.stdout == f"Wrote answer to {output_path}\n"

    payload = json.loads(output_path.read_text(encoding="utf-8"))

    assert payload["question"] == "How does this project start?"
    assert payload["match_type"] == "startup_flow"
    assert "tool_cli/cli.py (__main__ block)" in payload["answer"]


def test_summary_command_supports_markdown_output() -> None:
    result = runner.invoke(app, ["summary", "tests/fixtures/basic_cli", "--markdown"])

    assert result.exit_code == 0
    assert "# Repository: tool-cli" in result.stdout
    assert "## Entry Points" in result.stdout
    assert "- `tool_cli/cli.py`" in result.stdout


def test_summary_command_supports_json_output() -> None:
    result = runner.invoke(app, ["summary", "tests/fixtures/basic_cli", "--json"])

    assert result.exit_code == 0

    payload = json.loads(result.stdout)

    assert payload["repository"] == "tool-cli"
    assert payload["entry_points"][0]["path"] == "tool_cli/cli.py"
    assert payload["suggested_reading_order"][0]["path"] == "pyproject.toml"
    assert payload["framework_hints"] == ["typer"]


def test_summary_command_can_write_markdown_to_file(tmp_path) -> None:
    output_path = tmp_path / "summary.md"

    result = runner.invoke(
        app,
        ["summary", "tests/fixtures/basic_cli", "--markdown", "--output", str(output_path)],
    )

    assert result.exit_code == 0
    assert result.stdout == f"Wrote summary to {output_path}\n"
    assert output_path.read_text(encoding="utf-8").startswith("# Repository: tool-cli")


def test_summary_command_can_write_json_to_file(tmp_path) -> None:
    output_path = tmp_path / "summary.json"

    result = runner.invoke(
        app,
        ["summary", "tests/fixtures/basic_cli", "--json", "--output", str(output_path)],
    )

    assert result.exit_code == 0
    assert result.stdout == f"Wrote summary to {output_path}\n"

    payload = json.loads(output_path.read_text(encoding="utf-8"))

    assert payload["repository"] == "tool-cli"
    assert payload["framework_hints"] == ["typer"]
