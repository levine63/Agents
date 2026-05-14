# DOCX Format Standards

## Purpose

These standards apply to `.docx` artifacts edited by agents or humans in this repository ecosystem.

A `.docx` file is not plain text. It is a structured artifact with:

- semantic hierarchy
- named styles
- cross-references
- citation fields
- equations
- tables
- pagination logic
- headers and footers
- hidden metadata
- rendering behavior that may matter for submission, review, or operations

The primary objective is:

- make the smallest correct change while preserving document integrity

Use these standards together with the relevant genre standard, such as `academic_paper`, `README`, or `meeting_notes`.

## Core principles

### Scoped edits only

Modify only the requested sections, paragraphs, tables, figures, equations, captions, notes, or metadata.

Do not:

- rewrite nearby prose without cause
- normalize style globally
- reflow sections unnecessarily
- "clean up" unrelated formatting
- regenerate the full document unless explicitly requested

Prefer:

- paragraph-level patches
- object-level replacements
- section-local edits

### Atomic patching

If one sentence changes, edit the sentence only.

If one table changes, replace or repair the table only, not the surrounding section structure.

Full-document regeneration is a last resort and requires an explicit reason.

### Preservation over polish

Preserve document structure and rendering behavior even when the local formatting looks unusual.

Assume heterogeneous formatting may be intentional unless there is evidence otherwise.

## Structural metadata preservation

Treat the following as critical infrastructure:

- bookmarks
- cross-references
- citation field codes
- Zotero, EndNote, or Mendeley links
- bibliography fields
- caption numbering
- table numbering
- footnotes and endnotes
- comments
- tracked changes
- hyperlinks
- index markers
- table of contents fields
- section breaks
- page numbering logic
- headers and footers
- alt text and accessibility metadata

Do not break, flatten, or silently discard these structures.

## Reversibility and backups

Before editing, preserve a rollback path.

Preferred backup pattern:

- `backups/YYYY-MM-DD_HHMM_filename.docx`

For larger edits, also preserve:

- an intermediate version after major structural changes
- a short change summary
- a record of the backup location in the final report

## Styles and formatting discipline

### Use named styles

Prefer the document's existing named styles, such as:

- `Heading 1` through `Heading 4`
- `Normal`
- `Caption`
- `Quote`
- `Bibliography`
- table-text or note styles already present in the file

Avoid hard formatting when a named style exists.

Examples to avoid:

- manual font-family changes
- ad hoc font-size changes
- direct indentation hacks
- local numbering hacks
- paragraph-by-paragraph spacing overrides without cause

### No global normalization

Do not globally normalize:

- fonts
- spacing
- quotation marks
- citation punctuation
- indentation
- numbering

unless explicitly requested.

### Section-break safety

Section breaks are high-risk objects.

Do not modify section breaks unless necessary for the requested change.

When landscape orientation is needed:

- isolate the landscape region to the smallest practical section
- preserve header and footer logic
- preserve page numbering continuity
- verify margins and page orientation afterward

## Equation standards

### Prefer native equation objects

Prefer editable Word equation objects when possible.

Avoid:

- plaintext pseudo-equations
- screenshots of equations
- low-resolution equation images

If LaTeX content must be inserted, convert it into an editable equation object whenever practical.

### Preserve equation integrity

Do not:

- rasterize existing equations
- flatten editable equations into images
- break equation numbering
- leave clipped fractions, misaligned matrices, or malformed subscripts

## Table standards

### Readability first

Tables must remain readable in Word and after PDF export.

Prefer:

- sensible column widths
- repeated header rows where appropriate
- controlled wrapping
- captions attached to the correct object

Avoid:

- clipped columns
- invisible overflow
- single-character wrapping
- giant whitespace gaps

### Landscape review

Wide tables should trigger a landscape review rather than an automatic landscape conversion.

Before adding a landscape section, try:

- autofit behavior changes
- moderate font reduction
- reduced cell padding
- locally tighter margins

Only then add a landscape section if needed.

### Pagination hygiene

Avoid:

- orphaned table headers
- captions separated from tables
- unstable page splits
- single-row carryovers when avoidable

## Citation and cross-reference integrity

### Preserve citation systems

Never intentionally break citation-management structures.

Do not:

- convert linked citations to plain text by accident
- strip bibliography-field logic
- detach bibliography generation from the current citation system

### Reference QA

After edits, verify that references still resolve correctly where feasible.

Examples:

- `Table 2`
- `Figure 5`
- `Appendix B`
- `Equation (3)`

High-severity problems include:

- `Error! Reference source not found`
- broken hyperlinks
- duplicated numbering
- corrupted caption sequences

## Editing-mode expectations

### Track changes default

If the workflow supports tracked changes, default to preserving or using tracked changes unless instructed otherwise.

Do not silently accept or reject tracked changes without instruction.

### No-clean rule

Do not use a substantive edit request as a license to rewrite academic or operational prose for style.

Tone, hedging, legal phrasing, or caveat structure may be intentional.

### Evidence verification

If empirical results, counts, citations, or factual statements are updated, verify them against authoritative source artifacts when available.

Never invent:

- coefficients
- standard errors
- p-values
- Ns
- confidence intervals
- citations

## Visual QA requirements

Edits are not complete until affected pages have been visually inspected in a rendered form when tooling allows.

Preferred inspection path:

- render to PDF
- or render to page images

Inspect affected pages and nearby pages for:

- clipped tables
- shifted margins
- overlapping objects
- missing glyphs
- blank pages
- broken numbering
- damaged headers or footers
- equation corruption
- excessive whitespace
- ugly wrapping

## Reporting requirements

Every substantial DOCX editing session should report:

- what was modified
- what nearby structures were intentionally preserved
- what checks were performed
- what warnings or unresolved issues remain
- where the backup or rollback copy lives

## Automation and linting guidance

Where tooling exists, DOCX automation should prefer:

- automatic backups before edits
- non-destructive patching
- render-and-inspect workflows
- targeted linting for common failures

Helpful automated checks may flag:

- broken references
- corrupted tables of contents
- missing captions
- overflow tables
- rasterized equations
- missing bibliography fields
- unresolved tracked changes
- missing alt text
- absolute local file paths

Suggested severity model:

- `BLOCKER`
- `WARNING`
- `INFO`

## Agent-specific interaction rules

When agents edit `.docx` artifacts:

- preserve surrounding layout unless change requires otherwise
- avoid unrelated formatting drift
- prefer duplicating or backing up before risky structural edits
- preserve comments, notes, and speaker-like supporting content unless instructed otherwise
- flag interpretation-sensitive changes for human review rather than silently rewriting conclusions

## Bottom line

The `.docx` editor is not primarily a coauthoring engine.

It is:

- a precision patching system
- a formatting preservation system
- a rendering integrity system

Correctness and preservation outrank stylistic elegance.
