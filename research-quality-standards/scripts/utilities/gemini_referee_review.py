from __future__ import annotations

import argparse
import base64
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib import error, request
from xml.etree import ElementTree
from zipfile import BadZipFile, ZipFile

DEFAULT_PROVIDER = "gemini"
DEFAULT_GEMINI_MODEL = "gemini-2.5-pro"
DEFAULT_CLAUDE_MODEL = "claude-sonnet-4-20250514"
DEFAULT_OUTPUT_SUBDIR = Path("generated/external_reviews")
DEFAULT_ENV_FILE = Path(__file__).with_name("tools.env")
MAX_INLINE_BYTES = 18 * 1024 * 1024
ANTHROPIC_VERSION = "2023-06-01"
CLAUDE_TOOL_NAME = "submit_review"
CLAUDE_MAX_TOKENS = 4096
WORDPROCESSINGML_NAMESPACE = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
}

REVIEW_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "review_summary": {"type": "string"},
        "global_concerns": {"type": "array", "items": {"type": "string"}},
        "recommendations": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "title": {"type": "string"},
                    "category": {"type": "string"},
                    "severity": {"type": "string"},
                    "recommendation": {"type": "string"},
                    "rationale": {"type": "string"},
                    "evidence_from_report": {"type": "string"},
                    "affected_files": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "acceptance_test": {"type": "string"},
                    "confidence": {"type": "string"},
                },
                "required": [
                    "id",
                    "title",
                    "category",
                    "severity",
                    "recommendation",
                    "rationale",
                    "evidence_from_report",
                    "affected_files",
                    "acceptance_test",
                    "confidence",
                ],
            },
        },
        "questions_for_authors": {"type": "array", "items": {"type": "string"}},
    },
    "required": [
        "review_summary",
        "global_concerns",
        "recommendations",
        "questions_for_authors",
    ],
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Send a referee report and selected supported files to Gemini for a "
            "structured external review."
        )
    )
    parser.add_argument(
        "--provider",
        choices=["gemini", "claude"],
        default=DEFAULT_PROVIDER,
        help="Model provider to use. Defaults to gemini.",
    )
    parser.add_argument(
        "--report",
        required=True,
        help="Path to a supported referee report file such as .docx, .md, or .txt.",
    )
    parser.add_argument(
        "--files",
        nargs="+",
        required=True,
        help="One or more supported project files to include in the review.",
    )
    parser.add_argument(
        "--role",
        default="expert reviewer",
        help=(
            "Reviewer lens to ask Gemini to adopt, "
            "for example 'expert coder' or 'expert epidemiologist'."
        ),
    )
    parser.add_argument(
        "--focus",
        action="append",
        default=[],
        help="Optional review focus area. Repeat for multiple focus areas.",
    )
    parser.add_argument(
        "--project-name",
        default="current project",
        help="Name used in the prompt and output artifact naming.",
    )
    parser.add_argument(
        "--project-root",
        default=".",
        help="Root used to compute relative file paths in the prompt.",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="Optional model name override. Defaults depend on provider.",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help=(
            "Directory where JSON and Markdown review artifacts should be written. "
            "Defaults to <project-root>/generated/external_reviews."
        ),
    )
    parser.add_argument(
        "--timeout-seconds",
        type=int,
        default=120,
        help="HTTP timeout in seconds.",
    )
    return parser.parse_args()


def normalize_path(path_str: str) -> Path:
    return Path(path_str).expanduser().resolve()


def load_env_file(env_path: Path = DEFAULT_ENV_FILE) -> dict[str, str]:
    loaded: dict[str, str] = {}
    if not env_path.exists():
        return loaded

    for line_number, raw_line in enumerate(
        env_path.read_text(encoding="utf-8").splitlines(),
        start=1,
    ):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            raise ValueError(
                f"Invalid env line in {env_path} at line {line_number}: {raw_line!r}"
            )
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("\"'")
        if not key:
            raise ValueError(
                f"Invalid empty env key in {env_path} at line {line_number}."
            )
        loaded[key] = value
        os.environ.setdefault(key, value)
    return loaded


def resolve_model(provider: str, model: str | None) -> str:
    if model:
        return model
    if provider == "claude":
        return DEFAULT_CLAUDE_MODEL
    return DEFAULT_GEMINI_MODEL


