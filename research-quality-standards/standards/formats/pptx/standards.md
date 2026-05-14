# PPTX Format Standards

Use for PowerPoint or slide-deck files in `.pptx` format.

Apply these standards together with any relevant genre standard, especially `standards/genres/presentation/standards.md`.

If presentation-purpose and PowerPoint-format guidance conflict, the genre standard governs semantic content and the format standard governs file-specific execution.

## 1. Readability and layout

### 1.1 Minimum font size

Avoid text below:

- `14 pt` for primary presentation content

Smaller text may be acceptable for:

- appendix slides
- figure notes
- references
- dense technical backup material

only if readability remains adequate during projection or screen sharing.

Larger fonts are preferred for:

- key findings
- slide titles
- operational decisions

### 1.2 Readability over compression

Prefer:

- whitespace
- fewer bullets
- multiple slides
- progressive disclosure

Avoid:

- shrinking charts
- overcrowding tables
- excessive animation
- wall-of-text slides

### 1.3 Explicit labeling

All data-driven visuals should clearly specify:

- units
- sample sizes (`N`)
- treatment/control definitions
- axis labels
- time periods
- uncertainty measures where relevant
- data source when appropriate

Avoid unlabeled charts or unexplained abbreviations.

### 1.4 Acronyms and technical language

Spell out acronyms at first use within a section or presentation.

Example:

- `Institutional Review Board (IRB)`

Assume mixed audiences unless the deck is explicitly specialized.

## 2. Accessibility and usability

### 2.1 Color accessibility

Do not rely solely on color distinctions.

Use:

- labels
- patterns
- annotations
- direct labeling

when colorblind confusion is possible.

### 2.2 Projection robustness

Slides should remain legible when:

- projected
- screen-shared
- viewed remotely
- displayed on smaller screens

Before finalization:

- review slides in presentation mode
- verify readability at realistic viewing sizes
- check charts and tables under projection conditions when feasible

### 2.3 Animation restraint

Use animations only when they improve comprehension.

Avoid:

- distracting transitions
- excessive motion
- animation-dependent logic that fails in PDF export or screen sharing

## 3. Agent-specific editing rules

### 3.1 Scoped edits only

When updating or revising slides:

- preserve surrounding context unless explicitly instructed otherwise
- avoid unnecessary layout changes
- avoid modifying unrelated slides
- minimize visual disruption

Prefer small targeted edits over broad rewrites.

### 3.2 Preserve visual structure

Do not remove, resize, reposition, or restyle:

- manually placed diagrams
- annotations
- arrows
- screenshots
- branding elements
- user-created layouts

unless explicitly requested.

Assume unusual spacing or positioning may carry meaning.

### 3.3 Conservative interpretation updates

When statistical values or figures change:

- update the numerical results
- preserve surrounding interpretation when still broadly accurate
- flag slides requiring human review if interpretation may materially change

Examples:

- sign reversal
- loss of significance
- major effect-size change
- conflicting robustness results

Avoid silently rewriting conclusions.

### 3.4 Preserve appendix and hidden slides

Do not:

- delete backup slides
- remove hidden slides
- collapse appendix sections
- discard exploratory material

unless explicitly instructed.

If uncertain:

- preserve the original
- move questionable material into a `Review Required` section
- or duplicate the slide before revision

### 3.5 Preserve speaker notes

Do not overwrite or delete speaker notes unless explicitly requested.

### 3.6 Prefer duplication over destructive edits

If a major structural change is uncertain:

- duplicate the slide
- apply revisions to the duplicate
- preserve the original for comparison

### 3.7 Flag possible stale interpretations

If updated figures may invalidate nearby claims:

- flag the slide for review
- summarize the possible inconsistency
- avoid inventing revised interpretations unsupported by the evidence

### 3.8 Recommended analytical-slide layout

For analytical or evidence-heavy slides, this pattern is often effective:

- title: key claim or takeaway
- center: primary evidence such as chart, table, or diagram
- lower area: technical notes, Ns, uncertainty measures, source references, or reproducibility metadata

This is a recommendation, not a mandatory layout.

## 4. Finalization workflow

Before finalizing a `.pptx` deck:

- verify that slide titles communicate conclusions or purpose
- run deterministic checks where available
- verify figures and statistics against current outputs
- check readability in presentation mode
- remove or archive obsolete duplicate slides
- confirm appendix references and links function correctly
- verify that labels, Ns, and units are consistent
- confirm that reproducibility metadata is current when used
