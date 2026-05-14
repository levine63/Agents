# Research Quality Standards Hub

## Purpose

This repository is the shared standards, review, templates, and automation hub for research and agent work.

## Find Things Fast

### Standards and reviewer prompts stay together

Use `standards/` when you want the rules for how something should be written, reviewed, or structured.

- Genre standards live in `standards/genres/<genre>/`
- Format standards live in `standards/formats/<format>/`
- Reviewer prompts usually live beside the corresponding standard as `reviewer_prompt.md`

Examples:

- `standards/genres/survey/standards.md`
- `standards/genres/survey/reviewer_prompt.md`
- `standards/formats/python/standards.md`
- `standards/formats/python/reviewer_prompt.md`

### Templates stay together

Use `templates/` when you want a starter file to copy and fill in.

Examples:

- manuscripts: `templates/papers/`
- surveys: `templates/surveys/`
- weekly reports: `templates/weekly_reports/`
- project READMEs: `templates/README/`
- code templates: `templates/code/`

### Code templates

Code templates are now under `templates/code/`, not under `standards/`.

Use:

- generic Python: `templates/code/python_general/template.py`
- Python stats/research: `templates/code/python_stats/template.py`
- Stata: `templates/code/stata/template.do`

### Counterpart links

When helpful, a standard can link to its counterpart template using a normal relative Markdown link.

That is the GitHub-friendly counterpart to a Windows shortcut.

Example:

- a survey standard can link to `templates/surveys/household_survey_master_template.md`

## Start Here

- `standards/INDEX.md`
- `templates/INDEX.md`
- `skills/INDEX.md`
- `CAPABILITIES.md`
- `AGENTS.md`

## Main Areas

- `standards/`: canonical standards and review wrappers
- `templates/`: canonical starter templates
- `skills/`: reusable review and workflow skills
- `reviewer_prompts/`: shared top-level reviewer prompts where still useful
- `automation/`: Apps Script and workflow automation
- `scripts/`: linting, validation, and utilities
- `docs/`: workflow and architecture notes

## Practical Rule

If you are asking:

- "What are the rules?" go to `standards/`
- "Give me a starter file" go to `templates/`
- "How should an agent apply this?" look for `reviewer_prompt.md` next to the standard

## Quick Start

```bash
python ./scripts/validation/verify.py
```
