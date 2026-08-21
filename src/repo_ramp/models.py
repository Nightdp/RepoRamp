from dataclasses import dataclass, field


@dataclass(slots=True)
class RepositoryIndex:
    root: str
    project_name: str | None = None
    readme_files: list[str] = field(default_factory=list)
    documentation_files: list[str] = field(default_factory=list)
    config_files: list[str] = field(default_factory=list)
    package_roots: list[str] = field(default_factory=list)
    python_files: list[str] = field(default_factory=list)
    test_files: list[str] = field(default_factory=list)
    entry_points: list[dict[str, str]] = field(default_factory=list)
    key_files: list[dict[str, str]] = field(default_factory=list)
    framework_hints: list[str] = field(default_factory=list)
    skipped_files: list[str] = field(default_factory=list)
