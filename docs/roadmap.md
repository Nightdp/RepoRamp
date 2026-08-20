# RepoRamp Roadmap

`RepoRamp` is intentionally narrow.

The goal is not to become a general-purpose coding assistant. The goal is to
become a dependable local-first CLI for understanding unfamiliar Python
repositories quickly.

## Current Focus

These are the highest-value improvements for the next stretch of development:

- broader coverage for common Python repository layouts
- better ranking for "read this first" files
- clearer maintainer-facing summary output
- more fixture repositories that reflect real open source project shapes

## Near-Term Work

### 1. Better framework and layout hints

Improve detection for common structures such as:

- Django projects
- Flask apps with factory layouts
- FastAPI apps with routers and package-based startup
- larger `src/` layout libraries

### 2. Stronger onboarding output

Make summaries more useful for first-time contributors by improving:

- reading-order suggestions
- entry-point explanations
- package root descriptions
- config-file relevance

### 3. More fixture-backed confidence

Grow the test fixtures so the tool is validated against:

- CLI tools
- libraries
- web apps
- mixed-layout repositories
- partially broken repositories

## Later, If They Still Fit The Scope

Possible future additions that still align with the current project direction:

- Markdown export for onboarding docs
- JSON output for automation and tooling
- richer packaging metadata summaries

These should only happen if they preserve the project's current strengths:

- deterministic output
- local-first workflows
- narrow repository-understanding scope

## Explicitly Not The Plan

The following are not current roadmap goals:

- code generation
- refactoring assistance
- cloud-only workflows
- always-on background services
- multi-language support before Python coverage is solid

## Good Contribution Directions

If you want to contribute, the most helpful contributions right now are:

- new fixture repositories
- improved heuristics with tests
- summary formatting improvements
- documentation that helps maintainers evaluate the tool quickly
