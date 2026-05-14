# Source Integration Map

## Purpose

This document records where the current integrated files came from.

## Sources

### `Codex/tools`

Integrated:

- `scripts/utilities/gemini_referee_review.py`

Not copied:

- `tools.env` because it may contain local secrets or environment-specific configuration

### `Codex/research_quality_standards`

Integrated:

- validation helpers under `scripts/validation/`
- workflow docs under `docs/workflows/`

Borrowed concepts:

- deployment policy
- experience logging
- verification and review flow

### `GitHub/Agents/research-quality-standards`

Integrated:

- review prompts under `reviewer_prompts/`
- genre standards for README, interview, statistical results, and academic paper
- format standards for Python and Stata
- templates for README, manuscripts, reports, interview notes, and statistical results
- lint scripts and tests
- GitHub Actions workflow examples

## Current interpretation

This repository is a consolidation scaffold, not yet a final curated release.

Some imported files are:

- directly reusable
- partly adapted
- placeholders for later normalization

Use the indexes to see whether something is `active`, `integrated`, or `planned`.