def get_api_key(provider: str) -> str:
    env_names = (
        ["ANTHROPIC_API_KEY", "ANTHROPIC_KEY"]
        if provider == "claude"
        else ["GEMINI_API_KEY", "GEMINI_KEY"]
    )
    for env_name in env_names:
        api_key = os.environ.get(env_name)
        if api_key:
            return api_key
    preferred = env_names[0]
    aliases = ", ".join(env_names[1:])
    if aliases:
        raise SystemExit(
            f"{preferred} is not set in the environment. "
            f"Accepted aliases for this provider: {aliases}."
        )
    raise SystemExit(f"{preferred} is not set in the environment.")


def looks_binary(data: bytes) -> bool:
    if b"\x00" in data:
        return True
    if not data:
        return False
    text_bytes = sum(
        byte in b"\t\n\r\f\b" or 32 <= byte <= 126 or byte >= 128 for byte in data
    )
    return (text_bytes / len(data)) < 0.85


def decode_text(data: bytes, path: Path) -> str:
    for encoding in ("utf-8-sig", "utf-16", "cp1252", "latin-1"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    raise ValueError(f"Could not decode text file: {path}")


def extract_docx_text(path: Path) -> str:
    try:
        with ZipFile(path) as archive:
            document_xml = archive.read("word/document.xml")
    except KeyError as exc:
        raise ValueError(f"Word document is missing word/document.xml: {path}") from exc
    except BadZipFile as exc:
        raise ValueError(f"Invalid .docx file: {path}") from exc

    root = ElementTree.fromstring(document_xml)
    paragraphs: list[str] = []
    for paragraph in root.findall(".//w:p", WORDPROCESSINGML_NAMESPACE):
        parts: list[str] = []
        for node in paragraph.iter():
            if node.tag == f"{{{WORDPROCESSINGML_NAMESPACE['w']}}}t":
                parts.append(node.text or "")
            elif node.tag == f"{{{WORDPROCESSINGML_NAMESPACE['w']}}}tab":
                parts.append("\t")
            elif node.tag in {
                f"{{{WORDPROCESSINGML_NAMESPACE['w']}}}br",
                f"{{{WORDPROCESSINGML_NAMESPACE['w']}}}cr",
            }:
                parts.append("\n")
        paragraph_text = "".join(parts).strip()
        if paragraph_text:
            paragraphs.append(paragraph_text)
    return "\n\n".join(paragraphs)


def relative_label(path: Path, root: Path) -> str:
    try:
        return f"./{path.relative_to(root).as_posix()}"
    except ValueError:
        return path.as_posix()


def read_supported_document(path: Path) -> str:
    if path.suffix.lower() == ".docx":
        text = extract_docx_text(path)
        if not text.strip():
            raise ValueError(f"Word document did not contain readable text: {path}")
        return text.strip()

    data = path.read_bytes()
    if looks_binary(data):
        raise ValueError(
            f"Binary or unsupported file detected: {path}. "
            "Supported formats are plain-text files and .docx. "
            "Convert PDFs or legacy .doc files before using this tool."
        )
    return decode_text(data, path).strip()


def collect_text_documents(paths: list[str], root: Path) -> list[dict[str, str]]:
    documents: list[dict[str, str]] = []
    for path_str in paths:
        path = normalize_path(path_str)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        documents.append(
            {
                "path": relative_label(path, root),
                "text": read_supported_document(path),
            }
        )
    return documents


def collect_supported_documents(paths: list[str], root: Path) -> list[dict[str, Any]]:
    documents: list[dict[str, Any]] = []
    for path_str in paths:
        path = normalize_path(path_str)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        label = relative_label(path, root)
        if path.suffix.lower() == ".pdf":
            pdf_bytes = path.read_bytes()
            if not pdf_bytes:
                raise ValueError(f"PDF file is empty: {path}")
            documents.append(
                {
                    "path": label,
                    "kind": "pdf",
                    "mime_type": "application/pdf",
                    "data_base64": base64.b64encode(pdf_bytes).decode("ascii"),
                    "byte_length": len(pdf_bytes),
                }
            )
            continue

        documents.append(
            {
                "path": label,
                "kind": "text",
                "text": read_supported_document(path),
            }
        )
    return documents


def total_inline_bytes(documents: list[dict[str, Any]]) -> int:
    total = 0
    for document in documents:
        if document["kind"] == "text":
            total += len(document["text"].encode("utf-8"))
        elif document["kind"] == "pdf":
            total += len(document["data_base64"].encode("ascii"))
    return total


def format_document_block(title: str, documents: list[dict[str, str]]) -> str:
    sections = [title]
    for document in documents:
        sections.append(
            "\n".join(
                [
                    f"=== BEGIN FILE: {document['path']} ===",
                    document["text"],
                    f"=== END FILE: {document['path']} ===",
                ]
            )
        )
    return "\n\n".join(sections)


def build_prompt(
    report_document: dict[str, Any],
    project_documents: list[dict[str, Any]],
    role: str,
    focus: list[str],
    project_name: str,
) -> str:
    focus_lines = "\n".join(f"- {item}" for item in focus) if focus else "- None specified"
    text_project_documents = [
        document for document in project_documents if document["kind"] == "text"
    ]
    pdf_project_paths = [
        document["path"] for document in project_documents if document["kind"] == "pdf"
    ]
    instructions = [
        f"You are acting as a {role}.",
        f"Review the referee report against the supplied files for {project_name}.",
        "Treat the referee report as input, not truth.",
        "Be skeptical, specific, and evidence-based.",
        "Do not invent files, facts, references, or limitations not grounded in the provided material.",
        "Flag when a recommendation is underspecified, conflicts with the files, or needs author judgment.",
        "Prefer concrete implementation guidance over generic advice.",
        "For each recommendation, name likely affected files only if they are actually supported by the provided files.",
        "Return JSON only that matches the requested schema.",
        "",
        "Review focus:",
        focus_lines,
        "",
        "Evaluation criteria:",
        "- Identify which referee recommendations appear sound and actionable.",
        "- Separate coding, methods, documentation, validation, clarity, and citation concerns.",
        "- Highlight missing evidence, unsupported claims, and requests that should probably be declined.",
        "- For each recommendation, suggest a concrete acceptance test or verification step.",
        "",
    ]

    if report_document["kind"] == "text":
        instructions.extend(
            [
                format_document_block("Referee report:", [report_document]),
                "",
            ]
        )
    else:
        instructions.extend(
            [
                "The referee report is attached separately as a PDF part.",
                f"- Referee report PDF: {report_document['path']}",
                "Use the PDF itself as the source of truth for the report content.",
                "",
            ]
        )

    if text_project_documents:
        instructions.extend(
            [
                format_document_block("Project files provided as text:", text_project_documents),
                "",
            ]
        )

    if pdf_project_paths:
        instructions.extend(
            [
                "Project files attached separately as PDF parts:",
                *[f"- {path}" for path in pdf_project_paths],
                "Use the attached PDFs directly when evaluating figures, tables, formatting, or layout-sensitive arguments.",
                "",
            ]
        )

    return "\n".join(instructions)


def build_gemini_request_parts(
    prompt: str,
    report_document: dict[str, Any],
    project_documents: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    parts: list[dict[str, Any]] = [{"text": prompt}]
    for document in [report_document, *project_documents]:
        if document["kind"] != "pdf":
            continue
        parts.append({"text": f"Attached PDF file: {document['path']}"})
        parts.append(
            {
                "inline_data": {
                    "mime_type": document["mime_type"],
                    "data": document["data_base64"],
                }
            }
        )
    return parts


def build_claude_message_content(
    prompt: str,
    report_document: dict[str, Any],
    project_documents: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    content: list[dict[str, Any]] = []
    for document in [report_document, *project_documents]:
        if document["kind"] != "pdf":
            continue
        content.append(
            {
                "type": "document",
                "source": {
                    "type": "base64",
                    "media_type": document["mime_type"],
                    "data": document["data_base64"],
                },
                "title": document["path"],
            }
        )
    content.append({"type": "text", "text": prompt})
    return content


def fetch_review(
    provider: str,
    prompt: str,
    report_document: dict[str, Any],
    project_documents: list[dict[str, Any]],
    *,
    api_key: str,
    model: str,
    timeout_seconds: int,
) -> dict[str, Any]:
    if provider == "claude":
        return fetch_claude_review(
            prompt,
            report_document,
            project_documents,
            api_key=api_key,
            model=model,
            timeout_seconds=timeout_seconds,
        )
    return fetch_gemini_review(
        prompt,
        report_document,
        project_documents,
        api_key=api_key,
        model=model,
        timeout_seconds=timeout_seconds,
    )


def fetch_gemini_review(
    prompt: str,
    report_document: dict[str, Any],
    project_documents: list[dict[str, Any]],
    *,
    api_key: str,
    model: str,
    timeout_seconds: int,
) -> dict[str, Any]:
    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{model}:generateContent"
    )
    parts = build_gemini_request_parts(prompt, report_document, project_documents)
    payload = {
        "contents": [{"role": "user", "parts": parts}],
        "generationConfig": {
            "temperature": 0.1,
            "responseMimeType": "application/json",
            "responseJsonSchema": REVIEW_SCHEMA,
        },
    }
    body = json.dumps(payload).encode("utf-8")
    req = request.Request(
        url,
        data=body,
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": api_key,
        },
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=timeout_seconds) as response:
            raw = response.read().decode("utf-8")
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"Gemini API request failed with HTTP {exc.code}: {detail}"
        ) from exc
    except error.URLError as exc:
        raise RuntimeError(f"Gemini API request failed: {exc.reason}") from exc

    payload = json.loads(raw)
    return parse_gemini_payload(payload)


