# Model Configuration (Single + Multi-Model)

## Current model registry

Model profiles are defined in:

- `configs/models/model_registry.yaml`

Example entries:

- `mid_primary`
- `frontier_reference`

Each profile includes:

- provider
- model_id
- temperature
- max_tokens

## Current behavior

Today, student API wiring still initializes a default model in code.  
The registry exists but is not yet fully runtime-driven for all routes.

## Recommended production configuration

## 1) Add active model key in environment

Use one env variable to choose runtime model:

```bash
export ACTIVE_MODEL_KEY=mid_primary
```

## 2) Load registry at backend startup

Create a config loader that:

- reads `model_registry.yaml`
- validates selected key
- builds `ModelConfig`
- injects configured `LLMClient` into `AgentExecutor`

## 3) Add optional per-request model override

For research APIs, allow payload:

- `model_keys: ["mid_primary", "frontier_reference"]`

Then run experiment matrix across model x harness conditions.

## 4) Log model metadata in traces

Each trace should include:

- model key
- model id
- provider

This is required for reproducible research.

## Multi-model strategy

## Student production path

- Stable default: `mid_primary`
- Optional role/tenant override in DB settings

## Research path

- Batch runs with multiple models
- Report harness gain per model
- Separate model improvement from harness improvement

## Guardrails

- Reject unknown model keys.
- Block provider call if key is missing and strict mode is enabled.
- Expose current active model via `GET /api/researcher/experiments/status` or dedicated config route.
