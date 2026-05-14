from __future__ import annotations

import argparse
import ast
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


HEADER_KEYS = ("author:", "date:", "purpose:", "intent:", "inputs:")
NOT_YET_DONE_PATTERNS = ("not yet done", "status:")
PERSONAL_PATH_PATTERN = re.compile(r"(?:[A-Za-z]:\\Users\\|/Users/|/home/[^/]+/)")
WRITING_PLACEHOLDER_PATTERNS = (
    re.compile(r"\bTBD\b", re.IGNORECASE),
    re.compile(r"\bLorem ipsum\b", re.IGNORECASE),
    re.compile(r"\binsert (citation|here)\b", re.IGNORECASE),
    re.compile(r"\bXX\b"),
)
WRITING_CITE_PATTERNS = (
    re.compile(r"\[CITE[^\]]*\]", re.IGNORECASE),
    re.compile(r"\bcitation needed\b", re.IGNORECASE),
)
PYTHON_RANDOM_TRIGGERS = (
    "random.",
    "np.random",
    "numpy.random",
    "train_test_split",
    "shuffle",
    "bootstrap",
    "resample",
)
PYTHON_RANDOM_SEEDS = ("random.seed(", "np.random.seed(", "default_rng(")
STATA_RANDOM_TRIGGERS = ("bootstrap", "simulate", "bsample", " sample ", "runiform(")


@dataclass
class Issue:
    severity: str
    rule_id: str
    file: str
    line: int | None
    message: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run MVP deterministic lint checks.")
    parser.add_argument("paths", nargs="+", help="Files or directories to lint.")
    parser.add_argument("--json-out", help="Optional JSON report output path.")
    parser.add_argument("--md-out", help="Optional Markdown report output path.")
    return parser.parse_args()


def gather_files(paths: Iterable[str]) -> list[Path]:
    files: list[Path] = []
    for raw_path in paths:
        path = Path(raw_path).resolve()
        if path.is_dir():
            for child in path.rglob("*"):
                if child.is_file():
                    files.append(child)
        elif path.is_file():
            files.append(path)
    return sorted(files)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def has_header(text: str) -> bool:
    head = text[:2000].lower()
    return any(key in head for key in HEADER_KEYS)


def has_not_yet_done(text: str) -> bool:
    lower = text.lower()
    return any(pattern in lower for pattern in NOT_YET_DONE_PATTERNS)


def find_line(text: str, pattern: str) -> int | None:
    for index, line in enumerate(text.splitlines(), start=1):
        if pattern.lower() in line.lower():
            return index
    return None


def check_global_text_rules(path: Path, text: str, require_header: bool) -> list[Issue]:
    issues: list[Issue] = []
    if require_header and not has_header(text):
        issues.append(
            Issue(
                severity="error",
                rule_id="header_present",
                file=path.as_posix(),
                line=1,
                message="Required provenance header appears to be missing.",
            )
        )
    if require_header and not has_not_yet_done(text):
        issues.append(
            Issue(
                severity="warning",
                rule_id="not_yet_done_present",
                file=path.as_posix(),
                line=1,
                message="Missing 'Not Yet Done' or equivalent status field.",
            )
        )
    match = PERSONAL_PATH_PATTERN.search(text)
    if match:
        line = find_line(text, match.group(0))
        issues.append(
            Issue(
                severity="warning",
                rule_id="personal_path_scan",
                file=path.as_posix(),
                line=line,
                message="Detected likely hard-coded personal path.",
            )
        )
    return issues


def lint_python(path: Path, text: str) -> list[Issue]:
    issues = check_global_text_rules(path, text, require_header=True)
    try:
        tree = ast.parse(text)
    except SyntaxError as exc:
        issues.append(
            Issue(
                severity="error",
                rule_id="python_parseable",
                file=path.as_posix(),
                line=exc.lineno,
                message=f"Python syntax error: {exc.msg}",
            )
        )
        return issues

    if ast.get_docstring(tree) is None:
        issues.append(
            Issue(
                severity="warning",
                rule_id="module_docstring_present",
                file=path.as_posix(),
                line=1,
                message="Module docstring is missing.",
            )
        )

    for node in ast.walk(tree):
        if isinstance(node, ast.ExceptHandler) and node.type is None:
            issues.append(
                Issue(
                    severity="error",
                    rule_id="bare_except_absent",
                    file=path.as_posix(),
                    line=node.lineno,
                    message="Bare except detected.",
                )
            )

    if any(trigger in text for trigger in PYTHON_RANDOM_TRIGGERS):
        if not any(seed in text for seed in PYTHON_RANDOM_SEEDS):
            issues.append(
                Issue(
                    severity="error",
                    rule_id="randomness_seeded",
                    file=path.as_posix(),
                    line=None,
                    message="Randomness detected without an explicit seed or generator.",
                )
            )
    return issues


