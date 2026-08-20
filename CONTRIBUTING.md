# Contributing to RepoRamp

Thanks for taking a look at `RepoRamp`.

This project is intentionally small and local-first. Good contributions usually
make the tool more reliable, easier to understand, or more useful for real
repository onboarding work.

## Good First Contribution Areas

- add or improve fixture repositories under `tests/fixtures`
- improve entry-point or config-file heuristics for common Python layouts
- tighten summary wording without making it less deterministic
- add tests for a real-world repository shape that currently behaves poorly
- improve documentation for maintainers, contributors, and reviewers

## Development Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
pytest -q
```

## Project Principles

- Keep the tool deterministic and explainable.
- Prefer narrow, testable heuristics over broad magic.
- Avoid hosted dependencies or model APIs in core workflows.
- Keep the CLI easy to inspect and easy to contribute to.

## Before Opening a Pull Request

Please make sure you:

1. add or update tests when behavior changes
2. keep scope tight to one improvement at a time
3. update docs if the user-facing behavior changes
4. run `pytest -q`

## Design Notes

`RepoRamp` is for repository understanding, not code generation. If a proposed
change makes the tool feel more like a general-purpose chat assistant than a
repository orientation CLI, it is probably out of scope for this project.
