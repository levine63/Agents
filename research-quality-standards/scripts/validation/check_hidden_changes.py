#!/usr/bin/env python3
"""
Date: 2026-05-06
Purpose: Starter helper to compare changed files against a final report.
Usage: python scripts/check_hidden_changes.py tmp_codex_work/final_report.md
Notes: This is a heuristic based on repo-relative paths mentioned in the report.
Codex should improve it for each repo.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


def git_changed_files(repo_root: Path) -> list[str]:
    inside = subprocess.run(
        ["git", "rev-parse", "--is-inside-work-tree"],
        text=True,
        capture_output=True,
        check=False,
        cwd=repo_root,
    )
    if inside.returncode != 0:
        raise RuntimeError("Not inside a usable git work tree.")
    status = subprocess.run(
        ["git", "status", "--porcelain"],
        text=True,
        capture_output=True,
        check=False,
        cwd=repo_root,
    )
    if status.returncode != 0:
        raise RuntimeError("Could not read changed files from git status.")

    changed: list[str] = []
    for line in status.stdout.splitlines():
        if len(line) < 4:
            continue
        path = line[3:].strip()
        if not path:
            continue
        if " -> " in path:
            path = path.split(" -> ", 1)[1].strip()
        changed.append(path.replace("\\", "/"))
    return changed


def report_paths(report: str) -> set[str]:
    tokens = set()
    for token in re.findall(r"`([^`]+)`", report):
        normalized = token.strip().replace("\\", "/")
        if "/" in normalized or "." in Path(normalized).name:
            tokens.add(normalized)
    return tokens


def main() -> int:
    repo_root = Path(__file__).resolve().parents[2]
    report_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("tmp_codex_work/final_report.md")
    if not report_path.exists():
        print(f"ERROR: report not found: {report_path}")
        return 1

    report = report_path.read_text(encoding="utf-8", errors="replace")
    try:
        changed_files = git_changed_files(repo_root)
    except RuntimeError as exc:
        print(f"WARNING: hidden-change check skipped: {exc}")
        print("WARNING: file-to-report comparison did not run.")
        return 0

    reported_paths = report_paths(report)
    missing = [path for path in changed_files if path not in reported_paths]

    if missing:
        print("ERROR: changed files missing from final report:")
        for path in missing:
            print(f"  - {path}")
        return 1

    print("No hidden changed files detected by filename heuristic.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
