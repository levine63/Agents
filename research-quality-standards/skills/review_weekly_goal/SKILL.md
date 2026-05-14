---
name: review_weekly_goal
description: Use when reviewing weekly goals, weekly reports, or short-term work plans for clarity, visible deliverables, blocker honesty, parent-goal alignment, and one-week feasibility.
---

# Review Weekly Goal

## Purpose

Use this skill for weekly goals, weekly reports, and short-term progress artifacts.

The goal is to turn vague activity reporting into visible, reviewable progress with clear blockers and concrete next steps.

## When to use

Use this skill when:

- a weekly goal is being drafted
- a weekly report needs review
- the user wants to improve task clarity or detect hidden blockers
- an intern or RA update needs quick operational feedback

## Load

- `standards/genres/weekly_goals/standards.md`

Then choose the review prompt that matches the artifact:

- for goal-setting artifacts:
  - `standards/genres/weekly_goals/reviewer_prompt.md`
  - `reviewer_prompts/weekly_goal_review.md`
- for weekly report artifacts:
  - `reviewer_prompts/weekly_report_review.md`

Helpful templates:

- `templates/weekly_reports/weekly_goal_template.md`
- `templates/weekly_reports/weekly_report_template.md`
- `templates/weekly_reports/weekly_goal_training_memo.md`
- `templates/weekly_reports/gold_bad_blocked_examples.md`

## Deterministic checks first

Look first for obvious structural issues:

- missing parent goal
- missing artifact or evidence field
- vague verbs
- carried-over work with no explanation
- missing blocker details

If the artifact is a structured form export, use those fields directly rather than inferring them from prose.

## Review priorities

For weekly goals, prioritize:

- parent-goal alignment
- deliverable clarity
- definition of done
- first-step quality
- one-week feasibility

For weekly reports, prioritize:

- outputs versus activities
- evidence links or file references
- carryover honesty
- blocker specificity
- time and output plausibility

## Expected output

For goals, return the structure in `weekly_goal_review.md`.

For reports, return the structure in `weekly_report_review.md`.

## Bottom line

Prefer smaller concrete deliverables, explicit blockers, and visible artifacts over polished but vague updates.
