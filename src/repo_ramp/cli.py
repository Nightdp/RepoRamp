from pathlib import Path
import json

import typer

from . import __version__
from .indexer import build_index
from .question_router import SUPPORTED_PATTERNS, answer_question
from .summarizer import render_summary


app = typer.Typer(help="Understand unfamiliar Python repositories.")


QUESTION_MATCH_ORDER = (
    "config",
    "tests",
    "startup_flow",
    "package_layout",
    "entry_points",
    "reading_order",
)


def _detect_question_type(question: str) -> str:
    lowered = question.lower()

    for key in QUESTION_MATCH_ORDER:
        if any(token in lowered for token in SUPPORTED_PATTERNS[key]):
            return key

    return "unsupported"


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"RepoRamp {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        False,
        "--version",
        callback=_version_callback,
        is_eager=True,
        help="Show RepoRamp version and exit.",
    ),
) -> None:
    """RepoRamp command line interface."""


@app.command()
def summary(
    path: str,
    markdown: bool = False,
    json_output: bool = typer.Option(False, "--json"),
    output: Path | None = typer.Option(None, "--output", "-o"),
) -> None:
    """Summarize a Python repository."""
    index = build_index(Path(path))
    rendered = render_summary(index, markdown=markdown, json_output=json_output)

    if output is not None:
        output.write_text(rendered, encoding="utf-8")
        typer.echo(f"Wrote summary to {output}")
        return

    typer.echo(render_summary(index, markdown=markdown, json_output=json_output))


@app.command()
def index(path: str) -> None:
    """Index a Python repository."""
    raise typer.Exit(code=0)


@app.command()
def files(
    path: str,
    json_output: bool = typer.Option(False, "--json"),
    output: Path | None = typer.Option(None, "--output", "-o"),
) -> None:
    """Show key files in a Python repository."""
    index = build_index(Path(path))

    rendered = (
        json.dumps(index.key_files, indent=2)
        if json_output
        else "\n".join(f"{item['path']}: {item['reason']}" for item in index.key_files)
    )

    if output is not None:
        output.write_text(rendered, encoding="utf-8")
        typer.echo(f"Wrote files report to {output}")
        return

    if json_output:
        typer.echo(rendered)
        return

    typer.echo(rendered)


@app.command()
def ask(
    path: str,
    question: str,
    json_output: bool = typer.Option(False, "--json"),
    output: Path | None = typer.Option(None, "--output", "-o"),
) -> None:
    """Answer a supported repository question."""
    index = build_index(Path(path))
    answer = answer_question(index, question)

    rendered = answer

    if json_output:
        payload = {
            "question": question,
            "match_type": _detect_question_type(question),
            "answer": answer,
        }
        rendered = json.dumps(payload, indent=2)

    if output is not None:
        output.write_text(rendered, encoding="utf-8")
        typer.echo(f"Wrote answer to {output}")
        return

    typer.echo(rendered)
