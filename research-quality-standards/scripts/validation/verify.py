#!/usr/bin/env python3
"""
Date: 2026-05-06
Purpose: Cross-platform starter verification wrapper for Codex-managed tasks.
Usage: python scripts/verify.py
Notes: This is intentionally conservative. Customize per repository.
It validates `.codex_tests.json` as JSON only, not against a schema.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path


def run_command(command: list[str], label: str) -> int:
    print(label)
    result = subprocess.run(command, check=False)
    if result.returncode != 0:
        print(f"ERROR: command failed with exit code {result.returncode}: {' '.join(command)}")
    return result.returncode


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    skipped_checks: list[str] = []
    print("Running Codex verification...")

    secret_scanner = Path(__file__).resolve().parent / "detect_secrets.py"
    if secret_scanner.exists():
        code = run_command([sys.executable, str(secret_scanner)], "Running secret scan...")
        if code != 0:
            return code

    codex_tests = root / ".codex_tests.json"
    if codex_tests.exists():
        print("Found .codex_tests.json. Codex should parse and run configured tests.")
        try:
            json.loads(codex_tests.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            print(f"ERROR: .codex_tests.json is not valid JSON: {exc}")
            return 1
        print("Validated .codex_tests.json syntax only; schema validation is not implemented.")

    pytest_like = any((root / name).exists() for name in ("pytest.ini", "pyproject.toml")) or (root / "tests").exists()
    if pytest_like:
        pytest_path = shutil.which("pytest")
        if pytest_path:
            code = run_command([pytest_path, "-q"], "Running pytest...")
            if code != 0:
                return code
        else:
            message = "pytest-like project detected, but pytest is not installed; pytest checks were skipped."
            print(f"WARNING: {message}")
            skipped_checks.append(message)

    package_json = root / "package.json"
    if package_json.exists():
        npm_path = shutil.which("npm")
        if npm_path:
            text = package_json.read_text(encoding="utf-8", errors="ignore")
            if '"test"' in text:
                code = run_command([npm_path, "test"], "Running npm test...")
                if code != 0:
                    return code
        else:
            message = "package.json detected, but npm is not installed; npm-based checks were skipped."
            print(f"WARNING: {message}")
            skipped_checks.append(message)

    if skipped_checks:
        print("Verification completed with skipped checks:")
        for message in skipped_checks:
            print(f"- {message}")
    else:
        print("Verification completed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
