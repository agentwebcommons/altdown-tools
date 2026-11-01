"""Small scaffold-only test. Feature tests are tasks for Cursor to implement."""

from pathlib import Path


def test_project_artifacts_exist() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (root / "AGENTS.md").is_file()
    assert (root / "LICENSE").is_file()
    assert (root / "docs/features/v0.1-reader-validator/TASKS.md").is_file()
