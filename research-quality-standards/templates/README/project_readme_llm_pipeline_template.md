# Project Title

### Summary

State:

- what the pipeline does
- what decision or output it supports
- which steps are deterministic and which depend on an LLM

### Genre

`mixed_or_llm_pipeline`

### Quick Start

```bash
cp .env.example .env && python ./src/run_pipeline.py ./examples/minimal
```

**Expected output**

```text
Saved structured output to ./outputs/minimal/result.json
Evaluation summary written to ./outputs/minimal/eval.md
```

### Environment

- Python:
- Model provider:
- Model name:
- Lockfile:
- System dependencies:
- OS tested:

### Inputs

- Minimal example location:
- Prompt files:
- Upstream data source:
- Sensitive inputs:

### Deterministic Versus LLM Steps

- Deterministic:
- LLM-driven:

### Parameters

- temperature:
- max tokens:
- top_p:
- other important settings:

### Outputs

| Path | Meaning | Deterministic? |
| --- | --- | --- |
| `./outputs/...` | [What this file means] | [yes/no/partly] |

### Evaluation And Guardrails

- schema checks:
- automated tests:
- human review:
- red-team or adversarial checks:

### Failure Modes

- hallucination or unsupported claims:
- missing or partial extraction:
- format drift:
- model drift or upstream dependency drift:

### Cost And Timing

- minimal run token estimate:
- minimal run cost estimate:
- expected first-run time:
- expected later-run time:

### Not Included

- real secrets
- proprietary weights or private prompts, if excluded
- large raw inputs, if excluded

