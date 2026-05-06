from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


SUPPORTED_SUFFIXES = {".py", ".do", ".md"}
EXCLUDED_PATH_PARTS = {"generated", ".tmp_tests", "__pycache__"}
ZERO_SHA = "0000000000000000000000000000000000000000"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="List changed files that should be linted by lint_mvp.py."
    )
    parser.add_argument("--base", required=True, help="Base git ref or commit SHA.")
    parser.add_argument("--head", required=True, help="Head git ref or commit SHA.")
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Repository root for git commands. Defaults to current directory.",
    )
    return parser.parse_args()


def normalize_changed_paths(raw_paths: list[str]) -> list[str]:
    targets: list[str] = []
    for raw_path in raw_paths:
        raw_path = raw_path.strip()
        if not raw_path:
            continue
        path = Path(raw_path)
        if path.suffix.lower() not in SUPPORTED_SUFFIXES:
            continue
        if any(part in EXCLUDED_PATH_PARTS for part in path.parts):
            continue
        targets.append(path.as_posix())
    return sorted(dict.fromkeys(targets))


def git_changed_files(repo_root: Path, base: str, head: str) -> list[str]:
    if base == ZERO_SHA:
        command = ["git", "ls-files"]
    else:
        command = ["git", "diff", "--name-only", base, head]
    completed = subprocess.run(
        command,
        cwd=repo_root,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.splitlines()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    changed = git_changed_files(repo_root, args.base, args.head)
    targets = normalize_changed_paths(changed)
    for target in targets:
        print(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