def fetch_claude_review(
    prompt: str,
    report_document: dict[str, Any],
    project_documents: list[dict[str, Any]],
    *,
    api_key: str,
    model: str,
    timeout_seconds: int,
) -> dict[str, Any]:
    url = "https://api.anthropic.com/v1/messages"
    payload = {
        "model": model,
        "max_tokens": CLAUDE_MAX_TOKENS,
        "tools": [
            {
                "name": CLAUDE_TOOL_NAME,
                "description": (
                    "Return the structured review result for the supplied "
                    "referee report and project files."
                ),
                "input_schema": REVIEW_SCHEMA,
            }
        ],
        "tool_choice": {"type": "tool", "name": CLAUDE_TOOL_NAME},
        "messages": [
            {
                "role": "user",
                "content": build_claude_message_content(
                    prompt,
                    report_document,
                    project_documents,
                ),
            }
        ],
    }
    body = json.dumps(payload).encode("utf-8")
    req = request.Request(
        url,
        data=body,
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": ANTHROPIC_VERSION,
        },
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=timeout_seconds) as response:
            raw = response.read().decode("utf-8")
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"Claude API request failed with HTTP {exc.code}: {detail}"
        ) from exc
    except error.URLError as exc:
        raise RuntimeError(f"Claude API request failed: {exc.reason}") from exc

    payload = json.loads(raw)
    return parse_claude_payload(payload)


