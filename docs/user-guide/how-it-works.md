# How It Works

## End-to-end tutoring turn

1. Student sends a message from `/student`.
2. Frontend calls `POST /api/student/message`.
3. Backend enters `SessionManager.handle_message(...)`.
4. Harness mode (`H0/H1/H2/H3/...`) toggles active layers.
5. Verification may classify intent and set policy action.
6. Agent executor calls model through `LLMClient`.
7. Output is post-checked against verification decision.
8. If risk is high and governance enabled, escalation is queued and fallback returned.
9. If memory enabled, learner state is updated.
10. Trace is logged for research/audit.

## Harness layers

### H0 (agent only)
- Direct tutoring response.

### H1 (verification)
- Intent classification.
- Adversarial scoring.
- Contract-driven action (allow/withhold/escalate/rewrite).

### H2 (memory)
- Persist concept-level mastery and scaffold history.
- Use prior learning state in future prompts.

### H3 (governance)
- Escalate risky turns for teacher review.
- Teacher action can approve/rewrite/patch policies.
- All actions logged.

## Model invocation flow

- `LLMClient` chooses provider by config (`openai`, `anthropic`, etc.).
- If API key is present, real remote call is used.
- If key is missing, deterministic fallback text is returned for local dev/test.

## Teacher governance flow

1. Escalation created (rule hit, risky score, or post-check fail).
2. Queue item visible in `/teacher`.
3. Teacher selects action.
4. Action is persisted to patch log and queue updates via websocket.
5. Policy or response behavior changes for future turns.

## Research flow

1. Researcher launches pipeline from `/researcher`.
2. Backend runs `evaluation/run_full_phase6.py`.
3. Result files are written under `evaluation/data/results`.
4. Result pages read those artifacts (TTI, table, cost, traces).
