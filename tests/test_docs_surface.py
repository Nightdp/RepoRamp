from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_readme_links_to_architecture_doc() -> None:
    readme = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8")

    assert "docs/architecture.md" in readme


def test_architecture_doc_exists_with_core_sections() -> None:
    architecture = (PROJECT_ROOT / "docs" / "architecture.md")

    assert architecture.exists()

    content = architecture.read_text(encoding="utf-8")

    assert "# RepoRamp Architecture" in content
    assert "## Request Flow" in content
    assert "## Core Components" in content


def test_issue_template_contact_links_use_main_branch() -> None:
    config = (PROJECT_ROOT / ".github" / "ISSUE_TEMPLATE" / "config.yml").read_text(
        encoding="utf-8"
    )

    assert "/blob/main/CONTRIBUTING.md" in config
    assert "/blob/main/SECURITY.md" in config
