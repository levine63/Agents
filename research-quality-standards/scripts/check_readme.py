from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


LOCKFILES = (
    "requirements-lock.txt",
    "poetry.lock",
    "uv.lock",
    "package-lock.json",
    "pnpm-lock.yaml",
    "yarn.lock",
)
REQUIRED_SECTIONS = {
    "Genre": ("Genre",),
    "Summary": ("Summary", "Overview"),
    "Quick Start": ("Quick Start", "Quickstart"),
    "Environment": ("Environment", "Setup", "Runtime"),
    "Data and Inputs": ("Data & Inputs", "Data and Inputs", "Inputs", "Data"),
    "Outputs": ("Outputs",),
    "Reproducibility": ("Reproducibility", "Reproducing Results"),
    "Tests and Validation": ("Tests & Validation", "Tests and Validation", "Tests", "Validation"),
    "Limitations and Risks": ("Limitations & Risks", "Limitations and Risks", "Limitations", "Known Risks"),
    "Troubleshooting": ("Common Issues", "Troubleshooting", "FAQ"),
    "File Structure": ("File Structure", "Repository Structure"),
    "Contributing or Workflow": ("Contributing / Workflow", "Contributing Or Workflow", "Contributing", "Workflow"),
    "License": ("License",),
    "Contact or Ownership": ("Contact / Ownership", "Contact Or Ownership", "Contact", "Ownership"),
}
GENRE_LABELS = (
    "replication repo",
    "data analysis",
    "application code",
    "library / tooling",
    "library/tooling",
    "mixed / llm pipeline",
    "mixed/llm pipeline",
    "mixed or llm pipeline",
    "custom",
)
SECRET_PATTERNS = (
    re.compile(r"OPENAI_API_KEY\s*=\s*sk-[A-Za-z0-9]", re.IGNORECASE),
    re.compile(r"api[_-]?key\s*=\s*['\"]?[A-Za-z0-9_\-]{20,}", re.IGNORECASE),
    re.compile(r"password\s*=\s*['\"]?[^xX<\s][^\s]{6,}", re.IGNORECASE),
    re.compile(r"BEGIN RSA PRIVATE KEY", re.IGNORECASE),
    re.compile(r"BEGIN OPENSSH PRIVATE KEY", re.IGNORECASE),
)
QUICK_START_PATH_PATTERN = re.compile(
    r"\b((?:examples|src|tests|data|outputs|scripts|docs|prompts)/[A-Za-z0-9._/\-]+)"
)


@dataclass
class Finding:
    level: str
    message: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Static README quality checks.")
    parser.add_argument("readme_path", nargs="?", default="README.md")
    parser.add_argument("--strict", action="store_true", help="Exit nonzero on blocking issues.")
    return parser.parse_args()


def section_exists(text: str, names: tuple[str, ...]) -> bool:
    for name in names:
        pattern = re.compile(rf"^#{{1,3}}\s+{re.escape(name)}\s*$", re.IGNORECASE | re.MULTILINE)
        if pattern.search(text):
            return True
    return False


def extract_section(text: str, names: tuple[str, ...]) -> str | None:
    for name in names:
        pattern = re.compile(
            rf"^#{{1,3}}\s+{re.escape(name)}\s*$\n(?P<body>.*?)(?=^#{{1,3}}\s+|\Z)",
            re.IGNORECASE | re.MULTILINE | re.DOTALL,
        )
        match = pattern.search(text)
        if match:
            return match.group("body")
    return None


