# LLM Review Wrapper for Stata Code

Status: Placeholder
Last updated: 2026-05-15

This reviewer wrapper is intentionally minimal for now.

Use the Stata template and existing Stata standards as the source of truth:

- Template: `templates/code/stata/template.do`
- Standards: `standards/formats/stata/standards.md`

Reviewer guidance for now:

- Focus on reproducibility, path safety, logging, merge safety, seed-setting when randomness is used, and protection of raw data.
- Flag missing provenance notes, silent data changes, unexplained sample restrictions, and unclear output generation.
- If a requirement is missing, say `missing` rather than assuming intent.

This file exists so the Stata bundle has a clear placeholder counterpart until fuller Stata reviewer guidance is written.
