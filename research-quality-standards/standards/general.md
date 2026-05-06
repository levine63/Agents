# General Standards

Version: 0.1.0
Status: Draft
Last updated: 2026-05-06
Related templates: `templates/report_skeleton.md`
Related examples: `examples/README.md`
Lint opportunities: header presence, date format, `Not Yet Done` section, hard-coded personal paths

## Purpose

These standards apply to all submissions unless a more specific standards file adds tighter requirements.

This file operationalizes `standards/constitution.md`. It should not contradict the constitutional layer.

## Stage Definitions

- `EXPLORATORY`: early notes or rough work used to learn what the problem is
- `ROUGH_DRAFT`: partial but structured work that is not yet ready for broad circulation
- `DRAFT`: work that should be reviewable and substantially reproducible
- `SUBMISSION`: work intended for a PI, stakeholder, publication process, or external release

If stage is not declared, reviewers should treat the work as `DRAFT`.

## Severity Definitions

- `ERROR`: blocks advancement at `DRAFT` and `SUBMISSION`, and usually requires repair before review continues
- `WARNING`: should be fixed before the next stage, but does not always block immediate use
- `STYLE`: preferred practice that usually does not change correctness or usability

## Required Header

Every submission should begin with a header or equivalent metadata block containing:

- `Author`
- `Date`
- `Intent`
- `Inputs`
- `Assumptions`
- `Status / Not Yet Done`

## Header Severity Rules

- Missing header entirely: `ERROR` at all stages except `EXPLORATORY`, where it is `WARNING`
- Missing `Author` or `Date`: `ERROR` at all stages except `EXPLORATORY`, where it is `WARNING`
- Missing or vague `Intent`: `WARNING` at `EXPLORATORY`, `ERROR` at `DRAFT` and `SUBMISSION`
- Missing `Inputs`: `WARNING` at `EXPLORATORY`, `ERROR` at `DRAFT` and `SUBMISSION`
- Missing `Assumptions` when non-trivial choices were made: `WARNING` at `ROUGH_DRAFT`, `ERROR` at `DRAFT` and `SUBMISSION`
- Missing `Not Yet Done`: `STYLE` at `EXPLORATORY`, `WARNING` at `ROUGH_DRAFT`, `ERROR` at `SUBMISSION`

## Constitutional Carry-Through

Reviewers applying this file should also enforce the constitutional expectations of:

- provenance
- reproducibility and auditability
- epistemic honesty
- uncertainty disclosure
- traceability
- scope discipline
- non-destructive handling
- cross-artifact consistency
- honest stage declaration
- human reviewability

## Formatting For Target Platform

The artifact should match its target platform.

- Word or Google Drive documents should not contain raw markdown artifacts
- Markdown files may use normal markdown structure
- Reader-facing tables should be native tables when the platform supports them
- Heading structure should be consistent

Platform-mismatched formatting is usually a `WARNING`, except raw markdown left in Word or Google Drive outputs, which is an `ERROR`.

## Synchronization

If one artifact changes facts, numbers, or definitions used elsewhere, related artifacts should be updated as well.

At minimum, synchronize:

- reader-facing outputs
- code or calculation artifacts that drive those outputs
- assumptions and provenance notes that materially changed

Failure to update related artifacts that creates inconsistency is a `WARNING` at `DRAFT` and may be an `ERROR` at `SUBMISSION`.

## Mixed-Genre Coordination

Some artifacts span multiple genres, such as:

- a manuscript with embedded statistical results
- a results memo with linked analysis code
- an interview summary produced by an LLM agent

In those cases:

- apply `standards/general.md` plus all clearly relevant genre standards
- if requirements differ in strictness, follow the stricter rule unless there is a documented reason not to
- if one artifact cannot practically carry every required detail, the package as a whole must still be reviewable, with clear links between the reader-facing artifact and the supporting materials
- the submission should state which supporting artifacts carry code, provenance, raw outputs, or methodological detail when those are not all contained in the main document

When a reviewer believes combined standards create a practical conflict, the reviewer should identify the conflict explicitly rather than ignoring one standards file silently.

## Maintenance Rule

If the same defect recurs often, do not solve it only by adding more prompt text. Prefer one or more of:

- updating a standards file
- improving a template
- adding a deterministic lint rule
- adding a positive example
