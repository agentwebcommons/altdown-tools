"""Dependency-free verification of the Cursor-ready artifact scaffold."""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "LICENSE", "NOTICE", "README.md", "AGENTS.md", "CLAUDE.md",
    "docs/ARCHITECTURE.md", "docs/adr/README.md",
    "docs/adr/2026-10-31-separate-fetch-and-validation.md",
    "docs/features/v0.1-reader-validator/PLAN.md",
    "docs/features/v0.1-reader-validator/TASKS.md",
    "docs/features/v0.1-reader-validator/ACCEPTANCE.md",
    "docs/features/v0.1-reader-validator/PROMPTS.md",
    ".cursor/rules/project.mdc", ".cursor/rules/python.mdc",
    ".github/workflows/ci.yml", "pyproject.toml", "tests/test_scaffold.py",
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-accepted", action="store_true")
    args = parser.parse_args()
    missing = [path for path in REQUIRED if not (ROOT / path).is_file()]
    adr = (ROOT / "docs/adr/2026-10-31-separate-fetch-and-validation.md").read_text()
    tasks = (ROOT / "docs/features/v0.1-reader-validator/TASKS.md").read_text()
    plan = (ROOT / "docs/features/v0.1-reader-validator/PLAN.md").read_text()
    license_text = (ROOT / "LICENSE").read_text()
    problems = [f"Missing {path}" for path in missing]
    if "Apache License" not in license_text or "Version 2.0" not in license_text:
        problems.append("LICENSE is not full Apache-2.0 text")
    if not re.search(r"- Status:\s*\*\*Proposed\*\*|- Status:\s*\*\*Accepted\*\*", adr):
        problems.append("ADR has no recognized Proposed/Accepted status")
    if args.require_accepted and "- Status: **Accepted**" not in adr:
        problems.append("Human has not marked ADR Accepted")
    if args.require_accepted and "## Open questions for human review" in adr:
        problems.append("ADR still contains open questions; resolve and remove that section first")
    task_ids = re.findall(r"\*\*T(\d{3})\*\*", tasks)
    if len(task_ids) < 15 or len(task_ids) != len(set(task_ids)):
        problems.append("Tasks are missing or IDs are duplicated")
    if tasks.count("**verify:**") != len(task_ids):
        problems.append("Every task must have a verify command")
    if "## Out of scope" not in plan:
        problems.append("PLAN must specify out of scope")
    if problems:
        for problem in problems:
            print(f"FAIL: {problem}", file=sys.stderr)
        return 1
    print(f"PASS: {len(REQUIRED)} required files; {len(task_ids)} tasks; Apache-2.0 license")
    print("ADR status: " + ("Accepted" if "- Status: **Accepted**" in adr else "Proposed"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
