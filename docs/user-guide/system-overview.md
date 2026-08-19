# System Overview

## What EduHarness is

EduHarness is a layered tutoring system built around one core idea:  
**Do not let an LLM tutor run ungoverned.**

The platform wraps an LLM tutor with pedagogical and safety controls:

- **H0**: Base agent only
- **H1**: Agent + verification gate
- **H2**: H1 + durable learner memory
- **H3**: H2 + teacher governance loop
- **H0+M / H0+G**: partial-factorial controls for research analysis

## Three dashboard roles

### Student Tutor
- Learner asks for help.
- Tutor responds with scaffolding.
- Student can run code snippets.
- Mastery is tracked over time.

### Teacher Governance
- Escalated high-risk interactions appear in queue.
- Teacher can approve, rewrite, or patch policy.
- Actions are logged for auditability.

### Research Console
- Run experiment pipelines.
- Compare harness conditions and metrics.
- View traces, costs, and result summaries.

## Core architecture

- **Frontend**: Next.js + React + Material UI dashboard
- **Backend**: FastAPI routes for student, teacher, researcher
- **Harness core**: session manager, verify layer, memory layer, governance layer
- **Storage**: SQLite (local), files/logs in `evaluation/data/results`
- **Evaluation**: scripted pipeline and metrics outputs

## Current state (important)

The project is a strong prototype and research scaffold.  
Some components are production-ready, while others still use placeholders/hardcoded defaults.  
See `Improvement Roadmap` for exact next steps to fully productionize.
