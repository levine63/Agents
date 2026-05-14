# Contributing

## Principles

- make small reviewable changes
- preserve existing behavior unless intentionally changing it
- prefer deterministic checks before AI review
- update indexes when adding reusable assets

## Before large changes

- read `AGENTS.md`
- check `standards/INDEX.md`
- check `skills/INDEX.md`
- identify the relevant category and artifact type

## When adding reusable assets

For new standards, skills, templates, reviewer prompts, plug-ins, scripts, or workflows:

1. place the file in the appropriate directory
2. add it to the appropriate index
3. mark it as `active`, `integrated`, or `planned`
4. document source, purpose, and dependencies

## Safety

- do not commit secrets
- do not overwrite source material destructively
- do not expose credentials in examples or reports
