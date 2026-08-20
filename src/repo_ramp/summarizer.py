import json

from .models import RepositoryIndex


def _build_summary_payload(index: RepositoryIndex) -> dict[str, object]:
    return {
        "repository": index.project_name or "unknown",
        "entry_points": index.entry_points,
        "tests": index.test_files,
        "suggested_reading_order": index.key_files,
        "framework_hints": index.framework_hints,
    }


def _render_json_summary(index: RepositoryIndex) -> str:
    return json.dumps(_build_summary_payload(index), indent=2)


def _render_markdown_summary(index: RepositoryIndex) -> str:
    lines = [f"# Repository: {index.project_name or 'unknown'}", "", "## Entry Points"]

    if index.entry_points:
        lines.extend(f"- `{item['path']}` ({item['reason']})" for item in index.entry_points)
    else:
        lines.append("- none detected")

    lines.extend(["", "## Tests"])
    if index.test_files:
        lines.extend(f"- `{path}`" for path in index.test_files)
    else:
        lines.append("- none detected")

    lines.extend(["", "## Suggested Reading Order"])
    if index.key_files:
        lines.extend(f"- `{item['path']}`: {item['reason']}" for item in index.key_files)
    else:
        lines.append("- none detected")

    if index.framework_hints:
        lines.extend(["", "## Framework Hints"])
        lines.extend(f"- `{hint}`" for hint in index.framework_hints)

    return "\n".join(lines)


def render_summary(
    index: RepositoryIndex, *, markdown: bool = False, json_output: bool = False
) -> str:
    if json_output:
        return _render_json_summary(index)

    if markdown:
        return _render_markdown_summary(index)

    lines = [
        f"Repository: {index.project_name or 'unknown'}",
        "",
        "Entry Points:",
    ]

    if index.entry_points:
        lines.extend(f"- {item['path']} ({item['reason']})" for item in index.entry_points)
    else:
        lines.append("- none detected")

    lines.extend(["", "Tests:"])
    if index.test_files:
        lines.extend(f"- {path}" for path in index.test_files)
    else:
        lines.append("- none detected")

    lines.extend(["", "Suggested Reading Order:"])
    if index.key_files:
        lines.extend(f"- {item['path']}: {item['reason']}" for item in index.key_files)
    else:
        lines.append("- none detected")

    if index.framework_hints:
        lines.extend(["", "Framework Hints:"])
        lines.extend(f"- {hint}" for hint in index.framework_hints)

    return "\n".join(lines)
