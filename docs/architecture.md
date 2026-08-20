# RepoRamp Architecture

`RepoRamp` is intentionally small.

The architecture favors local filesystem inspection, deterministic heuristics,
and code paths that contributors can understand quickly without reading a large
framework or service layer.

## Design Goals

- stay local-first and offline
- prefer explainable heuristics over opaque scoring
- keep output deterministic for docs, CI, and demos
- keep the codebase small enough for first-time contributors to navigate

## Request Flow

At a high level, every CLI request follows the same path:

1. `repo_ramp.cli` parses the command and options with Typer.
2. `repo_ramp.indexer` walks the target repository and builds a `RepositoryIndex`.
3. One formatter layer renders that index into terminal text, Markdown, or JSON.
4. The CLI prints the result or writes it to a file when `--output` is used.

That shared flow is why `summary`, `files`, and `ask` stay lightweight. They do
not maintain separate repository models or hidden caches.

## Core Components

### `repo_ramp.cli`

The CLI module defines the user-facing commands and keeps command behavior
simple:

- `summary` renders a repository overview
- `files` returns the key files and their reasons
- `ask` answers a constrained set of repository-orientation questions

The CLI does not try to own repository analysis rules. It coordinates the
indexing and rendering layers.

### `repo_ramp.indexer`

The indexer is the main analysis layer.

It walks the repository tree, records candidate config files, package roots,
tests, likely entry points, and framework hints, then stores those findings in a
single `RepositoryIndex` object.

Current heuristics are intentionally narrow:

- filename-based entry-point hints for files like `main.py`, `app.py`, and `cli.py`
- AST inspection for `if __name__ == "__main__"` blocks
- light framework hinting from imports such as `typer` and `fastapi`
- `pyproject.toml` parsing for the project name

### `repo_ramp.models`

`RepositoryIndex` is the shared data contract between the indexing layer and the
rendering/answering layers.

Keeping this model small helps the project stay understandable and makes new
heuristics easier to add without introducing unnecessary abstraction.

### `repo_ramp.summarizer`

The summarizer turns a `RepositoryIndex` into deterministic output formats:

- plain terminal text
- Markdown
- JSON

This separation keeps formatting concerns out of the indexing layer.

### `repo_ramp.question_router`

The question router handles the project's constrained Q&A mode.

Instead of free-form chat, it maps a small set of supported question patterns to
structured answers derived from the same repository index used by the other
commands.

## Why The Project Stays Narrow

`RepoRamp` is not trying to become a coding agent or general repository copilot.

The narrow scope keeps the project useful for a specific job:

- get oriented in an unfamiliar Python repository quickly
- surface the files a contributor should inspect first
- support maintainers and reviewers with deterministic outputs

That constraint is also what keeps the codebase contributor-friendly.

## Extension Points

The most natural places to extend the project are:

- add more fixture repositories under `tests/fixtures`
- improve framework hint detection in `repo_ramp.indexer`
- improve rendered summaries without breaking determinism
- add new supported question patterns when they map cleanly to repository structure

Extensions that would require hidden services, non-deterministic behavior, or
free-form generation are intentionally out of scope.
