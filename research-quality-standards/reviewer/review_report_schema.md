# Review Report Schema

Version: 0.1.0
Last updated: 2026-05-06

Reviewer outputs should follow this structure.

## Header

- Artifact name
- Declared or inferred genre
- Declared or inferred stage
- Reviewer identity
- Standards files applied

## Sections

1. `Verdict`
   One of:
   - `PASS`
   - `PASS WITH MINOR ISSUES`
   - `REVISIONS REQUIRED`
   - `SERIOUS PROBLEMS`

2. `Counts`
   - number of `ERROR`s
   - number of `WARNING`s
   - number of `STYLE` items

3. `Blocking Issues`
   Only `ERROR`s. Each should include location and repair instruction.

4. `Warnings`
   Material issues that should be corrected before the next stage.

5. `Style`
   Non-blocking suggestions.

6. `Missing Information`
   Items the reviewer could not verify because required context or provenance was absent.

7. `Suggested Repair Instructions`
   Short, actionable instructions aimed at the author or repairing agent.

8. `Human Cautions`
   Brief summary of any residual risks or judgment calls a PI should see.
