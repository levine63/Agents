# Workflow: AI Referee Review

## Purpose

Use a second model, such as Claude, as a referee against the relevant standards.

This workflow is normally required for Tier 2 work, optional for Tier 1 work, and usually skipped for Tier 0 work.

## When to review

Run AI review for:

- substantial code changes
- statistical analysis
- data cleaning pipelines
- research memos
- public-facing documents
- standards or workflow changes
- anything marked MEDIUM or HIGH risk

AI review may be skipped for trivial typo fixes or small formatting changes.

For commit discipline:

- review should usually happen before a meaningful Tier 2 commit
- a fresh review is not required if a recent review already covered materially the same diff
- rerun review when the artifact, logic, claims, or workflow changed substantially after the last review

If AI review is unavailable, fails, or is not permitted:

- do not fabricate review output
- complete deterministic verification if possible
- document the missing review and why it was skipped
- require human review before treating the work as fully cleared when Tier 2 review would normally be required

## Review input packet

Send the reviewer:

1. task summary
2. artifact or diff
3. genre classification
4. risk level
5. relevant standards
6. review contract
7. specific questions, if any

Do not send unrelated standards.

## Review output

Reviewer must return:

- status
- severity-coded findings
- exact locations when possible
- repair instructions
- unresolved cautions
- whether human review is needed

Use `templates/referee_report_template.md`.

## After review

Codex should:

1. repair BLOCKER and ERROR issues
2. consider WARNING issues
3. ignore STYLE issues only with reason
4. rerun relevant verification
5. update final report
6. record review usefulness and friction in `logs/AGENT_EXPERIENCE_LOG.md` when the session qualifies under `AGENTS.md`

Reviewer-proposed repairs are welcome when feasible, but they are not self-authenticating. The original generating agent or a human must agree before those repairs are accepted.

Codex should still run deterministic verification before and after AI review.

## Human escalation

Escalate if:

- reviewer and Codex disagree on a safety issue
- reviewer flags confidential data risk
- reviewer identifies a design ambiguity
- the artifact is high-stakes
