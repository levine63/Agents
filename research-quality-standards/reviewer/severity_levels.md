# Severity Levels

Version: 0.1.0
Last updated: 2026-05-06

## Definitions

- `ERROR`: high-risk defect that blocks advancement at `DRAFT` and `SUBMISSION`
- `WARNING`: significant issue that should be fixed before the next stage
- `STYLE`: preferred improvement that usually does not affect validity or usability

## Escalation Rule

Treat missing or weak items more strictly as stage rises:

- `EXPLORATORY`: note major risks, but do not expect publication-grade polish
- `ROUGH_DRAFT`: structure should exist, but incomplete items may remain
- `DRAFT`: core reproducibility, evidence, and provenance expectations apply fully
- `SUBMISSION`: reader-facing consistency and compliance should be complete

## Reporting Rule

Each issue should include:

- severity
- location
- description
- why it matters
- required fix or suggested fix
