#!/usr/bin/env python3
"""
Date: 2026-05-06
Purpose: Cross-platform starter secret scan for repository content.
Usage: python scripts/detect_secrets.py
Notes: Prefer dedicated tools such as gitleaks or trufflehog for production use.
This starter scanner does not reliably detect encoded, split, or obfuscated secrets.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path


PATTERN = re.compile(
    r"AKIA[0-9A-Z]{16}"
    r"|sk-[a-zA-Z0-9_-]{20,}"
    r"|ghp_[a-zA-Z0-9]{30,}"
    r"|ghs_[a-zA-Z0-9]{30,}"
    r"|xox[baprs]-[a-zA-Z0-9-]{20,}"
    r"|eyJ[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9._-]{10,}\.[a-zA-Z0-9._-]{10,}"
    r"|-----BEGIN (?:RSA|OPENSSH|DSA|EC) PRIVATE KEY-----"
    r"|mongodb\+srv://[^\s]+"
    r"|postgresql://[^\s]+"
)
SKIP_DIRS = {".git", "__pycache__", "tmp_codex_work", ".codex_approvals"}
SKIP_FILES = {"detect_secrets.py", "detect_secrets.sh"}
FALLBACK_SUFFIXES = {".py", ".sh", ".json", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".env", ".js", ".ts", ".tsx", ".jsx"}


def repo_diff_text() -> str | None:
    inside = subprocess.run(
        ["git", "rev-parse", "--is-inside-work-tree"],
        text=True,
        capture_output=True,
        check=False,
    )
    if inside.returncode != 0:
        return None
    cached = subprocess.run(["git", "diff", "--cached"], text=True, capture_output=True, check=False)
    unstaged = subprocess.run(["git", "diff"], text=True, capture_output=True, check=False)
    return f"{cached.stdout}\n{unstaged.stdout}"


def filesystem_text(root: Path) -> str:
    chunks: list[str] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.name in SKIP_FILES:
            continue
        if path.suffix.lower() not in FALLBACK_SUFFIXES:
            continue
        try:
            chunks.append(path.read_text(encoding="utf-8", errors="ignore"))
        except OSError:
            continue
    return "\n".join(chunks)


def main() -> int:
    print("Scanning for common secret patterns...")
    content = repo_diff_text()
    if content is None:
        content = filesystem_text(Path(__file__).resolve().parents[2])
    if PATTERN.search(content):
        print("ERROR: possible secret detected.")
        print("Remove the secret, use placeholders, or configure an approved secret manager.")
        return 1
    print("No common secret pattern detected.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
