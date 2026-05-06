# Genre Classifier

Version: 0.1.0
Last updated: 2026-05-06

Use this classifier before review. If multiple genres apply, choose `mixed` and load `standards/general.md` plus no more than three specific standards files.

## Allowed Genres

- `readme`
- `software_code`
- `stats_code`
- `statistical_results`
- `writing`
- `interviews`
- `llm_agent_work`
- `mixed`

## Decision Rules

- Use `readme` for project onboarding documents whose main job is to explain setup, execution, dependencies, inputs, outputs, and workflow.
- Use `software_code` for general scripts, utilities, application logic, and automation code.
- Use `stats_code` for code that cleans data, constructs variables, estimates models, or generates statistical outputs.
- Use `statistical_results` for reader-facing tables, regression outputs, simulation results, and empirical summaries.
- Use `writing` for manuscripts, memos, policy briefs, reports, and structured prose.
- Use `interviews` for interview notes, summaries, transcripts, and qualitative field materials.
- Add `llm_agent_work` whenever an LLM or agent produced a material part of the artifact.

## Reviewer Loading Rule

Always load:

- `standards/general.md`

Then load:

- one primary genre standard
- optional `standards/llm_agent_work.md` if applicable
- up to two more specific standards files only if clearly necessary
