# README Standards

Version: 0.1.0
Status: Draft
Last updated: 2026-05-06
Related templates: `templates/README/project_readme_template.md`
Related examples: `examples/README.md`
Lint opportunities: required section presence, placeholder text, broken relative paths, `.env.example` references, missing quick start

## Scope

These standards apply to project `README.md` files and similar onboarding documents.

A README is not just project decoration. It is an operational handoff document. A new contributor should be able to understand what the project is, what it depends on, what is intentionally excluded, and how to produce a meaningful visible output without guessing hidden steps.

Apply `standards/general.md` and, when relevant, also apply:

- `standards/software_code.md`
- `standards/stats_code.md`
- `standards/statistical_results.md`
- `standards/llm_agent_work.md`

## First Rule

For most projects, a new contributor should be able to go from clone to one meaningful visible output using only the README in five minutes or less on a fresh machine.

If large downloads, model pulls, or external services make that unrealistic, the README should state:

- expected first-run time
- expected later-run time
- which steps are slow because of downloads, remote APIs, or heavyweight setup

The build and core execution path, excluding those heavy external steps, should still be quick and explicit.

## Genre

Each README should identify the closest project genre:

- `replication_repo`
- `data_analysis`
- `application_code`
- `library_or_tooling`
- `mixed_or_llm_pipeline`
- `custom`, with justification

If the project mixes several genres, state the dominant one and name the secondary ones in the summary or scope section.

`Custom` is appropriate when the repository is primarily a collection, index, standards hub, or meta repository rather than a single runnable application or pipeline. In that case, the README should say so explicitly and should still provide one meaningful quick-start command, often by validating or demonstrating the primary contained project.

## Required Sections

Every project README should contain, at minimum:

- `Title`
- `Summary`
- `Quick Start`
- `Environment`
- `Data and Inputs`
- `Outputs`
- `Reproducibility`
- `Tests and Validation`
- `Assumptions`
- `Limitations and Risks`
- `Not Included`
- `File Structure`
- `Contributing or Workflow`
- `Contact or Ownership`
- `License`

`Citation` is strongly recommended for reusable research or software projects.

## Quick Start

The `Quick Start` section should:

- include a copy-pasteable command sequence
- use repository-relative paths where paths are shown
- produce at least one visible output, health check, or saved artifact
- state the expected visible result
- avoid undocumented interactive prompts

When a one-line command is realistic, prefer one line. When it is not realistic, keep the command block short and explain why.

The minimal example should usually live under `./examples/minimal/`. If that is not appropriate, the README should say why.

A `Quick Start` that cannot plausibly be run from the README, or that does not say what success looks like, is an `ERROR` at `DRAFT` and `SUBMISSION`.

## Environment And Dependencies

The README should state:

- exact runtime versions when they materially affect behavior
- operating systems tested when platform differences materially affect behavior
- lockfiles used by the project
- system dependencies such as Docker, Graphviz, pandoc, Java, or database services
- whether `.env.example` must be copied or edited

Never place real secrets in the README. If environment variables are required, document them with dummy values only.

For non-trivial replication, data analysis, and mixed or LLM pipeline projects, Docker or a dev container is strongly recommended when feasible.

Missing or vague dependency information is a `WARNING` at `ROUGH_DRAFT` and an `ERROR` at `DRAFT` and `SUBMISSION`.

## Data And Inputs

The README should explain:

- major inputs and where they come from
- access restrictions or licenses when relevant
- expected schemas, contracts, or required fields when those are not obvious
- the minimal runnable example input, preferably under `./examples/minimal/`

If the project uses large data, paid APIs, or gated sources, say so explicitly.

For analysis or replication work, dataset provenance and access instructions are an `ERROR` at `DRAFT` and `SUBMISSION`.

## Outputs

The README should identify:

- main output files or directories
- output formats
- which outputs are deterministic
- which outputs depend on external services, LLMs, or manual review

If the quick start claims a visible output, the README should say where that output appears.

## Reproducibility

The README should document:

- the exact reproduction command or command sequence
- seed expectations when randomness exists
- whether results are fully deterministic, partially deterministic, or nondeterministic
- which external conditions can change outputs, such as API drift, model changes, or upstream data updates

For LLM or mixed pipelines, state:

- which steps are deterministic
- which steps are model-driven
- model provider, model name, and major settings when relevant
- known failure modes such as hallucination, omission, or classification instability

## Tests And Validation

The README should say:

- how to run tests or validation checks
- what a passing result looks like
- which validations are automated versus manual
- what is not currently covered by tests
- at least one integration or smoke check for the minimal example when feasible

If a project has no tests, the README should say what lightweight validation replaces them and why.

At `SUBMISSION`, a README that omits validation guidance entirely is an `ERROR`.

## Assumptions, Limitations, And Not Included

These sections are important enough to stand on their own.

The README should state:

- key assumptions needed to run or interpret the project
- main limitations or failure modes
- what the repository intentionally does not include

Typical `Not Included` items may include:

- large raw data
- production secrets
- proprietary models or weights
- manual labeling steps
- deployment infrastructure
- non-public supporting artifacts

If important exclusions are real but unstated, that is a `WARNING` at `DRAFT` and may become an `ERROR` at `SUBMISSION`.

## File Structure And Paths

The README should show the major project layout and use relative repository paths in documentation examples unless an external absolute path is truly required.

If the README references important files, scripts, or folders, those paths should exist or be clearly marked as planned.

