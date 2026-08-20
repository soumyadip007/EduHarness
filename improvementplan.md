# EduHarness Improvement Plan

This document records the implementation of roadmap items **1–4** from the [Improvement Roadmap](docs/user-guide/improvement-roadmap.md), adapted to the current EduHarness architecture.

## Executive Summary

EduHarness moved from prototype stubs toward a configurable, database-backed platform:

| Roadmap Item | Status | Key Deliverables |
|--------------|--------|------------------|
| 1. Remove hardcoding | Implemented | Registry-driven models, DB escalation queue, dynamic sessions/students/KPIs |
| 2. Governance maturity | Implemented | Ownership, SLA fields, policy versioning/rollback, rationale requirements, teacher reply delivery |
| 3. Pedagogy quality | Implemented | Weighted mastery estimator, prerequisite-aware scaffolding, per-student progress plans |
| 4. Evaluation rigor | Implemented | Run manifests, bootstrap CIs, significance testing, model vs harness compare view, PDF reports |

---

## 1) Remove Hardcoding

### Model runtime
- **Before:** `gpt-4o-mini` hardcoded in `api/student/routes.py`.
- **After:** `eduharness/core/model_registry.py` loads `configs/models/model_registry.yaml`.
- **Configuration:**
  - Env: `ACTIVE_MODEL_KEY=mid_primary`
  - DB setting via `PUT /api/config/models/active`
  - Per-request override: `model_key` in `POST /api/student/message`
- **Frontend:** Model selector on the student workspace.

### Teacher queue and class data
- **Before:** In-memory `_queue_items` dict disconnected from real escalations.
- **After:** `EscalationRecord` table + `EscalationStore` shared by `SessionManager` and teacher API.
- **Students:** Derived from `learner_state` + `chat_session` tables.

### Sessions and metrics
- **Before:** Hardcoded demo sessions and KPI JSON.
- **After:** `ChatSession` / `ChatTurn` persistence; teacher summary KPIs computed from escalation records.

---

## 2) Governance Maturity

| Feature | Implementation |
|---------|----------------|
| Escalation ownership | `POST /api/teacher/queue/{id}/assign` sets `owner_id` |
| SLA tracking | `opened_at`, `resolved_at`, `response_time_ms` on `EscalationRecord` |
| Policy versioning | `PolicyVersion` table; `PUT /api/teacher/contract` saves version; `POST /api/teacher/contract/rollback` |
| Action rationale | Required for `rewrite`, `patch_rule`, `freeze_topic` |
| Teacher reply delivery | `TeacherReply` queue; delivered on next student turn |

---

## 3) Pedagogy Quality

### Mastery estimator
- Replaced binary keyword check with weighted multi-signal scoring in `eduharness/verify/mastery_check.py`.
- Signals include concept-specific vocabulary and code patterns.

### Concept dependency-aware scaffolding
- `decide_action()` in `contract_engine.py` reads prerequisite graph from `configs/concept_maps/python_intro.yaml`.
- Returns `hint_L1` with `prerequisite_gap:*` when prerequisites are unmet.

### Long-horizon progress plans
- `eduharness/pedagogy/progress_plan.py` generates dependency-ordered steps.
- Exposed at `GET /api/student/progress-plan` and shown on the student progress page.

---

## 4) Evaluation Rigor

| Feature | Endpoint / Artifact |
|---------|---------------------|
| Run manifests | `ExperimentManifest` table; written on `POST /api/researcher/experiments/run` |
| Confidence intervals | Bootstrap CIs in `evaluation/analysis/stats.py` |
| Significance testing | Welch t-test for H0 vs H3 |
| Model vs harness compare | `GET /api/researcher/results/compare` and `/results/stats` |
| PDF reports | `GET /api/teacher/reports/pdf`, `GET /api/researcher/reports/pdf` (includes model metadata) |

---

## Open-Source Model Recommendations

The registry supports multiple providers. Recommended open-source options:

