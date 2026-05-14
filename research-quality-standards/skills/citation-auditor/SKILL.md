---
name: citation-auditor
description: Use when reviewing research manuscripts, reports, slide decks, or related scholarly writing for inline citation coverage, bibliography integrity, DOI validity, journal-style compliance, or claim-to-source support, especially near submission or when hallucinated or bluffing citations are a risk.
---

# Citation Auditor

## Purpose

Use this skill to audit citations in scholarly or research-facing writing.

The core job is to verify:

- inline citations versus bibliography coverage
- whether cited works appear to be real and correctly identified
- whether bibliography formatting matches the target venue when one is specified
- optionally, whether cited sources actually support the claims attached to them

This skill is for auditing, not for inventing references or laundering weak citations into plausible-looking ones.

## Modes

### Default mode: citation integrity audit

Run this by default.

It includes:

- cross-reference audit
- reality check
- style or journal-compliance check

### Optional mode: semantic audit

Run this only when:

- the user explicitly asks for it
- the manuscript is approaching submission
- the manuscript makes high-stakes empirical or causal claims

Semantic audit is slower and more expensive than ordinary citation checking.

If the user has not asked for it but the manuscript appears near submission, prompt briefly about whether to include semantic audit.

## Inputs

Gather only what is needed:

- the manuscript text or excerpt
- the bibliography or references section
- the target journal or style guide if known
- any prior checked-claims ledger if one exists

Helpful companion artifacts:

- `templates/papers/citation_discrepancy_table_template.md`
- `templates/papers/checked_claims_ledger_template.csv`

## Core workflow

### 1. Extract the citation surface

Identify:

- inline citations
- bibliography entries
- cited DOIs if present
- obvious footnote-style or author-year variants

Normalize enough to compare like with like, but do not silently rewrite the manuscript.

### 2. Run the cross-reference audit

Compare every inline citation against the bibliography.

Flag:

- inline citations missing from the bibliography
- bibliography entries never cited in the text
- ambiguous or inconsistent author-year forms
- duplicate or conflicting entries that appear to refer to the same work

### 3. Run the reality check

For each bibliography entry, verify as far as available tools allow that it appears to be a real publication.

Check:

- author names
- title plausibility
- venue plausibility
- year plausibility
- DOI validity when a DOI is given

Flag:

- suspicious or hallucinated publications
- malformed DOIs
- metadata that does not point to the cited work

If external verification tools are unavailable, state that clearly and downgrade the certainty of the reality check rather than pretending it was completed.

### 4. Run the journal-compliance check

If a target journal or style is specified, compare the bibliography formatting against that style.

Examples of issues to flag:

- author formatting
- initials
- title capitalization
- italics
- bolding
- punctuation
- journal-name formatting
- issue and volume formatting
- page-range formatting

If no target style is specified, say so explicitly and default to structural integrity rather than style policing.

### 5. Decide whether semantic audit is needed

Semantic audit is not automatic in ordinary drafting.

Prompt for it when:

- the manuscript is near submission
- the claims are central and high-stakes
- the risk of citation bluffing appears non-trivial

If semantic audit is not requested and not clearly necessary, stop after integrity, reality, and style review.

### 6. Run semantic audit when requested

For each selected claim-citation pair:

- locate the cited paper
- identify what the paper actually establishes
- compare that support to the manuscript's claim

Flag:

- citation bluffing
- irrelevant citations
- overclaiming
- citing correlational work for causal claims without qualification
- citing review language that the underlying source does not support

Do not over-audit routine background citations unless the user asks for exhaustive checking.

## Checked-claims ledger

To avoid repeating semantic audits, maintain a claim ledger when the workflow supports it.

Use:

- `templates/papers/checked_claims_ledger_template.csv`

Record at minimum:

- a stable claim excerpt
- the paired citation
- the audit mode
- the audit result
- the audit date

If the claim text and citation pair are unchanged, do not re-run the semantic audit unless the user requests a refresh.

If the claim wording changes materially or the citation changes, treat it as a new audit item.

## Output requirements

The output should always include a discrepancy table.

Use this structure:

| Citation | Issue Type | Detail | Fix Suggested |
|---|---|---|---|

Issue types may include:

- `Missing`
- `Format`
- `Reality`
- `Semantic`
- `Duplicate`
- `Ambiguous`

Also provide a short narrative summary of:

- overall integrity status
- major risks
- whether semantic audit was run, skipped, or recommended

## Reviewer stance

- Be skeptical rather than encouraging.
- Do not infer that a plausible-looking citation is real without evidence.
- Do not treat formatting polish as more important than citation integrity.
- Do not claim that semantic support was verified unless the source itself was checked.
- When evidence is incomplete, say exactly what remains unverified.

## Bottom line

This skill is meant to catch:

- missing citations
- hallucinated references
- malformed DOIs
- journal-style failures
- citation bluffing

before those issues reach submission, peer review, or public circulation.
