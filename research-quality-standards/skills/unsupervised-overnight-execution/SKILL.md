---
name: unsupervised-overnight-execution
description: Use when starting any unattended, long-running, or overnight session that may continue without user supervision, especially when multi-file edits, testing, promotion decisions, or destructive actions may occur.
---

# Unsupervised Overnight Execution

## Purpose

Use this skill for work that may continue for a long time without active human supervision.

The governing idea is:

- assume you will need to explain the entire session in the morning

Everything important should be:

- reconstructible
- reversible
- reviewable
- attributable to a session folder

## When to use

Use this skill when:

- the session may run overnight
- the user may be away for hours
- the work is long-running or multi-stage
- changes may touch multiple files
- promotion back into the source tree should depend on tests or smoke checks

Do not use it for trivial supervised edits.

## Safety model

Unattended execution should prefer containment over convenience.

The agent should not work directly in the source tree when a reasonable isolated workflow is available.

Preferred isolation order:

1. isolated git worktree
2. timestamped copied workspace
3. repo-local temp workspace
4. container or virtual-environment isolation layered on top when useful

If none of these can be established safely enough for the task, stop and leave a `NEEDS-HUMAN.md` note.

## Session setup

Before unattended execution begins:

1. create a timestamped session folder
2. record the task scope and intended editable files
3. establish the isolated working copy
4. define the verification plan
5. define any curfew or destructive-action restrictions

Preferred session-folder pattern:

- `tmp/overnight_sessions/YYYY-MM-DD_HHMM_topic/`

The session folder should contain at minimum:

- working notes or plan
- a session report
- a promotion decision summary
- a `NEEDS-HUMAN.md` file if the session halts without promotion

## Containment rules

### Work in the isolated copy

Perform edits inside the isolated workspace, not in the source tree.

Do not directly overwrite source files during the exploratory or implementation phase of unattended work.

### Copy only what is needed

Bring only the intended editable files and clearly related dependencies into the isolated workspace when possible.

This keeps the scope narrow and makes review easier.

### Preserve rollback

The original source tree is the rollback path.

If promotion later occurs, preserve the session folder long enough that a human can inspect:

- what changed
- what was tested
- what failed or remained uncertain

## Verification rules

Before promoting changes back:

- run the full available test suite when practical
- otherwise run the best available smoke checks
- if no checks exist, create the smallest reasonable smoke checks and run them

Do not silently skip verification.

If a check cannot run, record:

- what was attempted
- why it could not run
- what risk remains

## Promotion rules

Promote changes back to the source tree only when all of the following are true:

- the work stayed within the approved or inferred scope
- required tests or smoke checks passed
- no unresolved blocker makes the change misleading or unsafe
- the session report is complete enough for morning review

If those conditions are not met:

- do not promote changes
- leave the isolated session intact
- write `NEEDS-HUMAN.md`
- explain exactly what failed, what remains ambiguous, and what a human should decide next

## Destructive-action curfew

Do not begin destructive actions during unattended mode after the session's curfew unless they were explicitly pre-approved.

Destructive actions include:

- delete
- overwrite
- rename with loss of easy rollback
- bulk move
- cleanup that removes evidence

If no curfew policy is defined, treat unattended destructive actions as disallowed unless clearly necessary and pre-approved.

## Reporting requirements

Every unattended session should produce a session report.

Use:

- `templates/operations/overnight_session_report_template.md`

when possible.

The report should summarize:

- session purpose
- isolated workspace location
- intended source scope
- files changed
- checks run and results
- promotion decision
- unresolved risks
- items needing human review

If the session halts without promotion, use:

- `templates/operations/needs_human_template.md`

to leave a clean handoff note.

## Practical notes

- Prefer conservative promotion over optimistic promotion.
- Preserve evidence of failure; do not clean up the session folder just because the task did not complete.
- If interpretation of results changed materially, flag that for human review rather than silently rewriting conclusions.
- If true containment is impossible in the current environment, say so plainly and stop rather than pretending the safety model was satisfied.

## Bottom line

Unattended execution is allowed only when it remains:

- contained
- reviewable
- reversible

If the agent cannot keep those promises, it should stop and leave a human-readable handoff note.
