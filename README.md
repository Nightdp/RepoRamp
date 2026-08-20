# RepoRamp

[![Tests](https://github.com/Nightdp/reposense-py/actions/workflows/test.yml/badge.svg)](https://github.com/Nightdp/reposense-py/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)

`RepoRamp` is a local-first CLI for understanding unfamiliar Python repositories quickly.

It helps contributors, maintainers, and reviewers answer the first few questions that slow down every handoff:

- What does this repository do?
- Where is the entry point?
- Which files should I read first?
- Where are the tests and configuration files?

`RepoRamp` stays intentionally simple:

- local-first and offline
- deterministic terminal output
- no model API required
- focused on repository orientation, not code generation

## Project Status

`RepoRamp` is an early-stage open source tool with a working CLI, fixture-backed
tests, and a deliberately narrow scope.

The near-term focus is:

- better Python repository coverage
- clearer maintainer-oriented summaries
- more fixture repositories from real-world layouts
- a contributor experience that stays lightweight and approachable

## Why This Project Exists

A lot of open source friction is not "writing code" but getting oriented inside a new codebase fast enough to make a useful change.

`RepoRamp` is built for that first 10-minute onboarding window. It scans a Python repository, extracts lightweight structural signals, and turns them into a summary you can actually use before making edits.

That makes it a good fit for:

- first-time contributors exploring an unfamiliar repo
- maintainers reviewing small utilities and dependencies
- developers returning to an older internal or OSS project
- people triaging bugs in a codebase they did not originally write

## What RepoRamp Does Today

`RepoRamp` builds a lightweight repository index from filesystem structure, Python AST parsing, and common project metadata.

Current capabilities:

- detect likely entry points
- surface configuration files
- locate tests and package roots
- highlight important files with short reasons
- answer a constrained set of repository-orientation questions

## Quickstart

```bash
python -m venv .venv
.venv/Scripts/activate
pip install -e ".[dev]"
reporamp --version
python -m repo_ramp --version
reporamp summary path/to/repo
reporamp summary path/to/repo --markdown
reporamp summary path/to/repo --json
reporamp summary path/to/repo --markdown --output summary.md
reporamp files path/to/repo
reporamp files path/to/repo --json
reporamp files path/to/repo --output key-files.txt
reporamp ask path/to/repo "Where is the config?"
reporamp ask path/to/repo "Where is the config?" --json
reporamp ask path/to/repo "Where is the config?" --json --output config.json
```

If you only want the runtime install without test tooling, `pip install -e .`
still works.

## Local Development

Use the dev extra for the shortest contributor setup path:

```bash
python -m venv .venv
.venv/Scripts/activate
pip install -e ".[dev]"
python -m repo_ramp --version
python -m repo_ramp summary tests/fixtures/basic_cli --markdown
pytest -q
```

That makes quick local verification a little easier for contributors and
evaluators who want to run the project before installing the console script
globally.

## Demo

Real CLI examples live in [examples/demo-session.md](./examples/demo-session.md).

Here is a short sample from the current tool:

```text
Repository: tool-cli

Entry Points:
- tool_cli/cli.py (__main__ block)

Tests:
- none detected

Suggested Reading Order:
- pyproject.toml: project configuration
- tool_cli/cli.py: likely startup or high-value module

Framework Hints:
- typer
```

## Project Docs

If you are evaluating the project quickly, these are the best next reads:

- [Architecture](./docs/architecture.md)
- [Roadmap](./docs/roadmap.md)
- [Release Preview](./docs/releases/v0.1.0-preview.md)
- [Contributing Guide](./CONTRIBUTING.md)

## Why Maintainers Might Use It

`RepoRamp` is designed for the repeated work around open source maintenance, not
just one-off demos.

- onboarding a new contributor to an unfamiliar part of the repo
- getting a fast structural read before reviewing a PR
- triaging issues in a codebase you have not touched recently
- checking a small dependency or utility before adopting it

## Commands

- `reporamp summary <path>` prints a deterministic repository overview.
- `reporamp summary <path> --markdown` renders the same overview as Markdown.
- `reporamp summary <path> --json` renders the overview as structured JSON.
- `reporamp summary <path> --output <file>` writes the rendered summary to a file.
- `reporamp files <path>` lists the most important files and why they matter.
- `reporamp files <path> --json` renders key-file suggestions as structured JSON.
- `reporamp files <path> --output <file>` writes the file report to a file.
- `reporamp ask <path> "<question>"` answers supported repository-orientation questions.
- `reporamp ask <path> "<question>" --json` returns structured question/answer output.
- `reporamp ask <path> "<question>" --output <file>` writes the rendered answer to a file.

## Example Questions

```bash
reporamp ask path/to/repo "Where is the config?"
reporamp ask path/to/repo "Where are the tests?"
reporamp ask path/to/repo "Which files should I read first?"
reporamp ask path/to/repo "What is the package layout?"
reporamp ask path/to/repo "How does this project start?"
```

## Project Scope

`RepoRamp` is deliberately narrow in the first release.

In scope:

- Python repositories
- CLI tools, libraries, `src/` layouts, and simple web apps
- explainable heuristics over opaque scoring

Out of scope:

- editing or refactoring code
- free-form chat
- multi-language analysis
- cloud-only or paid-API workflows

## Why It Fits Open Source Workflows

For open source maintainers, repository understanding is a repeated maintenance task:

- onboarding contributors
- reviewing pull requests in unfamiliar areas
- checking small dependencies before adoption
- documenting project structure for new users

`RepoRamp` aims to make that workflow faster with a tool that is transparent, testable, and useful even without any hosted service.

## Current Status

This project is early-stage, but it already has:

- a working CLI
- fixture-backed tests
- deterministic outputs suitable for demos and CI checks
- a codebase small enough for contributors to understand quickly
- a public contribution guide
- a CI workflow that runs the test suite on push and pull request
- real example output checked into the repository for quick evaluation
- a public roadmap and initial release notes for evaluators

## Roadmap

The short version:

- broader framework hints for common Python stacks
- better ranking for "read this first" files
- richer summaries for `pyproject.toml` and package scripts
- file export for docs and onboarding workflows

More detail lives in [docs/roadmap.md](./docs/roadmap.md).

If you want the first-release framing, see
[docs/releases/v0.1.0-preview.md](./docs/releases/v0.1.0-preview.md).

If you want the implementation overview, see
[docs/architecture.md](./docs/architecture.md).

## Contributing

If you want to help, good contribution areas include:

- more Python fixture repositories
- better heuristics for entry-point detection
- clearer summary formatting
- support for more real-world project layouts

See [CONTRIBUTING.md](./CONTRIBUTING.md) for setup, scope, and pull request
expectations.

## License

This project is available under the [MIT License](./LICENSE).
