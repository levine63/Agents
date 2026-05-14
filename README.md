# Agents

## Genre

`custom`

Justification: this is a top-level collection repository that organizes shared agent-related projects and reusable workflow assets rather than one standalone application runtime.

## Summary

This repository is a container for agent-related projects and supporting materials. Its current primary subproject is `./research-quality-standards/`, which now acts as the canonical shared standards hub for reusable quality standards, reviewer prompts, skills, templates, validation helpers, and review automation used by agents such as Codex.

## Quick Start

```bash
python ./research-quality-standards/scripts/validation/verify.py
```

**Expected output**

```text
Scanning for common secret patterns...
No common secret pattern detected.
Running Codex verification...
```

## File Structure

```text
Agents/
|- research-quality-standards/
|  |- standards/
|  |- reviewer_prompts/
|  |- skills/
|  |- templates/
|  |- automation/
|  |- scripts/
|  |- docs/
|  \- README.md
|- README.md
```

## Notes

- `./research-quality-standards/` is the current canonical home for reusable review standards and agent workflow materials.
- Additional agent-related projects may still be added later as separate top-level directories.