def parse_gemini_payload(payload: dict[str, Any]) -> dict[str, Any]:
    candidates = payload.get("candidates") or []
    if not candidates:
        raise ValueError("Gemini response did not include any candidates.")
    parts = candidates[0].get("content", {}).get("parts", [])
    if not parts or "text" not in parts[0]:
        raise ValueError("Gemini response did not contain a text part.")
    parsed = json.loads(parts[0]["text"])
    validate_review_result(parsed)
    return parsed


def parse_claude_payload(payload: dict[str, Any]) -> dict[str, Any]:
    content = payload.get("content") or []
    for block in content:
        if (
            block.get("type") == "tool_use"
            and block.get("name") == CLAUDE_TOOL_NAME
            and isinstance(block.get("input"), dict)
        ):
            parsed = block["input"]
            validate_review_result(parsed)
            return parsed
    raise ValueError("Claude response did not contain the expected review tool output.")


def validate_review_result(result: dict[str, Any]) -> None:
    required_top_level = [
        "review_summary",
        "global_concerns",
        "recommendations",
        "questions_for_authors",
    ]
    missing = [key for key in required_top_level if key not in result]
    if missing:
        raise ValueError(f"Review result missing required keys: {', '.join(missing)}")
    if not isinstance(result["recommendations"], list):
        raise ValueError("Review result field 'recommendations' must be a list.")


