# LLM Agent Work Standards

Version: 0.1.0
Status: Draft
Last updated: 2026-05-06
Related templates: `templates/report_skeleton.md`
Related examples: `examples/README.md`
Lint opportunities: model/version field, prompt field, raw markdown in Word-targeted output, emoji scan, citation placeholder scan

## Scope

These standards apply when some or all of a submission is produced by an LLM, scripted agent, or automated pipeline.

## Identity And Transparency

The submission should state:

- model name and version
- generation date
- pipeline name and version when applicable
- prompt or prompt-template reference when feasible

Missing model identity is an `ERROR` at all stages beyond `EXPLORATORY`.

## Verification

The agent must:

- flag claims that depend on recall rather than provided materials
- avoid fabricated citations
- avoid invented numbers
- say when human verification is still needed

Unverified factual claims presented as verified are an `ERROR`.
Fabricated citations are an `ERROR`.
Interpolated or guessed numbers presented as actual values are an `ERROR`.

## Verification Disclosure

Verification disclosure should be explicit enough that a human reviewer can tell which parts are confirmed and which still need checking.

At minimum, the agent should:

- label unverified factual claims as `unverified` or `requires human verification`
- identify the source basis for important numerical claims when available, such as provided file, cited table, calculation, or external source
- say plainly when a citation, number, or factual statement could not be verified from the available materials
- avoid mixing verified and unverified claims in a way that makes the boundary hard to see

For longer outputs, verification status may be conveyed through a dedicated note, a provenance section, or brief inline markers, but the disclosure must be easy to find.

## Scope Discipline

The agent must not silently:

- expand the task
- omit requested components
- work around blocked tasks without disclosing the limitation

Silent omission of a requested component is an `ERROR`.

## Tone And Epistemic Conduct

The agent should not use flattery or confidence theater that obscures uncertainty.

Politeness is acceptable. Sycophancy that substitutes for evidence or hides limits is not.

## Formatting

Word and Google Drive outputs should:

- avoid raw markdown artifacts
- avoid ASCII pipe tables unless explicitly requested
- use consistent headings

Formatting mismatch is usually a `WARNING`, but raw markdown left in a Word or Drive artifact is an `ERROR`.
