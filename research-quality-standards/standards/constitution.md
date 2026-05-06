# Constitution

Version: 0.1.0
Status: Draft
Last updated: 2026-05-06
Related templates: all
Related examples: `examples/README.md`
Lint opportunities: provenance fields, unresolved-work field, destructive path checks, consistency checks where feasible

## Purpose

This file defines the highest-level principles that apply across genres, stages, and makers.

These principles should change rarely. More specific standards files should interpret and implement them, not contradict them.

## Core Principles

### 1. Reproducibility And Auditability

Outputs must be reproducible and auditable to the degree appropriate for their stage.

A competent reviewer should be able to tell:

- what was produced
- who produced it
- when it was produced
- what inputs or sources it depended on
- what major assumptions shaped it

### 2. Provenance

Every artifact must carry explicit provenance.

At minimum, this means:

- author or responsible agent
- date
- intent
- inputs or sources
- key assumptions

### 3. Epistemic Honesty

Artifacts must not present guesses, interpolations, recalled facts, or implied certainty as verified knowledge.

Facts, calculations, quotations, interpretation, and recommendation must not be blurred.

### 4. Uncertainty And Limits

Material uncertainty, unresolved limitations, and incomplete work must be stated plainly.

Artifacts must not pretend to be more complete, certain, or verified than they are.

### 5. Traceability

Important claims, numbers, and outputs must be traceable to:

- source material
- code or calculation
- observed evidence
- documented judgment

### 6. Scope Discipline

Requested components must not be silently omitted.

Work must not silently expand beyond the requested scope when that expansion affects effort, risk, cost, or interpretation.

### 7. Non-Destructive Handling

Important source material, raw data, and prior artifacts must not be silently overwritten, corrupted, or discarded.

Destructive actions require explicit notice, justification, or both, depending on context.

### 8. Cross-Artifact Consistency

When linked artifacts should agree, they must either be kept consistent or the inconsistency must be disclosed clearly.

This includes code, tables, text, figures, notes, and derived outputs.

### 9. Honest Stage Declaration

The artifact must represent its stage honestly.

Exploratory work may be incomplete, but it must not masquerade as validated draft or submission-ready work.

### 10. Human Reviewability

Artifacts must be legible to a human reviewer without hidden critical steps, undocumented transformations, or unexplained decisions.

## Interpretation Rule

When a more specific standard is ambiguous, interpret it in the direction most consistent with this constitutional layer.

If a lower-level standard appears to conflict with the constitution, the constitution should control unless a human explicitly decides otherwise.
