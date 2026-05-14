# Writing Standards

Version: 0.1.0
Status: Draft
Last updated: 2026-05-06
Related templates: `templates/report_skeleton.md`
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
- the reference list should be complete enough that in-text citations can be resolved
- bibliography entries should not be silently missing for cited works

Uncited empirical claims are an `ERROR` at `DRAFT` and `SUBMISSION`.

## Internal Consistency

- abstract, body, tables, and figures should agree
- variables and parameter names should be consistent
- referenced model parameters should match analytic files

Numerical inconsistency between abstract and body is an `ERROR` at `DRAFT` and `SUBMISSION`.

## Scope And Completeness

At `DRAFT` and `SUBMISSION`, the artifact should state:

- target venue or intended audience when known
- document type or section type when relevant
- what remains unresolved
- the document's purpose or contribution early enough that a new reader does not have to infer it from later sections
- whether supporting appendix material exists when the main text relies on it
- whether data/code availability expectations are relevant and, if so, how they will be handled

At `SUBMISSION`, tables and figures should be referenced in the text.

If an appendix exists or is cited for technical detail, robustness, or extra tables, the appendix should be referenced explicitly in the main text where relevant.

For empirical manuscripts approaching submission, include a data/code availability statement or an explicit placeholder noting its status unless journal or funder rules clearly make that inapplicable.

## Language

- use plain, concrete wording where possible
- prefer topic sentences that make the paragraph's job clear
- keep paragraphs organized around one main idea when feasible
- avoid vague nouns such as `issues`, `things`, or `factors` when a more precise term is available
- hedge deliberately, not reflexively
- claims should be tied to evidence, citations, or explicit reasoning rather than left as unsupported assertions
- note counterarguments, alternative explanations, or important competing interpretations when they materially affect the claim
- state important limitations explicitly rather than implying them obliquely
- avoid placeholder text in late-stage drafts

Placeholder text such as `TBD`, `XX`, or `insert here` is an `ERROR` at `SUBMISSION`.