Broken or misleading repo-relative path references are a `WARNING` at `DRAFT` and an `ERROR` at `SUBMISSION`.

## Troubleshooting

When the project is non-trivial, include a `Troubleshooting` or `Common Issues` section with real failure cases.

Prefer at least:

- one dependency or setup issue
- one operating-system-specific issue when platform differences matter
- two concrete issues overall, unless the README explains briefly why that would be artificial

For tiny projects where this would be artificial, state briefly why troubleshooting is minimal.

## Glossary

If the README uses domain terms or project-specific language that may confuse a new contributor, include a short glossary with no more than about five terms.

If more are needed, move the extras to `./docs/glossary.md` or an equivalent glossary file.

## Genre-Specific Add-Ons

### Replication Repo

Add:

- dataset provenance and license
- access instructions and size notes
- exact table and figure reproduction steps
- output checksums or key expected metrics when feasible
- archive or artifact registry location when one exists

### Data Analysis

Add:

- pipeline stages and data flow
- codebook or variable-definition pointer
- notebook execution order when notebooks matter
- major exclusions, filters, or cleaning assumptions
- unit of observation
- units for key variables when they are not obvious

### Application Code

Add:

- local development run instructions
- health-check command or smoke test
- main entry points such as UI URL, API route, or CLI command
- environment variable setup using `.env.example`
- local supporting services when relevant, such as a database, queue, or mock external dependency

### Library Or Tooling

Add:

- installation command
- minimal input-to-output example
- supported CLI or API surface
- supported runtime versions when they materially affect compatibility
- contracts or schemas when relevant
- versioning or backward-compatibility notes when relevant

### Mixed Or LLM Pipeline

Add:

- deterministic versus LLM-driven steps
- prompt locations when prompts live in the repo
- provider, model, and major settings when relevant
- expected token or cost implications for example runs when material
- guardrails, invariants, and evaluation notes
- what is validated by automated checks versus human review
- what is known to drift over time, such as upstream models, prompts, or external services

## Genre-Specific Requirements Explained

These add-ons exist because README risks differ by project type. The goal is not to force every project into the same mold. The goal is to make the README sufficient for its actual genre.

For all genres:

- keep the README concise, but not at the expense of hidden setup or hidden risk
- keep `Not Included` explicit
- prefer reviewer-checkable wording over vague claims
- prefer static facts over aspirational language about what "should" work

When a project is hybrid:

- choose one primary genre
- add secondary-genre requirements only when they materially affect setup, execution, interpretation, or trust

### Replication Repo

Purpose: enable reproduction of the paper's results closely enough for another researcher to verify the claims.

Required:

- dataset provenance, license, access instructions, and size or timing notes when large
- explicit commands or numbered steps to reproduce tables, figures, or core outputs
- fixed seeds when randomness exists
- a concrete validation target, such as matching checksums, matching saved artifacts, or matching key metrics within stated tolerance

Recommended:

- artifact registry or archive location

Why it matters: replication work fails when data access, execution order, or expected outputs are left implicit.

### Data Analysis

Purpose: make the analytic path transparent, auditable, and repeatable.

Required:

- pipeline stages or execution order
- codebook or variable-definition pointer for important variables
- unit of observation
- major exclusions, filters, or cleaning assumptions

Recommended:

- numbered notebook order when notebooks are part of the workflow
- brief note on where key transformations happen

Why it matters: hidden filtering, undocumented transformations, and unclear units make analysis hard to trust or extend.

### Application Code

Purpose: let a new contributor run the project locally and verify core behavior quickly.

Required:

- local run instructions
- environment-variable setup via `.env.example` when relevant
- main entry points such as primary UI routes, API endpoints, or CLI commands
- one health check or smoke test

Recommended:

- note local supporting services such as databases, queues, caches, or external-service mocks

Why it matters: application onboarding breaks down when startup steps, configuration, or success checks are scattered across tribal knowledge.

### Library Or Tooling

Purpose: help users and contributors consume the tool safely and understand its interface boundaries.

Required:

- installation command
- at least one minimal input-to-output example
- the main CLI or API surface

Recommended:

- supported runtime versions
- schema or contract references
- versioning or backward-compatibility notes when relevant

Why it matters: consumers care most about interface, compatibility, and a fast proof that the tool works.

### Mixed Or LLM Pipeline

Purpose: make nondeterministic and model-driven steps visible enough to debug, evaluate, and trust.

Required:

- clear distinction between deterministic steps and model-driven steps
- prompt locations when prompts live in the repo
- provider, model, and major settings when relevant
- major failure modes
- what is validated automatically versus by human review

Recommended:

- rough token, latency, or cost expectations for example runs when material
- explicit note on what is likely to drift over time

Why it matters: LLM pipelines can appear runnable while hiding nondeterminism, model drift, cost, and evaluation weaknesses.

## Stage Guidance

- `EXPLORATORY`: a shorter README is acceptable, but the project should still identify purpose, dependencies, and known gaps
- `ROUGH_DRAFT`: core sections should exist, even if some are brief
- `DRAFT`: the README should be runnable, honest, and suitable for handoff
- `SUBMISSION`: the README should be accurate enough for external or PI-facing use and should not rely on tribal knowledge

## High-Priority Failure Modes

Treat the following as especially serious:

- no actionable quick start
- hidden dependencies or missing system requirements
- claimed outputs that the README does not explain how to obtain
- real secrets or unsafe instructions
- README text that contradicts actual repo structure or workflow
- failure to disclose large missing pieces under `Not Included`