| Registry Key | Model | Provider | Credential Required |
|--------------|-------|----------|---------------------|
| `llama_local` | Llama 3.2 | Ollama (local) | None — run `ollama pull llama3.2`; set `LOCAL_MODEL_BASE_URL` |
| `gemma_ollama` | Gemma 2 9B | Ollama (local) | None — run `ollama pull gemma2:9b` |
| `mistral_groq` | Llama 3.1 8B Instant | Groq | `GROQ_API_KEY` from [console.groq.com](https://console.groq.com) |
| `qwen_openrouter` | Qwen 2.5 7B Instruct | OpenRouter | `OPENROUTER_API_KEY` from [openrouter.ai](https://openrouter.ai) |

### Closed-source (reference / baseline)
| Registry Key | Credential |
|--------------|------------|
| `mid_primary` | `OPENAI_API_KEY` |
| `frontier_reference` | `OPENAI_API_KEY` |

### Suggested setup for OSS-first development

```bash
# Option A: Fully local (no API keys)
ollama pull llama3.2
export ACTIVE_MODEL_KEY=llama_local
export LOCAL_MODEL_BASE_URL=http://localhost:11434

# Option B: Hosted OSS via Groq (free tier available)
export GROQ_API_KEY=your_key
export ACTIVE_MODEL_KEY=mistral_groq

# Option C: OpenRouter (many OSS models, pay-per-use)
export OPENROUTER_API_KEY=your_key
export ACTIVE_MODEL_KEY=qwen_openrouter
```

Without any API keys or Ollama, the system falls back to a deterministic local stub response (useful for tests).

---

## Architecture Changes

```
Student UI ──► POST /api/student/message (model_key, mode)
                    │
                    ▼
              SessionManager
                    ├── ModelRegistry → LLMClient (OpenAI/Groq/Ollama/OpenRouter)
                    ├── EscalationStore (SQLite)
                    ├── SessionStore (SQLite)
                    ├── TeacherReplyStore (SQLite)
                    └── TraceLogger (JSONL + model metadata)

Teacher UI ──► EscalationStore / PolicyVersioning / PDF Report

Researcher UI ──► ExperimentManifest / stats / compare / PDF Report
```

### New database tables
- `escalation_record`, `chat_session`, `chat_turn`
- `policy_version`, `teacher_reply`, `progress_plan`
- `app_setting`, `experiment_manifest`

Run `python scripts/setup_db.py` to create tables on existing databases.

---

## API Additions

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/api/config/models` | List models + active key |
| PUT | `/api/config/models/active` | Set global active model |
| GET | `/api/student/progress-plan` | Dependency-aware learning plan |
| POST | `/api/teacher/queue/{id}/assign` | Assign escalation owner |
| GET | `/api/teacher/contract/versions` | List policy versions |
| GET | `/api/teacher/reports/pdf` | Teacher KPI PDF |
| GET | `/api/researcher/results/compare` | Model vs harness comparison |
| GET | `/api/researcher/results/stats` | CIs + significance |
| GET | `/api/researcher/reports/pdf` | Research PDF with model info |

---

## Remaining Work (Roadmap Items 5–6)

Not in scope for this sprint but noted for follow-up:

- **Item 5:** Auth/RBAC, error UX, charting filters, a11y
- **Item 6:** Postgres migration, background jobs, structured logging dashboards
- **Class/enrollment entities** remain future LMS work; student lists are derived from learner/session records

## Completed in Follow-up Sprint

The following partial gaps were closed:

- Teacher queue UI: rationale, rewrite text, assign owner
- Dynamic student session ID (localStorage) — no hardcoded demo session
- Teacher mastery heatmap from `/api/teacher/students/mastery-heatmap`
- Global model config on Researcher dashboard (`PUT /api/config/models/active`)
- Experiment form: multi-model × multi-harness matrix passed to Phase 6 runner via manifest
- Researcher results: bootstrap CIs, significance, live learning curve from API
- Exercise question selection from `course_content/exercises/` via `/api/student/questions`
- Trace latency/tokens populated from LLM call metadata

## API Keys Configuration

See **[docs/user-guide/api-keys.md](docs/user-guide/api-keys.md)** for where to set credentials.

Quick reference:

| What | Where |
|------|-------|
| API keys (secrets) | `.env` in project root (copy from `.env.example`) |
| Model profiles | `configs/models/model_registry.yaml` |
| Default model key | `ACTIVE_MODEL_KEY` in `.env` or Researcher UI |

---

## Verification

```bash
pip install -r requirements.txt
python scripts/setup_db.py
pytest tests/test_api_routes.py -q
```

Manual checks:
1. Student page — select a model, send a message, verify trace includes `model_key`.
2. Teacher queue — trigger H3 escalation, assign owner, resolve with rationale.
3. Teacher reports — download PDF; confirm model metadata section.
4. Researcher results — view compare card; download research PDF.

---

## Files Touched (Summary)

**Core:** `eduharness/core/model_registry.py`, `app_settings.py`, `session_store.py`  
**Governance:** `escalation_store.py`, `policy_versioning.py`, `teacher_reply_store.py`  
**Pedagogy:** `progress_plan.py`, `mastery_check.py`, `contract_engine.py`  
**Reports:** `eduharness/reports/pdf_report.py`  
**Evaluation:** `evaluation/analysis/stats.py`  
**API:** `api/services.py`, `api/config/routes.py`, updated student/teacher/researcher routes  
**Frontend:** student page, progress page, teacher reports, researcher results  
**Config:** `configs/models/model_registry.yaml`, `.env.example`
