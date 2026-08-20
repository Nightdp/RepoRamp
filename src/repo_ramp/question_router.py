from .models import RepositoryIndex


SUPPORTED_PATTERNS = {
    "config": ("config", "configuration", "settings"),
    "tests": ("tests", "test suite"),
    "startup_flow": ("startup flow", "how does this start", "how does this project start"),
    "package_layout": ("package layout", "package root", "package structure", "src layout"),
    "entry_points": ("start", "run", "entry point", "main"),
    "reading_order": ("read first", "important files", "read"),
}


def answer_question(index: RepositoryIndex, question: str) -> str:
    lowered = question.lower()

    if any(token in lowered for token in SUPPORTED_PATTERNS["config"]):
        return "Configuration files:\n" + "\n".join(f"- {item}" for item in index.config_files)

    if any(token in lowered for token in SUPPORTED_PATTERNS["tests"]):
        return "Test files:\n" + "\n".join(f"- {item}" for item in index.test_files)

    if any(token in lowered for token in SUPPORTED_PATTERNS["startup_flow"]):
        lines = ["Startup flow:"]

        if index.entry_points:
            lines.extend(f"- Start at {item['path']} ({item['reason']})" for item in index.entry_points)
        else:
            lines.append("- No likely entry point detected")

        if index.key_files:
            lines.extend(f"- Read {item['path']}: {item['reason']}" for item in index.key_files)

        return "\n".join(lines)

    if any(token in lowered for token in SUPPORTED_PATTERNS["package_layout"]):
        if not index.package_roots:
            return "Package roots:\n- none detected"

        return "Package roots:\n" + "\n".join(f"- {item}" for item in index.package_roots)

    if any(token in lowered for token in SUPPORTED_PATTERNS["entry_points"]):
        return "Entry points:\n" + "\n".join(
            f"- {item['path']} ({item['reason']})" for item in index.entry_points
        )

    if any(token in lowered for token in SUPPORTED_PATTERNS["reading_order"]):
        return "Files to read first:\n" + "\n".join(
            f"- {item['path']}: {item['reason']}" for item in index.key_files
        )

    return (
        "Supported questions: entry points, config, tests, package layout, startup flow, "
        "files to read first."
    )