def find_issues(readme_path: Path) -> list[Finding]:
    findings: list[Finding] = []
    if not readme_path.exists():
        return [Finding("BLOCKING", f"{readme_path.as_posix()} not found.")]

    text = readme_path.read_text(encoding="utf-8")
    repo_root = readme_path.parent

    for label, variants in REQUIRED_SECTIONS.items():
        if not section_exists(text, variants):
            findings.append(Finding("WARNING", f"Missing recommended section: {label}."))

    lowered = text.lower()
    if not section_exists(text, ("Genre",)) and not any(genre in lowered for genre in GENRE_LABELS):
        findings.append(Finding("WARNING", "README should explicitly declare project genre."))

    quick_start = extract_section(text, REQUIRED_SECTIONS["Quick Start"])
    if quick_start is None:
        findings.append(Finding("BLOCKING", "Missing Quick Start section."))
    else:
        if not re.search(r"```(?:bash|sh|shell)\n[\s\S]+?```", quick_start, re.IGNORECASE):
            findings.append(Finding("BLOCKING", "Quick Start should include a fenced bash/sh command block."))
        if not re.search(r"expected\s+output", quick_start, re.IGNORECASE):
            findings.append(Finding("WARNING", "Quick Start should include an Expected output block."))
        if re.search(r"read\s+-p|input\(|press any key|interactive", quick_start, re.IGNORECASE):
            findings.append(Finding("WARNING", "Quick Start appears to require interactive input."))
        for raw_path in QUICK_START_PATH_PATTERN.findall(quick_start):
            if "*" in raw_path:
                continue
            if not (repo_root / raw_path).exists():
                findings.append(Finding("WARNING", f"Quick Start references a missing path: {raw_path}."))

    if not (repo_root / "examples" / "minimal").exists():
        if not re.search(r"examples/minimal.*(not applicable|n/a|not needed|rationale|why not)", text, re.IGNORECASE):
            findings.append(Finding("WARNING", "Missing ./examples/minimal/ or a rationale for its absence."))

    has_lockfile = any((repo_root / name).exists() for name in LOCKFILES)
    if not has_lockfile and not re.search(r"lockfile.*(not applicable|n/a|not needed|rationale|why not)", text, re.IGNORECASE):
        findings.append(Finding("WARNING", "No lockfile found and no rationale for its absence was documented."))

    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            findings.append(Finding("BLOCKING", "README may expose a real secret or credential."))
            break

    if ".env" in text and ".env.example" not in text:
        findings.append(Finding("WARNING", "README references .env; prefer .env.example with dummy values."))

    if section_exists(text, REQUIRED_SECTIONS["Troubleshooting"]):
        issue_count = len(re.findall(r"\*\*Error:\*\*", text))
        if issue_count < 2 and not re.search(
            r"(troubleshooting|common issues).*(not applicable|n/a|not needed|rationale|why not)",
            text,
            re.IGNORECASE | re.DOTALL,
        ):
            findings.append(Finding("WARNING", "Troubleshooting should include at least 2 '**Error:**' entries or a rationale."))

    glossary = extract_section(text, ("Glossary",))
    if glossary:
        term_count = len(re.findall(r"^[-*]\s+\*\*[^*]+\*\*:?"," \n" + glossary, re.MULTILINE))
        if term_count > 5 and "./docs/glossary.md" not in text and "docs/glossary.md" not in text:
            findings.append(Finding("WARNING", "Glossary has more than 5 terms; move extras to ./docs/glossary.md."))

    if "mixed_or_llm_pipeline" in lowered or "llm pipeline" in lowered:
        for phrase in ("model", "temperature", "evaluation", "cost", "token"):
            if phrase not in lowered:
                findings.append(Finding("WARNING", f"LLM pipeline README should mention {phrase}."))

    if "replication_repo" in lowered or "replication repo" in lowered:
        for phrase in ("data access", "artifact registry", "citation"):
            if phrase not in lowered:
                findings.append(Finding("WARNING", f"Replication README should mention {phrase}."))

    return findings


def render(findings: list[Finding]) -> str:
    blocking = [item for item in findings if item.level == "BLOCKING"]
    warnings = [item for item in findings if item.level == "WARNING"]
    lines = ["README QUALITY CHECK", ""]
    if blocking:
        lines.append("BLOCKING:")
        lines.extend(f"- {item.message}" for item in blocking)
        lines.append("")
    if warnings:
        lines.append("WARNINGS:")
        lines.extend(f"- {item.message}" for item in warnings)
        lines.append("")
    if not findings:
        lines.append("No issues found by static checker.")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    args = parse_args()
    findings = find_issues(Path(args.readme_path).resolve())
    print(render(findings))
    if args.strict and any(item.level == "BLOCKING" for item in findings):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
