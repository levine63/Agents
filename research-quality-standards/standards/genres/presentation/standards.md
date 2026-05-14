# Presentation Standards

Use for slide-based presentations intended for:

- academic talks
- lab meetings
- operational reviews
- conference presentations
- funder updates
- teaching
- internal decision-making

These standards prioritize:

- rapid comprehension
- operational clarity
- statistical integrity
- traceable evidence
- decision support

Decorative design is secondary to communication quality and interpretability.

## 1. Structure and narrative logic

### 1.1 Decision-oriented titles

Each slide title should communicate:

- the main finding
- the operational implication
- or the purpose of the slide

Prefer titles such as:

- `Treatment increased uptake by 12 percentage points`
- `Enumerator attrition concentrated in two districts`
- `Proposed workflow for survey QA`
- `Three candidate explanations for low adherence`

Avoid generic titles such as:

- `Results`
- `Analysis`
- `Findings`
- `Discussion`

Titles should usually function as standalone summaries.

### 1.2 One primary idea per slide

Slides should usually communicate one primary idea.

If a slide contains:

- multiple unrelated findings
- dense text
- several competing visuals

split it into multiple slides rather than shrinking content to fit.

Comparison or workflow slides may contain multiple linked components if the relationships are visually and conceptually clear.

### 1.3 Explicit narrative flow

Presentations should support a clear progression such as:

- question
- motivation
- method
- evidence
- interpretation
- implication
- next step

Avoid abrupt transitions or unexplained jumps in logic.

### 1.4 Progressive disclosure

Use:

- main slides for core conclusions
- appendix slides for robustness
- backup slides for technical detail

Do not overload primary narrative slides with every caveat or specification.

## 2. Evidence communication

### 2.1 Self-contained figures and tables

Figures and tables should be understandable with minimal verbal explanation.

Include:

- informative titles
- labeled axes
- legends where needed
- concise notes
- clear highlighting of key comparisons

### 2.2 Statistical integrity

Reported values must match:

- current analysis scripts
- regression outputs
- source datasets
- canonical analysis artifacts

Before finalization:

- rerun figures and tables when feasible
- or verify values against canonical outputs

If figures are manually copied into slides, verify that stale values have not persisted after analysis updates.

### 2.3 Readable use of tables

Do not paste large regression tables directly into primary slides.

Instead:

- highlight key coefficients
- simplify rows
- focus on substantive interpretation
- move full tables to appendix slides

Primary slides should optimize for comprehension, not completeness.

### 2.4 Visual honesty

Avoid misleading presentation choices such as:

- truncated axes without explicit indication
- inconsistent scales across comparison charts
- distorted aspect ratios
- exaggerated visual effects
- selective visual emphasis unsupported by the data

When axes are truncated or transformed, indicate this clearly.

### 2.5 Figure consistency

Within a presentation, use consistent:

- labels
- color conventions
- terminology
- scales when comparing related figures

Do not change treatment labels, units, or color meanings across slides without explanation.

## 3. Operational integrity and reproducibility

### 3.1 Source traceability

Slides presenting analytical or operational results should reference canonical source artifacts when feasible.

Examples:

- GitHub repositories
- analysis scripts
- Google Sheets
- dashboards
- canonical datasets

The goal is to make it possible to trace important results back to their source.

### 3.2 Reproducibility metadata

For automated outputs, include reproducibility metadata in:

- slide notes
- appendix slides
- or supporting documentation

Examples:

- Git commit hash
- analysis date
- dataset version
- script name
- pipeline identifier

This is especially important for:

- recurring reports
- operational dashboards
- evolving analyses

### 3.3 Version control and naming

Presentations should include:

- date
- version
- or revision identifier

Avoid ambiguous filenames such as:

- `final_v2_REALFINAL.pptx`

Use meaningful, traceable naming conventions.

## 4. Audience and decision support

### 4.1 Audience calibration

Adjust:

- terminology
- detail level
- statistical depth
- operational framing

for the intended audience.

Examples:

- policymakers
- NGO staff
- technical researchers
- field teams
- funders
- students

### 4.2 Communication over decoration

Presentations should optimize for:

- understanding
- operational decisions
- evidence communication

Avoid decorative complexity that reduces comprehension.

## 5. Common failure modes

Flag:

- generic slide titles
- overcrowded slides
- unreadable tables
- unlabeled axes
- inconsistent terminology
- stale statistics
- unexplained acronyms
- missing Ns or units
- appendix slides disconnected from the main narrative
- duplicated contradictory figures
- unsupported visual emphasis