def slugify(value: str) -> str:
    slug = []
    for char in value.lower():
        if char.isalnum():
            slug.append(char)
        elif slug and slug[-1] != "-":
            slug.append("-")
    return "".join(slug).strip("-") or "review"


def resolve_output_dir(project_root: Path, output_dir_arg: str | None) -> Path:
    if output_dir_arg:
        return normalize_path(output_dir_arg)
    return (project_root / DEFAULT_OUTPUT_SUBDIR).resolve()


def render_markdown(
    result: dict[str, Any],
    *,
    metadata: dict[str, Any],
) -> str:
    lines = [
        f"# External Referee Review: {metadata['project_name']}",
        "",
        f"- Generated: {metadata['generated_at']}",
        f"- Provider: {metadata['provider']}",
        f"- Model: {metadata['model']}",
        f"- Reviewer role: {metadata['role']}",
        f"- Referee report: `{metadata['report_path']}`",
        "",
        "## Summary",
        "",
        result["review_summary"],
        "",
        "## Global Concerns",
        "",
    ]

    if result["global_concerns"]:
        lines.extend(f"- {item}" for item in result["global_concerns"])
    else:
        lines.append("- None reported.")

    lines.extend(["", "## Recommendations", ""])

    if not result["recommendations"]:
        lines.append("- No concrete recommendations returned.")
    else:
        for rec in result["recommendations"]:
            lines.extend(
                [
                    f"### {rec['id']}: {rec['title']}",
                    "",
                    f"- Category: {rec['category']}",
                    f"- Severity: {rec['severity']}",
                    f"- Confidence: {rec['confidence']}",
                    f"- Affected files: {', '.join(rec['affected_files']) or 'None specified'}",
                    f"- Recommendation: {rec['recommendation']}",
                    f"- Rationale: {rec['rationale']}",
                    f"- Evidence from report: {rec['evidence_from_report']}",
                    f"- Acceptance test: {rec['acceptance_test']}",
                    "",
                ]
            )

    lines.extend(["## Questions For Authors", ""])
    if result["questions_for_authors"]:
        lines.extend(f"- {item}" for item in result["questions_for_authors"])
    else:
        lines.append("- None reported.")

    return "\n".join(lines).strip() + "\n"


def write_artifacts(
    result: dict[str, Any],
    *,
    metadata: dict[str, Any],
    output_dir: Path,
) -> Path:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_dir / f"{stamp}-{slugify(metadata['project_name'])}"
    run_dir.mkdir(parents=True, exist_ok=False)

    review_json_path = run_dir / "review.json"
    review_md_path = run_dir / "review.md"
    manifest_path = run_dir / "manifest.json"

    review_json_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    review_md_path.write_text(
        render_markdown(result, metadata=metadata),
        encoding="utf-8",
    )
    manifest_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    return run_dir


def main() -> int:
    args = parse_args()
    load_env_file()
    model = resolve_model(args.provider, args.model)
    api_key = get_api_key(args.provider)

    project_root = normalize_path(args.project_root)
    report_documents = collect_supported_documents([args.report], project_root)
    project_documents = collect_supported_documents(args.files, project_root)

    inline_total = total_inline_bytes(report_documents + project_documents)
    if inline_total > MAX_INLINE_BYTES:
        raise SystemExit(
            "The selected files are too large for the current inline workflow. "
            "Reduce the file set or add a Gemini Files API upload implementation."
        )

    report_document = report_documents[0]
    prompt = build_prompt(
        report_document,
        project_documents,
        args.role,
        args.focus,
        args.project_name,
    )
    result = fetch_review(
        args.provider,
        prompt,
        report_document,
        project_documents,
        api_key=api_key,
        model=model,
        timeout_seconds=args.timeout_seconds,
    )

    metadata = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "project_name": args.project_name,
        "provider": args.provider,
        "model": model,
        "role": args.role,
        "report_path": report_document["path"],
        "project_root": relative_label(project_root, project_root),
        "files": [document["path"] for document in project_documents],
        "focus": args.focus,
    }
    output_dir = resolve_output_dir(project_root, args.output_dir)
    run_dir = write_artifacts(result, metadata=metadata, output_dir=output_dir)
    print(run_dir.as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
