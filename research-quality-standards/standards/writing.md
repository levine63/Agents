# Writing Standards

Version: 0.1.0
Status: Draft
Last updated: 2026-05-06
Related templates: `templates/papers/report_skeleton.md`
Related examples: `examples/README.md`
Lint opportunities: placeholder text, acronym expansion markers, section references, citation placeholders

## Scope

These standards apply to manuscripts, memos, reports, policy writing, and other reader-facing prose.

## Acronyms

- spell out acronyms at first use unless a clear local convention says otherwise
- after first use, use the acronym consistently
- if many acronyms are used, provide a glossary or abbreviations list at `SUBMISSION`

Acronym not spelled out at first use is an `ERROR` at `ROUGH_DRAFT`, `DRAFT`, and `SUBMISSION`.

## Citation And Attribution

- empirical claims should be cited
- placeholders such as `[CITE]` or `TBD citation` should be recorded in `Not Yet Done`
- citation style should be consistent

Uncited empirical claims are an `ERROR` at `DRAFT` and `SUBMISSION`.

## Internal Consistency

- abstract, body, tables, and figures should agree
- variables and parameter names should be consistent
- referenced model parameters should match analytic files

Numerical inconsistency between abstract and body is an `ERROR` at `DRAFT` and `SUBMISSION`.

## Scope And Completeness

At `DRAFT` and `SUBMISSION`, the artifact should state:

- target venue or target audience when known
- document type or section type when relevant
- what remains unresolved

At `SUBMISSION`, tables and figures should be referenced in the text.

## Language

- use plain, concrete wording where possible
- hedge deliberately, not reflexively
- avoid placeholder text in late-stage drafts

Placeholder text such as `TBD`, `XX`, or `insert here` is an `ERROR` at `SUBMISSION`.

