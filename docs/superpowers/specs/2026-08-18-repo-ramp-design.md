# RepoRamp Design

## Summary

`repo-ramp` is a local-first CLI that helps developers understand unfamiliar Python repositories quickly. It scans a repository, builds a lightweight structured index from source code and project metadata, then uses that index to produce summaries and answer a limited set of repository-understanding questions.

The first release should feel like a dependable developer tool rather than an experimental AI assistant. It should work offline, avoid paid APIs, and favor deterministic output over open-ended generation.

## Problem

Developers regularly lose time when joining a new project, reviewing an unfamiliar repository, or returning to an old codebase. The first questions are usually repetitive:

- What does this repository do?
- Where is the main entry point?
- Which files should I read first?
- How is the code organized?
- Where are the tests and configuration files?

Existing tooling can search for symbols and list files, but it rarely converts raw structure into a clear repository-level explanation. `repo-ramp` fills that gap for Python repositories.

## Goals

- Provide a fast way to understand an unfamiliar Python repository from the command line.
- Work without any network dependency or model API.
- Surface the most important files, modules, entry points, configuration files, and test locations.
- Support both one-shot summaries and constrained question answering backed by a local index.
- Produce outputs that are useful in terminals, docs, demos, and screenshots.

## Non-Goals

- Editing source code or applying automatic fixes.
- Supporting every programming language in the first release.
- Providing free-form chat with arbitrary reasoning quality.
- Building an IDE extension, daemon, or web service in the first release.
- Performing deep semantic program analysis such as full call graphs or type inference.

## Target User

The primary user is a developer who has just opened an unfamiliar Python repository and wants a reliable orientation pass before making changes.

Typical scenarios:

- A contributor evaluating whether to submit a patch.
- An engineer onboarding to an internal or open-source project.
- A maintainer reviewing a dependency or reference implementation.
- A developer triaging a bug in a repository they have not seen before.

## User Experience

The first release exposes four commands:

### `reporamp index <path>`

Scans the repository and stores a local JSON index. This command is explicit so users can inspect or refresh the index when the repository changes.

### `reporamp summary <path>`

Prints a concise summary of the repository, including:

- project identity inferred from metadata and README
- likely application type
- likely entry points
- important top-level packages and files
- test layout
- configuration and dependency signals
- recommended reading order

### `reporamp ask <path> "<question>"`

Answers a narrow set of supported questions using the local index. The first release should explicitly support questions in these categories:

- entry points
- configuration files
- tests
- package or module layout
- likely startup flow
- files worth reading first

If a question falls outside the supported categories, the CLI should say so clearly rather than pretending to know.

### `reporamp files <path>`

Prints the key files detected during indexing, grouped by role such as entry points, configuration, tests, packaging, documentation, and core modules.

## Scope Boundaries

The first release should only target Python repositories with common layouts such as:

- flat package repositories
- `src/` layout packages
- CLI tools
- web apps with recognizable framework conventions
- libraries with test directories

The first release may use heuristics for frameworks such as FastAPI, Flask, Django, and Typer, but these heuristics should remain shallow and readable.

## Architecture

The tool should be organized as a small set of focused modules:

- `cli.py`: command definitions and output formatting
- `indexer.py`: filesystem scan and repository index construction
- `summarizer.py`: summary generation from the index
- `question_router.py`: supported question detection and answer generation
- `models.py`: typed index structures

This keeps data gathering, interpretation, and presentation separate. The design should stay simple enough that contributors can understand the whole codebase quickly.

## Repository Index Model

The local index should be stored as JSON and contain only the data needed for user-facing commands. The model should include:

- repository root path
- detected package roots
- Python modules discovered
- classes and top-level functions per file
- imports per file
- likely entry point files and why they were marked
- detected config files
- detected packaging metadata files
- detected test files and test directories
- README presence and extracted high-level signals
- framework hints
- key-file ranking with short reasons