def lint_stata(path: Path, text: str) -> list[Issue]:
    issues = check_global_text_rules(path, text, require_header=True)
    top_lines = "\n".join(text.splitlines()[:25]).lower()
    if "version " not in top_lines:
        issues.append(
            Issue(
                severity="error",
                rule_id="stata_version_present",
                file=path.as_posix(),
                line=1,
                message="Missing Stata version declaration near the top of the file.",
            )
        )
    if "set more off" not in top_lines:
        issues.append(
            Issue(
                severity="warning",
                rule_id="set_more_off_present",
                file=path.as_posix(),
                line=1,
                message="Missing 'set more off' near the top of the file.",
            )
        )
    lower = f" {text.lower()} "
    if any(trigger in lower for trigger in STATA_RANDOM_TRIGGERS) and "set seed" not in lower:
        issues.append(
            Issue(
                severity="error",
                rule_id="stata_randomness_seeded",
                file=path.as_posix(),
                line=None,
                message="Stochastic Stata command detected without 'set seed'.",
            )
        )
    return issues


def lint_writing(path: Path, text: str) -> list[Issue]:
    issues = check_global_text_rules(path, text, require_header=True)
    for pattern in WRITING_PLACEHOLDER_PATTERNS:
        match = pattern.search(text)
        if match:
            issues.append(
                Issue(
                    severity="error",
                    rule_id="placeholder_text_scan",
                    file=path.as_posix(),
                    line=find_line(text, match.group(0)),
                    message=f"Placeholder text detected: {match.group(0)!r}.",
                )
            )
            break
    for pattern in WRITING_CITE_PATTERNS:
        match = pattern.search(text)
        if match:
            issues.append(
                Issue(
                    severity="warning",
                    rule_id="cite_placeholder_scan",
                    file=path.as_posix(),
                    line=find_line(text, match.group(0)),
                    message=f"Unfinished citation marker detected: {match.group(0)!r}.",
                )
            )
            break
    return issues


def lint_file(path: Path) -> list[Issue]:
    suffix = path.suffix.lower()
    if suffix not in {".py", ".do", ".md"}:
        return []
    text = read_text(path)
    if suffix == ".py":
        return lint_python(path, text)
    if suffix == ".do":
        return lint_stata(path, text)
    return lint_writing(path, text)


def summarize(issues: list[Issue]) -> dict[str, int]:
    counts = {"error": 0, "warning": 0, "style": 0}
    for issue in issues:
        counts[issue.severity] = counts.get(issue.severity, 0) + 1
    return counts


def render_markdown(files: list[Path], issues: list[Issue]) -> str:
    counts = summarize(issues)
    lines = [
        "# MVP Lint Report",
        "",
        f"- Files checked: {len(files)}",
        f"- Errors: {counts.get('error', 0)}",
        f"- Warnings: {counts.get('warning', 0)}",
        f"- Style: {counts.get('style', 0)}",
        "",
        "## Issues",
        "",
    ]
    if not issues:
        lines.append("- No issues found.")
    else:
        for issue in issues:
            location = f"{issue.file}:{issue.line}" if issue.line else issue.file
            lines.append(
                f"- `{issue.severity.upper()}` `{issue.rule_id}` at `{location}`: {issue.message}"
            )
    return "\n".join(lines) + "\n"


def main() -> int:
    args = parse_args()
    files = gather_files(args.paths)
    issues: list[Issue] = []
    for path in files:
        issues.extend(lint_file(path))

    payload = {
        "files_checked": [path.as_posix() for path in files],
        "counts": summarize(issues),
        "issues": [asdict(issue) for issue in issues],
    }

    if args.json_out:
        json_path = Path(args.json_out).resolve()
        json_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    markdown = render_markdown(files, issues)
    if args.md_out:
        md_path = Path(args.md_out).resolve()
        md_path.parent.mkdir(parents=True, exist_ok=True)
        md_path.write_text(markdown, encoding="utf-8")

    print(markdown)
    return 1 if payload["counts"].get("error", 0) else 0


if __name__ == "__main__":
    raise SystemExit(main())
