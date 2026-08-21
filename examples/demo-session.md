# RepoRamp Demo Session

This file shows real output from the current CLI against the fixture
repositories in `tests/fixtures`.

## Show the installed version

Command:

```bash
reporamp --version
```

Output:

```text
RepoRamp 0.1.0
```

## Run the module entrypoint directly

Command:

```bash
python -m repo_ramp --version
```

Output:

```text
RepoRamp 0.1.0
```

## Summary a small CLI-style repository

Command:

```bash
reporamp summary tests/fixtures/basic_cli
```

Output:

```text
Repository: tool-cli

Entry Points:
- tool_cli/cli.py (__main__ block)

Tests:
- none detected

Documentation:
- README.md

Suggested Reading Order:
- pyproject.toml: project configuration
- tool_cli/cli.py: likely startup or high-value module

Framework Hints:
- typer
```

## List key files for a small web-style repository

Command:

```bash
reporamp files tests/fixtures/web_app
```

Output:

```text
pyproject.toml: project configuration
README.md: project overview and setup guide
docs/getting-started.md: supplemental project documentation
webapp/main.py: likely startup or high-value module
```

## Render key files as JSON

Command:

```bash
reporamp files tests/fixtures/web_app --json
```

Output:

```json
[
  {
    "path": "pyproject.toml",
    "reason": "project configuration"
  },
  {
    "path": "README.md",
    "reason": "project overview and setup guide"
  },
  {
    "path": "docs/getting-started.md",
    "reason": "supplemental project documentation"
  },
  {
    "path": "webapp/main.py",
    "reason": "likely startup or high-value module"
  }
]
```

## Write key files to a file

Command:

```bash
reporamp files tests/fixtures/web_app --output key-files.txt
```

Output:

```text
Wrote files report to key-files.txt
```

## Render a summary as Markdown

Command:

```bash
reporamp summary tests/fixtures/basic_cli --markdown
```

Output:

```markdown
# Repository: tool-cli

## Entry Points
- `tool_cli/cli.py` (__main__ block)

## Tests
- none detected

## Documentation
- `README.md`

## Suggested Reading Order
- `pyproject.toml`: project configuration
- `tool_cli/cli.py`: likely startup or high-value module

## Framework Hints
- `typer`
```

## Write a Markdown summary to a file

Command:

```bash
reporamp summary tests/fixtures/basic_cli --markdown --output summary.md
```

Output:

```text
Wrote summary to summary.md
```

## Render a summary as JSON

Command:

```bash
reporamp summary tests/fixtures/basic_cli --json
```

Output:

```json
{
  "repository": "tool-cli",
  "entry_points": [
    {
      "path": "tool_cli/cli.py",
      "reason": "__main__ block"
    }
  ],
  "tests": [],
  "readme_files": [
    "README.md"
  ],
  "documentation_files": [
    "README.md"
  ],
  "suggested_reading_order": [
    {
      "path": "pyproject.toml",
      "reason": "project configuration"
    },
    {
      "path": "tool_cli/cli.py",
      "reason": "likely startup or high-value module"
    }
  ],
  "framework_hints": [
    "typer"
  ]
}
```

## Ask where the docs live

Command:

```bash
reporamp ask tests/fixtures/web_app "Where are the docs?"
```

Output:

```text
Documentation files:
- README.md
- docs/getting-started.md
```

## Ask where the README lives

Command:

```bash
reporamp ask tests/fixtures/web_app "Where is the README?"
```

Output:

```text
README files:
- README.md
```

## Ask where configuration lives

Command:

```bash
reporamp ask tests/fixtures/web_app "Where is the config?"
```

Output:

```text
Configuration files:
- pyproject.toml
```

## Ask where configuration lives as JSON

Command:

```bash
reporamp ask tests/fixtures/web_app "Where is the config?" --json
```

Output:

```json
{
  "question": "Where is the config?",
  "match_type": "config",
  "answer": "Configuration files:\n- pyproject.toml"
}
```

## Write a JSON answer to a file

Command:

```bash
reporamp ask tests/fixtures/web_app "Where is the config?" --json --output config.json
```

Output:

```text
Wrote answer to config.json
```

## Ask what to read first

Command:

```bash
reporamp ask tests/fixtures/src_layout "Which files should I read first?"
```

Output:

```text
Files to read first:
- pyproject.toml: project configuration
- src/pkgdemo/app.py: likely startup or high-value module
```

## Ask about package layout

Command:

```bash
reporamp ask tests/fixtures/src_layout "What is the package layout?"
```

Output:

```text
Package roots:
- src/pkgdemo
```

## Ask how the project starts

Command:

```bash
reporamp ask tests/fixtures/basic_cli "How does this project start?"
```

Output:

```text
Startup flow:
- Start at tool_cli/cli.py (__main__ block)
- Read pyproject.toml: project configuration
- Read tool_cli/cli.py: likely startup or high-value module
```