The index format should be deterministic and human-inspectable so users can debug why the tool produced a given answer.

## Analysis Strategy

Indexing should combine four lightweight passes:

1. Metadata pass
   Read `pyproject.toml`, `requirements*.txt`, `setup.py`, `setup.cfg`, and similar files to infer package name, scripts, dependencies, and project type signals.

2. Documentation pass
   Read `README` files and capture the repository title, quick description, installation hints, usage examples, and mentions of major commands or frameworks when easily detectable.

3. Filesystem pass
   Walk the repository and classify directories and files into buckets such as source, tests, docs, configuration, CI, and packaging.

4. AST pass
   Parse Python files with the standard library `ast` module to detect modules, classes, top-level functions, imports, `if __name__ == "__main__"` blocks, decorators, and framework-specific clues.

The tool should skip obviously irrelevant directories like `.git`, virtual environments, and cache folders.

## Heuristics

The first release should use explainable heuristics rather than opaque scoring. Examples:

- mark a file as an entry point if it contains `if __name__ == "__main__"` or is referenced by packaging scripts
- boost files named `main.py`, `app.py`, `cli.py`, `manage.py`, or package `__main__.py`
- detect test locations from `tests/`, `test_*.py`, and `*_test.py`
- detect configuration from common filenames such as `.env.example`, `pyproject.toml`, `tox.ini`, `pytest.ini`, and framework config modules
- detect likely frameworks from imports and dependency metadata

Every surfaced “important file” should include a short reason generated from these heuristics.

## Summary Output

`summary` output should favor structured terminal text over paragraphs. A good default layout is:

- repository name and likely type
- one short description
- entry points
- important files
- package layout
- tests
- configuration
- suggested reading order

This format is easy to scan and easy to share in screenshots or documentation.

## Question Answering

`ask` should not be a general natural-language engine. It should classify the question into one of the supported categories, then answer from the index with a template-driven response.

Examples of supported questions:

- "How do I start this project?"
- "Where is the config?"
- "Which files should I read first?"
- "Where are the tests?"
- "What is the main package?"

If classification confidence is low, the tool should respond with a supported-question hint and suggest `summary` or `files`.

## Error Handling

Error handling should stay practical:

- if the path does not exist, fail with a clear message
- if the repository has no Python files, say that Python analysis is unavailable
- if some files fail AST parsing, continue indexing and report the skipped files count
- if an index is missing for `summary`, `ask`, or `files`, either build one automatically or print the exact command to run

The first release should prefer clear messages over complex recovery flows.

## Testing Strategy

The project should include automated tests around fixture repositories. The initial test matrix should cover:

- a small library-style repository
- a CLI-style repository
- a web-app-style repository with recognizable imports
- a repository with `src/` layout
- a repository containing syntax errors in one file

Core assertions should verify:

- entry point detection
- test detection
- configuration detection
- package discovery
- summary rendering
- supported-question routing

## Packaging And Distribution

The project should ship as a normal Python package installable with `pip`. The CLI entry point should be exposed through `pyproject.toml`.

Distribution priorities for the first release:

- easy local install for contributors
- simple `pip` install path for users
- clear README examples

No plugin system or extra packaging complexity is needed in the first release.

## Success Criteria

The first release is successful if:

- a user can run the CLI on a small or medium Python repository and get a useful summary in seconds
- the reported entry points, config files, and test locations are usually correct on supported layouts
- the command output is deterministic enough for tests and demos
- the codebase stays small, readable, and contributor-friendly

## Future Extensions

These are intentionally out of scope for the first release, but the architecture should not block them later:

- optional LLM-backed richer answers
- multi-language support
- editor integrations
- markdown or JSON export modes
- repository diff understanding

## Initial Release Plan Shape

The implementation plan should focus on:

- project skeleton and packaging
- typed index model
- repository scanner and AST extraction
- summary generation
- constrained question routing
- fixture-based tests
- README and release polish
