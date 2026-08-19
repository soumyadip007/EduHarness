# Agentic Tutoring with a Pedagogical Harness

## EduHarness: A Pedagogical Harness for Verified Agentic Tutoring & Teacher Governance

**For:** Instructor review - final topic direction  
**Date:** August 2026  
**Status:** Draft proposal

---

## 1. Working Title

**Agentic Tutoring with a Pedagogical Harness: Verification, Durable Memory, and Teacher Governance for Trustworthy Multi-Session Tutoring**

Short versions:
- **Slides:** *Agentic Tutor, Pedagogical Harness*
- **Tagline:** *Verify, Remember, Govern*

---

## 2. How This Topic Is Positioned

Most papers today sit in one of two camps:

- **Agentic tutoring** - an LLM agent that plans, uses tools, and tutors over time (EduClaw, SocraticLM, many LMS agents).
- **Harness / safety work** - runtime layers that control what the model is allowed to do (SHAPE, general harness engineering).

This proposal does **both**, with a clear split of roles:

| Layer | Role in this work | What we claim |
|-------|-------------------|---------------|
| **Agentic tutor** | The *executor* - observes the student, chooses tutoring actions, uses retrieval/tools, runs over days | Implementation + evaluation target (learning gain, curriculum behavior) |
| **Pedagogical harness** | The *research object* - verifies actions, stores learner state, routes teacher control | Main contribution - architecture, ablation, governance protocol |

**One-line pitch:**

> I build an **agentic tutor** that operates over weeks in a course-like setting, but the **scientific contribution** is the **pedagogical harness** around it - verification under adversarial prompting, durable learner memory, and a teacher governance protocol - evaluated with model x harness ablations on benchmarks in the SHAPE / EduClaw / LongTutor line.

This keeps the work inside **agentic AI in education** (agent behavior, multi-session tutoring, LMS-style interaction) while avoiding the trap of "yet another chatbot tutor" with no systems story.

### 2.1 Original work framing (how to read this proposal)

**EduHarness is a fresh system design**, not a replication or extension of any single publisher paper.

| What we do | What we do **not** do |
|------------|------------------------|
| Propose a **new integrated pedagogical harness** (Verify + Remember + Govern) with H0–H3 ablation | Re-implement DBagent, SageJavon, PyTutor, AGL, or STAP |
| Use a **minimal agentic executor** (one tutor + course retrieval + programming tools) as the evaluation vehicle | Claim novelty on ReAct, RAG, hint ladders, or KT as standalone contributions |
| Cite IEEE/ACM/Springer/Elsevier work in **Section 8.6** to justify the gap and scope | Copy their architectures, metrics-only papers as our design spec |
| Evaluate on SHAPE / EduClaw / LongTutor benchmarks where comparable | Present our work as "X + Y from paper Z stitched together" |

**How to present it:** *"We introduce EduHarness — a pedagogical harness for trustworthy multi-session agentic tutoring. Prior work addresses verification, memory, or governance in isolation; we unify them in one ablatable runtime with teacher-executive control. The agent executor is intentionally standard; the harness is the contribution."*

Publisher literature stays in the document **for thesis related-work and supervisor review only**. Design sections (4, 6, 7) describe **our** architecture in our terms.

---

## 3. Problem Statement

Agentic tutors are being deployed as autonomous helpers - they plan steps, call tools, and interact with students over many sessions. EduClaw-Bench shows this can work in principle, but also that **most agent+harness combinations plateau early** and often fail on curriculum structure and learning gain, not just answer leakage.

At the same time, SHAPE shows that even strong models break **pedagogical safety** under adversarial prompting at the turn level. LongTutor shows models can read history but struggle to **diagnose state and teach from it**.

So the open problem is not only "build a smarter agent." It is:

**How do you wrap an agentic tutor in a harness that stays trustworthy across many sessions — under adversarial students, with durable learner state, and with teachers who can actually govern it?**

Three failures keep appearing together:

1. **The agent bypasses pedagogy** when students push for direct answers (SHAPE line).
2. **The agent forgets the learner** when sessions stack up and context is compressed (LongTutor / multi-session memory line).
3. **Teachers cannot govern the agent** in a structured, auditable way (institutional adoption gap).

This proposal treats them as one integrated design problem: **agent + pedagogical harness + environment**.

---

## 4. Core Features

The system has three interdependent layers that wrap around a single agentic tutor. Each addresses a specific failure mode seen in the literature.

### Feature 1: Pedagogical Verification Gate (Verify)

- **What it does:** Before every tutor response, the harness checks the student's inferred mastery against the pedagogical contract and decides: scaffold, hint, withhold, or allow a fuller explanation.
- **Tiered scaffolding policy:** For programming tasks, the contract enforces **minimum-necessary support** — e.g. pseudocode → cloze → conceptual hint → minimal code scaffold → fuller explanation only when mastery and assessment mode allow. Reduces answer leakage without blanket refusal.
- **Adversarial handling:** Detects answer-inducing patterns (refusal suppression, role play, rephrasing) and enforces policy even when the student tries to bypass it.
- **Pre-delivery verification pass (H1):** Optional harness check on draft responses before the student sees them — grounding, leakage, and policy compliance; refuse or rewrite when the gate is uncertain.
- **Tied to assessment mode:** Behavior changes depending on whether the student is in practice, homework, or exam mode.
- **Extends SHAPE:** SHAPE does this at the turn level; we keep it running across sessions, tied to durable state.

### Feature 2: Durable Learner Memory (Remember)

- **What it does:** Maintains a persistent, structured record of the student across sessions - mastery levels, misconceptions, scaffolding history, and teacher overrides.
- **Harness-owned state (not chat log):** Long-term learner state lives in the **harness store**, with provenance and compaction rules — not in the agent's context window or raw chat history. Optional LMS/quiz signals can update mastery when available.
- **Course concept map:** Teacher-authored prerequisite graph per course scopes what mastery means and what the verification gate checks.
- **Not just a long context window:** Memory is explicit state estimation with write/read/compact/recover policies. Compaction must not delete constraints or teacher corrections.
- **Drift detection:** If inferred mastery diverges from observed behavior, the harness flags it and can trigger a re-assessment or teacher escalation.
- **Extends LongTutor:** LongTutor shows models fail to use history for diagnosis. We give the agent structured state instead of raw log retrieval.

### Feature 3: Teacher Governance Protocol (Govern)

- **What it does:** Gives teachers a concrete escalation path - when to intervene, what evidence they see, what actions they can take, and how corrections feed back into harness policy.
- **Executive governance:** Teacher-approved **policy patches** update verification rules, memory policies, and escalation thresholds at runtime — governance is binding, not optional advice to the agent.
- **Declarative teacher contracts:** Teachers express rules in structured YAML / natural language (scaffold strictness, exam-mode rules, hint caps) loaded per course — not hardcoded application logic.
- **Escalation contract:** Trigger (why the harness cannot safely continue), evidence packet (dialogue, mastery, rule fired), allowed actions (approve, rewrite, freeze topic, patch rule), latency budget (safe fallback for the student while waiting).
- **Policy patch log + immutable audit:** Every governance action is logged; teacher corrections become durable harness updates, not one-off chat edits.
- **Graceful degradation:** If teacher is unavailable, harness falls back to strict verify-only mode rather than ungoverned answers.
- **Scope v1:** Teacher-primary governance; multi-stakeholder negotiation (parents, regulators) is **future work**, not v1 scope.
- **Not in SHAPE or EduClaw:** Neither paper has an explicit teacher governance layer.

### How the three features depend on each other

- Verification without memory fails after a few sessions (the gate forgets what was already scaffolded).
- Memory without teacher governance is hard for institutions to adopt (no accountability).
- Teacher governance without verification has nothing to escalate against (no policy contract).

All three share one learner-state store and one audit trail.

---

## 5. Abstract

### 5.1 Revised abstract (innovation-led, for submission)

Agentic LLM tutors can plan, use tools, and interact with learners over days or weeks, but their trustworthiness breaks down along three axes that current work treats separately: pedagogical safety collapses under adversarial prompting, learner state is lost as sessions accumulate, and teachers have no structured way to govern agent behavior at runtime. We introduce a **unified pedagogical harness** - an education-native runtime layer wrapped around a single agentic tutor - that addresses all three failures in one integrated system. The harness contributes three novel, interdependent components: (1) a **mastery-aware verification gate** that enforces pedagogical contracts across assessment modes and resists answer-inducing attacks not just at the turn level but over sustained multi-session interaction; (2) a **durable learner-state store** with explicit write, compact, and drift-recovery policies that preserves misconceptions, scaffolding commitments, and teacher overrides beyond context-window boundaries; and (3) a **teacher governance protocol** with structured escalation triggers, evidence packets, policy patches, and rollback - operationalizing institutional oversight as a measurable runtime service rather than an aspirational principle. A key design choice is that these layers share one state and one audit trail, so verification can read durable memory, governance can patch verification rules, and every decision is traceable to a specific harness layer. We evaluate the system using an **ablation ladder** (H0: prompt-only agent, H1: +verification, H2: +memory, H3: +governance) crossed with multiple model tiers, reporting adversarial safety, long-horizon learning gain, history-aware teaching quality, policy compliance, state divergence, teacher intervention burden, and layer-level failure attribution. The expected contribution is not a better chatbot but a **reference architecture and empirical protocol** showing which harness layers are necessary - and in what combination - for trustworthy, semester-scale agentic tutoring in higher education.

### 5.2 Original abstract (reference copy)

Educational systems increasingly use **agentic LLM tutors** - models that plan tutoring actions, use tools, and interact with learners over days or weeks. Recent benchmarks show that tutoring quality depends on both the base model and the surrounding runtime, yet existing work typically addresses **pedagogical safety** (SHAPE), **extended tutoring evaluation** (EduClaw-Bench), or **historical diagnosis and teaching** (LongTutor) in isolation. This research proposes an agentic tutoring system whose primary contribution is a **pedagogical harness** integrating (1) **runtime verification** under adversarial prompting, (2) **durable learner memory** that preserves mastery, misconceptions, and instructional commitments across sessions, and (3) **teacher-in-the-loop governance** with escalation triggers, evidence packets, and policy patches that update harness behavior without retraining the model. The agent executes tutoring; the harness makes that execution trustworthy and deployable. Evaluation follows a **model x harness** design with ablation levels H0-H3, reusing metrics from SHAPE, EduClaw-Bench, and LongTutor where possible, and adding harness-specific measures (policy compliance, state divergence, teacher intervention burden, layer attribution). Expected outputs are a reference architecture, ablation protocol, and auditable traces for semester-scale agentic tutoring in higher education.

---

## 6. Research Scope

### 6.1 In scope

| Area | What we build / study |
|------|------------------------|
| **Agentic tutor core** | Single tutoring agent: observe -> plan tutoring action -> generate (with retrieval/tools) -> act in a course-like loop over multiple sessions/days |
| **Pedagogical harness** | Verification gate, learner-state store, teacher governance plane, audit traces |
| **Pedagogical contract** | Checkable rules: scaffold vs hint vs solution; assessment mode; escalation triggers |
| **Multi-session interaction** | Multi-session or multi-day evaluation (benchmark sim or pilot module) |
| **Adversarial robustness** | Answer-inducing and adversarial student prompts (SHAPE-style) |
| **Teacher protocol** | Escalation, evidence packet, approve/rewrite/patch, policy write-back |
| **Ablation study** | H0 (prompt-only agent) -> H1 (+verify) -> H2 (+memory) -> H3 (+governance) |
| **Evaluation** | SHAPE metrics + EduClaw-style extended tutoring axes + LongTutor-style history tasks + harness-only metrics |
| **Domain** | **Undergraduate programming (Python)** — one course module for evaluation; confirm with supervisor |

### 6.2 Out of scope

| Not in scope | Why |
|--------------|-----|
| New foundation model or large fine-tune | Contribution is system design, not model weights |
| Multi-agent classroom orchestration | One tutor + harness; multi-agent is future work |
| Full LMS product / replacement | LMS is optional environment hook, not the research object |
| Generic software-agent harness | Harness is **education-native** (mastery, scaffolding, assessment integrity) |
| Claim that AI replaces teachers | Harness is designed so teachers retain control |

### 6.3 Research questions

**Main question:**  
Does an agentic tutor wrapped in a pedagogical harness (verify + remember + govern) sustain trustworthy tutoring quality across many sessions better than the same agent with prompt-only or partial harness support?

**Sub-questions:**

1. Under adversarial prompting, how much does the verification layer improve Safety and Helpfulness vs the bare agent (H0 vs H1)?
2. Over multi-week tutoring, how much does durable memory reduce state divergence and improve history-aware teaching (H1 vs H2)?
3. Does teacher governance reduce failure recovery cost without unacceptable workload (H2 vs H3)?
4. Do harness benefits depend on model tier (model x harness interaction, following EduClaw)?
5. Can traces attribute failures to agent reasoning vs memory vs verification vs governance?

### 6.4 Scope verification audit (August 2026)

This subsection checks whether the declared scope (Sections 6.1-6.2) is **internally consistent** and **defensible against recent IEEE / ACM / Springer / Elsevier literature** (Section 8.6).

| Scope element | Status | Notes |
|---------------|--------|-------|
| Single agentic tutor + harness (not multi-agent classroom) | **In scope** | One tutor + harness; multi-agent overlays cited only in Section 8.6 |
| Verify + Remember + Govern as one ablatable harness | **Core contribution** | Original integrated design; publisher papers cover axes separately (Section 8.6) |
| Multi-session / multi-day evaluation | **In scope** | EduClaw-style horizon + harness-specific stress tests |
| Adversarial prompting (SHAPE-style) | **In scope** | Our eval protocol; not a replication of any single publisher tutor |
| Teacher governance protocol | **Core contribution** | Original executive protocol; related work cited for gap only (Section 8.6) |
| One domain (programming) | **Set → Python** | Single course module for controlled evaluation; math deferred to future work |
| Classroom pilot | **Optional — OK** | Benchmark-first (EduClaw / SHAPE / LongTutor); classroom study only if supervisor approves |
| Dynamic teacher profiles | **Partially documented** | Teacher-specific contracts described in companion notes; should be folded into H3 evaluation (Experiment E5) |
| Out of scope: new foundation model | **Aligned** | Consistent with harness-engineering and ITS literature |
| Out of scope: full LMS product | **Aligned** | LMS is environment hook only |

**Scope risks to manage in writing:**

1. **"Just engineering"** — mitigate with H0-H3 factorial design and borrowed metrics (Section 10).
2. **Overlap with verification-only papers** (Section 8.6) — emphasize **integrated multi-session harness + teacher patches**, not another hint-tier tutor.
3. **Overlap with governance-only papers** (Section 8.6) — emphasize **executive runtime protocol + verification gate**, not replication of advisory or orchestration UIs.
4. **Domain ambiguity** — resolve with supervisor before Phase 2 build.

**Verdict:** Research scope is **coherent and publishable** provided (a) one domain is locked, and (b) the contribution is framed as an **integrated, ablatable pedagogical harness** rather than a new tutor model.

---

## 7. Complete Workflow and Technical Plan

### 7.1 End-to-end workflow (what happens in one tutoring turn)

```text
  STUDENT                    HARNESS                         AGENT / LLM
    |                           |                                |
    |-- message --------------->|                                |
    |                           |                                |
    |                     1. Load learner state                  |
    |                        (mastery, misconceptions,           |
    |                         scaffolding history,               |
    |                         teacher overrides)                 |
    |                           |                                |
    |                     2. Load pedagogical contract            |
    |                        (assessment mode, scaffold rules,   |
    |                         escalation triggers)               |
    |                           |                                |
    |                     3. Classify student intent              |
    |                        help-seeking | answer-inducing |    |
    |                        off-topic | exam-sensitive           |
    |                           |                                |
    |                     4. Estimate mastery / prerequisites     |
    |                           |                                |
    |                     5. VERIFICATION DECISION               |
    |                        scaffold | hint | withhold |        |
    |                        escalate-to-teacher |               |
    |                        allow-fuller-explanation             |
    |                           |                                |
    |                     6. If allowed:                          |
    |                           |--- prompt + constraints ------>|
    |                           |                                |
    |                           |<-- draft response ------------|
    |                           |                                |
    |                     7. Post-check                           |
    |                        policy compliance,                  |
    |                        grounding, safety                   |
    |                           |                                |
    |                     8. Update memory                        |
    |                        (what was taught, withheld,          |
    |                         new mastery evidence)              |
    |                           |                                |
    |                     9. If uncertain or high-stakes:         |
    |                        queue teacher review                |
    |                        (evidence packet)                   |
    |                           |                                |
    |                    10. Log trace                            |
    |                        (action, state, decision,           |
    |                         layer, outcome)                    |
    |                           |                                |
    |<-- final response --------|                                |
```

### 7.2 System architecture (technical)

```text
+------------------------------------------------------------------+
|                     STUDENT INTERFACE                             |
|  Web UI / chat / LMS embed                                       |
+------------------------------------------------------------------+
         |                                          ^
         v                                          |
+------------------------------------------------------------------+
|                    SESSION MANAGER                                |
|  Receives student message, loads context, returns response       |
+------------------------------------------------------------------+
         |                                          ^
         v                                          |
+------------------------------------------------------------------+
|                   PEDAGOGICAL HARNESS                            |
|                                                                  |
|  +------------------+  +------------------+  +----------------+  |
|  | VERIFICATION     |  | LEARNER-STATE    |  | TEACHER        |  |
|  | GATE             |  | STORE            |  | GOVERNANCE     |  |
|  |                  |  |                  |  | PLANE          |  |
|  | - Intent classif.|  | - Mastery model  |  | - Escalation   |  |
|  | - Mastery check  |  | - Misconceptions |  |   queue        |  |
|  | - Contract eval  |  | - Scaffolding    |  | - Evidence     |  |
|  | - Adversarial    |  |   history        |  |   packets      |  |
|  |   detection      |  | - Teacher        |  | - Policy patch |  |
|  | - Action routing |  |   overrides      |  |   log          |  |
|  |                  |  | - Provenance     |  | - Approval     |  |
|  +------------------+  +------------------+  |   queue        |  |
|                                              +----------------+  |
|  +------------------+  +------------------+                      |
|  | PEDAGOGICAL      |  | AUDIT / TRACE    |                      |
|  | CONTRACT STORE   |  | ENGINE           |                      |
|  |                  |  |                  |                      |
|  | - Scaffold rules |  | - Per-turn trace |                      |
|  | - Assessment     |  | - Layer label    |                      |
|  |   modes          |  | - Failure attrib.|                      |
|  | - Escalation     |  | - Episode pack.  |                      |
|  |   triggers       |  |                  |                      |
|  +------------------+  +------------------+                      |
+------------------------------------------------------------------+
         |                                          ^
         v                                          |
+------------------------------------------------------------------+
|                    AGENTIC TUTOR (EXECUTOR)                       |
|                                                                  |
|  Standard agent loop: observe -> plan -> act -> respond          |
|  Course retrieval + code tools (executor only — not the claim)   |
|  Reads harness state each turn; does not own long-term memory    |
|                                                                  |
|  Uses: LLM API, course content retrieval, code run / lint tools  |
+------------------------------------------------------------------+
         |
         v
+------------------------------------------------------------------+
|                    FOUNDATION MODEL(S)                            |
|  GPT-4o / Claude / open-source (locked per experiment)           |
+------------------------------------------------------------------+

EXTERNAL:
+---------------------+   +---------------------+
| TEACHER DASHBOARD   |   | LMS (optional)      |
| - Review queue      |   | - Roster            |
| - Evidence viewer   |   | - Course content    |
| - Patch editor      |   | - Assessment mode   |
| - Audit trail       |   | - Grades (optional) |
+---------------------+   +---------------------+
```

### 7.3 Data stores

| Store | Technology (suggested) | Holds | Read by | Written by |
|-------|------------------------|-------|---------|------------|
| Learner-state DB | PostgreSQL or SQLite | Mastery, misconceptions, scaffolding log, teacher overrides, provenance | Verification gate, agent, teacher dashboard | Session manager (after each turn), teacher (via patch) |
| Contract store | JSON/YAML files or DB table | Scaffold rules, assessment modes, escalation triggers, retention policy | Verification gate | Teacher (via patch editor), researcher (initial config) |
| Trace store | Append-only log (JSONL or DB) | Per-turn: student input, intent class, mastery snapshot, verification decision, agent output, post-check result, layer label | Audit engine, teacher dashboard, evaluation scripts | Session manager (after each turn) |
| Teacher queue | Task queue (Redis / DB table) | Pending escalations with evidence packets | Teacher dashboard | Verification gate (on escalation trigger) |

### 7.4 Technical plan by phase

#### Phase 1: Foundation (Months 1-2)

**Goal:** Understand the landscape, fix design decisions.

| Task | Output |
|------|--------|
| Read SHAPE, EduClaw-Bench, LongTutor, Zhong & Zhu | Annotated gap table |
| Confirm domain (Python programming module) with supervisor | Domain locked |
| Define pedagogical contract schema (JSON/YAML) | Contract v0.1 |
| Define learner-state schema (DB tables) | Schema v0.1 |
| Define escalation contract (trigger, evidence, actions) | Protocol v0.1 |
| Define trace schema (what is logged per turn) | Trace spec v0.1 |
| Set up repo, dev environment, LLM API access | Working repo |

#### Phase 2: H0 - Bare Agent (Month 3)

**Goal:** Build the agentic tutor with no harness, as the baseline.

| Task | Output |
|------|--------|
| Build session manager (receives student message, returns response) | Working chat loop |
| Build agentic tutor core: observe -> plan -> tools/retrieval -> generate | Agent that can tutor in chosen domain |
| System prompt with basic pedagogical instructions (no runtime enforcement) | H0 baseline |
| Collect 30-50 adversarial / answer-inducing student prompts | Adversarial test set v0.1 |
| Run H0 on adversarial set, record Safety / Helpfulness / Pedagogy | H0 baseline numbers |

#### Phase 3: H1 - Verification Gate (Months 4-5)

**Goal:** Add runtime pedagogical verification.

| Task | Output |
|------|--------|
| Build intent classifier (help-seeking vs answer-inducing vs off-topic vs exam-sensitive) | Classifier (LLM-based or rule-based) |
| Build mastery estimator (reads learner-state, checks prerequisites) | Mastery check module |
| Build verification router (scaffold / hint / withhold / escalate / allow) | Verification gate v1 |
| Integrate contract store (rules loaded per session) | Contract-driven routing |
| Build post-check (does agent output match contract decision?) | Output filter |
| Run H0 vs H1 on adversarial set | Safety / Helpfulness / Pedagogy comparison table |

#### Phase 4: H2 - Durable Memory (Months 5-7)

**Goal:** Add persistent learner state across sessions.

| Task | Output |
|------|--------|
| Implement learner-state DB (mastery, misconceptions, scaffolding history, overrides) | Working DB + read/write API |
| Build memory write policy (what gets stored after each turn) | Write rules |
| Build memory read policy (what the agent sees at start of each session) | State injection |
| Build compaction policy (how old sessions are summarized without losing constraints) | Compaction rules |
| Build drift detection (flag when inferred mastery diverges from observed behavior) | Drift alert |
| Run multi-session test (7-14 sessions): H0 vs H1 vs H2 | State divergence, contradiction rate, History Utilization |
| Run LongTutor-style offline tasks: H0 vs H2 | MR accuracy, Macro-F1 |

#### Phase 5: H3 - Teacher Governance (Months 7-9)

**Goal:** Add teacher escalation, evidence, and policy patches.

| Task | Output |
|------|--------|
| Build teacher queue (escalation triggers push to queue with evidence packet) | Working queue |
| Build teacher dashboard (review queue, evidence viewer, action buttons) | Simple web UI |
| Implement policy patch flow (teacher correction -> contract/memory update -> harness behavior change) | Patch pipeline |
| Build patch log (what was changed, by whom, when) | Audit trail for governance |
| Measure patch latency (time from teacher correction to behavior change) | Latency metric |
| Run H2 vs H3 comparison on multi-session test | Teacher intervention rate, workload survey |

#### Phase 6: Full Evaluation (Months 9-12)

**Goal:** H0-H3 ablations on all benchmarks.

| Task | Output |
|------|--------|
| Adversarial stress test (SHAPE-style): H0-H3 | Safety / Helpfulness / Pedagogy tables |
| Multi-day sim (EduClaw-style, 14-30 days): H0 vs H2 vs H3 | Delta Solve, Gagne, Rosenshine, plateau day |
| LongTutor-style offline tasks: H0 vs H2 | MR, F1, History Utilization |
| Model x harness factorial (2 model tiers x 4 harness levels) | Interaction plot |
| Compute harness-only metrics: policy compliance, state divergence, drift recovery, layer attribution | Full metric suite |
| Build composite Trustworthy Tutoring Index (TTI) | Headline number |

#### Phase 7: Pilot (Months 10-14, if classroom access)

**Goal:** Small real-world test.

| Task | Output |
|------|--------|
| Pick one course module + get ethics approval | IRB / ethics clearance |
| Deploy H2 and H3 for two groups (or within-subjects) | Live system |
| Collect: teacher workload survey, student feedback, 3-5 traced case studies | Qualitative + quantitative pilot data |
| If no classroom access: run simulation-only and document as limitation | Sim-only results |

#### Phase 8: Writing (Months 15-18)

**Goal:** Paper / thesis.

| Section | Content |
|---------|---------|
| Introduction | Three failures + harness as the answer |
| Related work | SHAPE, EduClaw, LongTutor, harness engineering + gaps |
| Architecture | Agent + harness diagram, contract schema, memory design, teacher protocol |
| Experiments | H0-H3 ablations, model x harness factorial |
| Results | Ablation table, learning curve, adversarial table, governance case study |
| Discussion | Which layer matters most, model dependence, practical adoption |
| Limitations | Domain scope, simulated vs real students, teacher sample size |

### 7.5 Ablation ladder (H0-H3)

Same agentic tutor core; harness layers added step by step:

| Level | Agent | Harness enabled | What we test |
|-------|-------|-----------------|--------------|
| **H0** | Yes | None (prompt-only guardrails) | Baseline agentic tutor |
| **H1** | Yes | + Verification gate | Pedagogical enforcement |
| **H2** | Yes | + Durable learner memory | Cross-session consistency |
| **H3** | Yes | + Teacher governance + full audit | Deployable full system |

### 7.6 Suggested tech stack

| Component | Options |
|-----------|---------|
| LLM API | OpenAI / Anthropic / open-source (Llama, Qwen) - lock model ID per experiment |
| Agent executor | Simple observe-plan-act loop; course retrieval + code tools (minimal, fixed across H0–H3) |
| Orchestrator | LangGraph / custom Python graph / simple state machine |
| Learner-state DB | PostgreSQL (production) or SQLite (prototype) — **harness-owned**, not agent chat log |
| Mastery updates | Harness write rules from dialogue + optional LMS grade hooks |
| Concept map | YAML/JSON prerequisite graph per course (teacher-authored) |
| Contract store | YAML files (v1), DB table (v2); per-teacher policy fields |
| Trace store | JSONL files (v1), ClickHouse or PostgreSQL (v2) |
| Teacher dashboard | Streamlit or simple Flask/React app |
| Student UI | Streamlit chat or simple web UI |
| Deployment | Docker compose (local dev), cloud VM (pilot) |

---

## 8. Comparison with Existing Work

This work sits **between** agentic tutoring papers and harness/safety papers. Below: anchor comparisons (SHAPE / EduClaw / LongTutor), **strict publisher literature** (Section 8.6), and where EduHarness differs.

### 8.1 Summary table

| Work | What they contribute | Agentic? | Harness? | Long horizon? | Teacher govern? | Gap this work fills |
|------|----------------------|----------|----------|---------------|-----------------|---------------------|
| **SHAPE** | Safety, Helpfulness, Pedagogy under adversarial prompts; gating pipeline | No (turn-level) | Yes (verification) | No | No | Extend verification into **multi-session memory + teacher protocol** |
| **EduClaw-Bench** | 30-day agent tutoring benchmark; model x harness matters; plateau / no-curriculum failures | Yes | Yes (adapters) | Yes | No | Prescribe **education-native harness** (verify+memory+govern), not just compare adapters |
| **LongTutor** | Evidence -> Diagnosis -> Teaching on real logs | Eval only | No | Logs, not live agent loop | No | **Live agent + durable state store** that feeds diagnosis and teaching |
| **SocraticLM** | Strong pedagogical dialogue via model | Partial | Prompt/style | Limited | No | **Runtime enforcement + memory + governance**, not style-only |
| **Zhong & Zhu (Harness Eng.)** | General model-harness-environment formalism | General agents | Yes | N/A | Partial | **Education-native** harness (mastery, scaffolding, assessment) |
| **TEAS** | Trust / audit framing for educational AI | N/A | Standards | N/A | Conceptual | **Concrete runtime protocol** and measurable teacher burden |
| **Chu et al. (LLM Agents for Ed.)** | Landscape of educational agents | Yes | Varied | Varied | Varied | **Unified eval + ablatable harness** for one agentic tutor |

### 8.2 SHAPE - verification line

**Paper:** SHAPE: Unifying Safety, Helpfulness and Pedagogy for Educational LLMs  
**URL:** https://arxiv.org/abs/2604.22134

SHAPE formalizes three metrics tied to a knowledge-mastery graph and tests them under adversarial prompting (refusal suppression, role play). Their graph-augmented pipeline improves worst-case safety dramatically on many models.

| Their metrics | Meaning |
|---------------|---------|
| Safety | Withholds solution when prerequisites not mastered |
| Helpfulness | Gives solution when mastery is complete |
| Pedagogy | Safe responses target missing concepts |

**Where we differ:** SHAPE is the **verification anchor**. We use the same stress test (H0 vs H1) but ask: *does safety still hold on day 14 of an agentic tutor, after memory compaction, and when a teacher can patch policy?* SHAPE does not study that.

**What we reuse:** Safety / Helpfulness / Pedagogy tables under default vs adversarial prompts.  
**What we add:** Multi-session agent loop + memory layer + teacher escalation when the gate is uncertain.

---

### 8.3 EduClaw-Bench — extended agentic tutoring evaluation

**Paper:** EduClaw-Bench: A Long-Horizon Benchmark for Pedagogical LLM Agents with Simulated Learners  
**URL:** https://arxiv.org/abs/2608.03206

EduClaw evaluates **agent tutors + harness adapters** over **30 virtual days** through an LMS API, with a KT-grounded simulated learner. Key findings:

- Tutoring quality = **model + harness together**; rankings reorder across tiers.
- Most runs **plateau by day 5-10**.
- Top failures: **no curriculum (~48.5%)**, **no learning gain (~53.3%)** - not just answer leakage.
- Metrics span learning gain, responsiveness, helpfulness (LearnLM), Gagne, Rosenshine.

| Axis | Metric |
|------|--------|
| I | Delta Solve Rate |
| II | Responsiveness |
| III | Helpfulness (LearnLM rubric) |
| IV | Gagne, Rosenshine |
| Safety aux. | Answer-holding / hand-over |

**Where we differ:** EduClaw is the **agentic evaluation anchor**. We participate in the same question ("what makes sustained agentic tutoring work over weeks?") but contribute a **specified harness architecture** rather than another adapter in their grid.

**What we reuse:** Delta Solve, helpfulness, curriculum rubrics, plateau day, model x harness factorial.  
**What we add:** Verification contract + durable learner-state store + teacher governance with measurable intervention burden.

**Realistic win condition vs EduClaw baselines:** Later plateau, fewer no-curriculum runs, or higher post-plateau gain - attributed to memory + governance, not just a stronger base model.

---

### 8.4 LongTutor - history, diagnosis, teaching line

**Paper:** LongTutor: Benchmarking LLMs for Long-term Personalized Tutoring  
**URL:** https://aclanthology.org/2026.acl-long.1371.pdf

LongTutor benchmarks three tasks on expert-annotated logs:

1. **Evidence acquisition** - pull facts from history (models strong here).
2. **State diagnosis** - classify knowledge gaps (models weak; best Macro-F1 ~40%).
3. **Teaching action** - history-aware tutoring moves (History Utilization often below 2/5).

**Where we differ:** LongTutor shows **what the agent should use history for**. We provide a **harness-maintained learner model** that the agentic tutor reads and updates - not raw log retrieval alone.

**What we reuse:** MR accuracy, Macro-F1, History Utilization judge scores (offline eval on golden tasks).  
**What we add:** Live agent loop where memory is **written and repaired** over sessions; link memory quality to teaching scores.

---

### 8.5 Other related work

| Paper | URL | Role in comparison |
|-------|-----|-------------------|
| SocraticLM (NeurIPS 2024) | https://proceedings.neurips.cc/paper_files/paper/2024/hash/9bae399d1f34b8650351c1bd3692aeae-Abstract-Conference.html | Strong **agentic dialogue** baseline; lacks runtime harness ablation |
| Zhong & Zhu, AI Harness Engineering | https://arxiv.org/abs/2605.13357 | Theoretical frame for **model-harness-environment**; we instantiate it for education |
| TEAS | https://arxiv.org/abs/2601.06066 | Trust/audit standards; we operationalize teacher oversight |
| Chu et al., LLM Agents for Education | https://aclanthology.org/2025.findings-emnlp.743/ | Positions agentic tutors in ed; we narrow to **trustworthy multi-session harness** |
| Scoping Review of LLM Pedagogical Agents | https://arxiv.org/abs/2604.12253 | Gap justification - verification, memory, governance rarely integrated |

### 8.6 Strict publisher literature review (IEEE / ACM / Springer / Elsevier)

> **Reference only.** This subsection supports thesis *Related Work* and gap justification. **EduHarness does not replicate these systems.** Design choices in Sections 4, 6, and 7 are original to this proposal unless explicitly cited as an evaluation benchmark (SHAPE, EduClaw, LongTutor).

The anchor papers in Sections 8.2-8.4 (SHAPE, EduClaw-Bench, LongTutor) sit on **ACL / arXiv** and define our **evaluation lineage**. This subsection adds a **strict publisher filter** — only venues from **IEEE, ACM, Springer, and Elsevier** — to show what peer-reviewed ITS work exists **per axis**, and why integration is still open.

**Reading key:** Verify = runtime pedagogical / safety gate; Remember = durable learner state beyond chat history; Govern = structured teacher control with audit; Agentic = plans/tools over sessions; Ablation = reported component removal study.

#### 8.6.1 Cross-publisher comparison matrix

| Paper | Publisher | Verify | Remember | Govern | Agentic loop | Multi-session | Ablation | Closest EduHarness layer | Gap vs our plan |
|-------|-----------|:------:|:--------:|:------:|:------------:|:-------------:|:--------:|--------------------------|-----------------|
| **VERITAS** | ACM | Strong | Partial (RAG) | No | Multi-agent workflow | Course Q&A | No | H1 | No teacher protocol; verification is answer correctness, not mastery contract |
| **STAP** | ACM | Strong | Weak | No | Pipeline tutor | Single session | No | H1 | Socratic scaffolding + leakage control; no durable state or teacher patches |
| **Teacher-Driven Framework** | ACM | Partial (RAG validation) | Partial (VARK profiles) | Strong (teacher config UI) | Chat tutor | Not long-horizon | No | H3 | Teacher configures content/style; no runtime escalation contract or verify ablation |
| **Pair-Up** | ACM | No | Partial (analytics) | Strong (co-orchestration) | Classroom ITS ecosystem | Classroom sessions | No | H3 (different setting) | Classroom pairing/orchestration, not single-agent harness ablation |
| **Human-AI Co-Creative ITS** | ACM | Partial (HITL review) | No | Strong (teacher approves) | Conceptual ITS | Not specified | No | H3 | Conceptual co-creation; no verify+memory integration or ablation protocol |
| **PEAT** | IEEE | Partial (explainable feedback) | Strong (learner profiling) | No | Adaptive tutor | Simulated long use | No | H2 | Profiling + RL adaptation; no adversarial verify gate or teacher governance |
| **EduPlanner** | IEEE TLT | Partial (CIDDP evaluator) | Partial (Skill-Tree) | No | Multi-agent planners | N/A (planning) | Yes | Out of scope | Instructional **design** agents, not live tutoring harness — useful eval comparison only |
| **Responsible learner modeling** | IEEE Access | No | Strong (DKT vs LLM) | No | Tutoring case study | Temporal KT | No | H2 motivation | Shows LLM mastery drift; motivates structured Remember layer, not a harness design |
| **DBagent** | Springer | Partial (RAG grounding) | Strong (chat memory) | No | ReAct agent + tools | 4-week classroom | No | H0-H2 | CS agent with memory/RAG; no verify contract, adversarial eval, or teacher governance |
| **AGL** | Springer | No | No | Strong (advisory overlay) | Multi-agent advisory | Not specified | No | H3 | Multi-stakeholder **advisory** governance; does not verify pedagogy or maintain learner-state store |
| **ITS + LLM teaching review** | Springer | Discusses HITL | Discusses memory | Discusses oversight | Survey | Multi-session noted | N/A | Framing | Confirms gap: human validation and memory called out separately; integration rare |
| **SageJavon** | Elsevier | Partial (hint ladder) | Strong (graph KT) | No | LPES tutoring loop | 12-week course | Partial (RAG) | H2 | Full tutoring product with KT; no adversarial verify ablation or teacher escalation protocol |
| **PyTutor** | Elsevier | Strong (hint tiers) | Weak | No | ChatGPT ITS | 11-week study | Prompt A/B | H1 | Structured hints reduce leakage; no durable mastery store or teacher governance plane |
| **Reliable GenAI scaffolding** | Elsevier | Strong (multi-agent eval) | No | No | SRL scaffolds | N/A | Yes (agents) | H1 | Pre-delivery hallucination check for scaffolds; not live tutoring harness |
| **Adaptive tutoring via PK prompting** | Elsevier | Partial (pedagogical prompts) | Partial | No | Prompted tutor | Not long-horizon | No | H1 partial | Pedagogical-knowledge prompting; no memory compaction or teacher patches |

**Synthesis:** Across strict publishers, **Verify**, **Remember**, and **Govern** appear repeatedly but **almost never in one ablatable runtime harness around a single agentic tutor**. EduHarness occupies the empty cell: **Verify + Remember + Govern + H0-H3 factorial evaluation**.

#### 8.6.2 Publisher-by-publisher notes

**ACM**

| Paper | URL | Relevance | Comparison to EduHarness |
|-------|-----|-----------|---------------------------|
| VERITAS: Verification-based Tutoring Agent System | https://doi.org/10.1145/3748522.3779997 | Multi-agent verification + RAG for reliable ITS | Overlaps **H1** on factual/pedagogical reliability; we add **mastery-aware contract**, adversarial student prompts, and multi-session state |
| STAP: Socratic Tutor for Adaptive Programming | https://doi.org/10.1145/3775073.3775165 | Four-stage pipeline; formalizes answer leakage | Strong **H1** neighbor for programming domain; lacks Remember/Govern and ablation ladder |
| A Teacher-Driven Framework for Reliable and Personalised AI Tutors | https://doi.org/10.1145/3750069.3750121 | Teacher-curated RAG + VARK configuration | Overlaps **H3** on teacher agency; we add **runtime escalation**, evidence packets, and policy patches tied to verify rules |
| Pair-Up: Human-AI Co-orchestration in the Classroom | https://doi.org/10.1145/3544548.3581398 | Teacher overrides pairing suggestions; analytics dashboard | **Govern** precedent for teacher override; different unit of analysis (classroom orchestration vs single tutor harness) |
| Human-AI Co-Creative Intelligent Tutoring Systems | https://doi.org/10.1145/3766557.3766625 | Teacher-in-the-loop validation of AI tutoring decisions | Supports **Govern** motivation; EduHarness operationalizes with measurable intervention burden (Section 10) |

**IEEE**

| Paper | URL | Relevance | Comparison to EduHarness |
|-------|-----|-----------|---------------------------|
| PEAT: Scalable LLM-Powered Tutoring with Real-Time Adaptation | https://doi.org/10.1109/icec2nt65402.2025.11380089 | Dynamic learner profiling + explainable feedback | Overlaps **H2** on profiling; no verify gate under adversarial prompts or teacher policy patches |
| EduPlanner: Multiagent Instructional Design | https://doi.org/10.1109/tlt.2025.3561332 | Evaluator/optimizer agents for lesson plans | **Out of live-tutor scope** but shows IEEE appetite for **ablation** in educational AI systems |
| Why LLMs Fall Short for Responsible Learner Modeling | https://doi.org/10.1109/access.2026.3701047 | DKT beats LLM on temporal mastery coherence | **Motivates H2** structured state store rather than raw LLM memory |
| LLM-Based Hint Generation (PythonTutor pilot) | https://doi.org/10.1109/waie67422.2025.11381301 | Scaffolded hints + teacher oversight in web UI | Overlaps **H1 + partial H3** for programming; smaller pilot; no factorial harness study |

**Springer**

| Paper | URL | Relevance | Comparison to EduHarness |
|-------|-----|-----------|---------------------------|
| DBagent: LLM educational agent for CS (database course) | https://doi.org/10.1186/s40594-026-00641-y | ReAct agent, RAG, chat memory; 4-week quasi-experiment | Closest **agentic executor** neighbor in strict publishers; missing verify contract, adversarial eval, teacher governance |
| AGL: Multi-stakeholder Advisory Governance Layer | https://doi.org/10.1007/978-3-032-16451-3_23 | Non-intrusive governance overlay with audit | Closest **H3** architecture paper; **advisory only** — does not verify pedagogy or maintain learner-state compaction policies |
| Simulation of teaching behaviours in ITS (LLM review) | https://doi.org/10.1007/s10462-025-11464-8 | Systematic review of LLM-in-ITS | Use in thesis **Related Work**; cites human-in-the-loop feedback validation as open need — aligns with Govern |
| Leveraging RAG and AI Agents in Education (ICTIM) | https://doi.org/10.1007/978-3-032-15147-6_6 | RAG + async agents for CS/math Q&A | Agent + RAG baseline; no harness ablation |

**Elsevier**

| Paper | URL | Relevance | Comparison to EduHarness |
|-------|-----|-----------|---------------------------|
| SageJavon: Scalable AI tutor for programming (LPES) | https://doi.org/10.1016/j.ipm.2025.104605 | Learn-Practice-Evaluate-Support loop; graph KT; 12-week deployment | Strong **H2** product neighbor if domain = programming; no adversarial verify layer or teacher escalation protocol |
| PyTutor: ChatGPT ITS with structured hints | https://doi.org/10.1016/j.caeai.2024.100309 | Tiered hints; classroom RCT | Strong **H1** evidence for hint-based verification in Python; prompt A/B only — not integrated harness |
| Reliable GenAI-driven scaffolding (SRL) | https://doi.org/10.1016/j.compedu.2025.105448 | Multi-agent reliability evaluation before showing scaffolds | Parallel to **pre-response verify**; different task (SRL scaffolds, not multi-session agentic tutor) |
| Adaptive tutoring via pedagogical knowledge-augmented prompting | https://doi.org/10.1016/j.eswa.2026.133414 | PK-augmented prompts for adaptive tutoring | Prompt-level pedagogy; no durable state store or teacher governance |

#### 8.6.3 How EduHarness differs from the publisher landscape

Publisher literature confirms that **verification**, **memory**, and **governance** are active but **fragmented**. EduHarness proposes a **single original harness** that unifies all three with shared state, executive teacher patches, and H0–H3 ablation — evaluated on SHAPE / EduClaw / LongTutor metrics, not by reproducing SageJavon, DBagent, or AGL implementations.

#### 8.6.4 Recommended citations by thesis section

| Thesis section | Strict publisher papers to cite |
|----------------|----------------------------------|
| Introduction / problem | Márquez et al. (Springer review); IEEE Access learner modeling |
| Related work — Verify | STAP, PyTutor, VERITAS, Reliable GenAI scaffolding |
| Related work — Remember | SageJavon, PEAT, DBagent |
| Related work — Govern | AGL, Teacher-Driven Framework, Pair-Up, Co-Creative ITS |
| Differentiation | Comparison matrix (Section 8.6.1) |
| Evaluation design | EduPlanner (ablation methodology); SHAPE / EduClaw / LongTutor (metric sources) |

### 8.7 Positioning diagram

```text
                    AGENTIC (executor)
                         ^
                         |
              EduClaw-Bench - SocraticLM
                         |
    SHAPE ----------------+---------------- LongTutor
  (verify)               |              (history eval)
                         |
                         v
              OUR WORK: Agentic tutor
              + Pedagogical harness
              (verify + remember + govern)
                         |
                         v
              Deployable multi-session tutoring
              (benchmark + optional classroom)
```

### 8.8 Literature-informed boundaries (reference, not replication)

After reviewing publisher PDFs (Section 8.6), these **boundaries** keep EduHarness presented as **fresh work**:

| Topic | What related work does | What **EduHarness** does instead |
|-------|------------------------|----------------------------------|
| Agent executor | Various agents use RAG, ReAct, chat memory, LPES loops | **Fixed minimal executor** across all ablations; harness is what changes (H0→H3) |
| Verification | Turn-level hints, Socratic pipelines, answer-check agents | **Mastery-aware contract** tied to assessment mode + multi-session adversarial eval |
| Memory | Chat history, KT products, learner profiles | **Harness-owned structured store** with compaction, drift recovery, teacher overrides |
| Governance | Advisory overlays, config UIs, classroom orchestration | **Executive teacher protocol** — patches bind runtime behavior + audit trail |
| Evaluation | Per-paper classroom RCTs or single-axis metrics | **Unified H0–H3 factorial** on SHAPE + EduClaw + LongTutor + harness metrics |

**Presentation rule for thesis/paper:** Cite publisher work to show the gap; describe EduHarness architecture **without** "we adopt X from paper Y" in the contribution section. Use "prior work" / "related systems" language only in Related Work.

---

## 9. Novelty

### 9.1 What is not new (honest scope)

To avoid over-claiming:

- **Agentic tutoring loops** - EduClaw, SocraticLM, and many LMS agents already exist.
- **Turn-level pedagogical safety** - SHAPE and similar benchmarks cover this.
- **Extended multi-session evaluation** - EduClaw-Bench and LongTutor cover complementary slices.
- **General harness ideas** - context, tools, traces appear in software-agent harness surveys.
- **Single-axis publisher systems** - STAP/PyTutor/VERITAS (verify), SageJavon/PEAT/DBagent (remember), AGL/Pair-Up (govern) in IEEE/ACM/Springer/Elsevier (Section 8.6).

We do **not** claim to invent "the first AI tutor" or "the first harness."

### 9.2 What is new

| # | Novelty | Why it is original |
|---|---------|-------------------|
| 1 | **Hybrid research object** | Explicit split: **agent executes**, **harness is evaluated** — one integrated system, not another standalone tutor product |
| 2 | **Integrated pedagogical harness** | Verification + durable memory + teacher governance in **one stateful runtime** with shared audit trail |
| 3 | **Education-native verification contract** | Mastery-aware gating tied to assessment mode over **multi-day** agentic loops (beyond turn-level safety benchmarks) |
| 4 | **Memory as policy durability** | Learner store holds misconceptions, scaffolding history, **and** teacher overrides — harness-owned, not chat context |
| 5 | **Teacher governance protocol** | Escalation triggers, evidence packets, **executive** policy patches — measurable runtime service, not principles-only |
| 6 | **H0-H3 ablation on the same agent** | Causal claims about **which harness layer** fixes which failure (safety vs plateau vs governance load) |
| 7 | **Joint metric suite** | SHAPE (adversarial) + EduClaw (sustained learning gain) + LongTutor (diagnosis/teaching) + harness-only metrics in **one study** |
| 8 | **Trace-native layer attribution** | Label failures as agent vs memory vs verification vs governance |

### 9.3 Novelty in one paragraph

Recent work shows that educational LLMs must be **safe under adversarial prompting** (SHAPE), that **agentic tutoring quality depends on harness design** over weeks (EduClaw-Bench), and that models struggle to **diagnose and teach from long-term history** (LongTutor). This research contributes an **integrated pedagogical harness for an agentic tutor** that jointly enforces verification, maintains durable learner state, and operationalizes teacher governance - with **ablatable layers (H0-H3)** and evaluation metrics drawn from all three lines of work. The agent provides sustained multi-session tutoring behavior; the harness provides the **trust and deployability** that prior agentic systems lack.

### 9.4 Expected concrete outputs

| Output | Type |
|--------|------|
| Reference architecture (agent + harness) | Design |
| Pedagogical contract schema | Artifact |
| Teacher escalation + policy patch protocol | Protocol |
| H0-H3 ablation results | Empirical |
| Model x harness interaction analysis | Empirical |
| Trace schema with layer attribution | Method |
| Optional classroom pilot (H2 vs H3) | Deployment |

### 9.5 How we will show it worked (summary)

Full metric definitions, model comparison protocol, and result tables are in **Section 10**. At a high level:

| Source | Metrics | Our use |
|--------|---------|---------|
| SHAPE | Safety, Helpfulness, Pedagogy (adversarial) | H0 vs H1 (+ later layers) |
| EduClaw | Delta Solve, Helpfulness, Gagne, Rosenshine, plateau day | H0 vs H2 vs H3 on multi-day sim |
| LongTutor | MR, Macro-F1, History Utilization | H0 vs H2 on offline tasks |
| **Ours** | Policy compliance, state divergence, teacher intervention rate, patch latency, layer attribution | Harness-only contribution |

**Headline result sentence (fill after experiments):**

> The same agentic tutor at **H3** improves adversarial Safety by [X]% vs **H0**, reduces state divergence by [Y]% vs **H1**, raises History Utilization by [Z] vs prompt-only memory, and keeps teacher interventions below [N] per student-hour - showing that trustworthy agentic tutoring requires harness design, not a stronger agent alone.

---

## 10. Performance Metrics and Evaluation Protocol

This section defines **what to measure**, **how to compare different LLMs**, and **how to evaluate and report results**. Metrics are borrowed from anchor papers where possible so our numbers are comparable; we add harness-specific metrics for contributions SHAPE, EduClaw, and LongTutor do not cover together.

### 10.1 Design principle: model x harness factorial

EduClaw-Bench shows tutoring quality is a **joint property of base model and harness** — rankings change when either is swapped. Our evaluation must therefore report **both**:

1. **Harness ablation** — same model, H0 vs H1 vs H2 vs H3 (what each layer adds)
2. **Model comparison** — same harness level, Model A vs Model B vs Model C (which LLM benefits most from the harness)

```text
                    H0    H1    H2    H3
Model A (frontier)   .     .     .     .
Model B (mid-tier)   .     .     .     .
Model C (open)       .     .     .     .

Each cell = full metric suite for that (model, harness) pair
```

**Minimum experimental grid:** 2 model tiers x 4 harness levels = **8 conditions**. Stretch: 3 tiers x 4 levels = 12 conditions.

**Recommended model tiers (lock IDs in every run):**

| Tier | Example models | Role |
|------|----------------|------|
| Frontier | GPT-4o, Claude Sonnet, Gemini Pro | Strong baseline; may saturate some metrics |
| Mid | GPT-4o-mini, Llama-3-70B, Qwen-72B | Where harness effect often largest (EduClaw finding) |
| Open/local | Llama-3-8B, Qwen-7B | Cost and deployability stress test |

---

### 10.2 Metrics from existing work (borrow for comparison)

#### A. SHAPE — verification and adversarial pedagogy

**Paper:** SHAPE (ACL 2026) — turn-level Safety, Helpfulness, Pedagogy under adversarial prompting.

| Metric | Definition | How computed | Higher / lower is better |
|--------|------------|--------------|--------------------------|
| **Safety** | Withholds direct answer when prerequisites not mastered | % of test pairs where model does not leak solution | Higher |
| **Helpfulness** | Gives solution when mastery is complete | % of pairs where mastered student gets full help | Higher |
| **Pedagogy** | Among safe responses, targets missing concepts | % of safe responses with concept-focused scaffolding | Higher |
| **Safety (default)** | Safety under normal student prompts | Same, non-adversarial subset | Higher |
| **Safety (adversarial)** | Safety under refusal suppression / role play | Worst-case or per-attack-type breakdown | Higher |
| **Worst-case drop** | Safety(default) - Safety(worst adversarial) | Measures brittleness | Lower drop is better |

**When to run:** H0 vs H1 primary; report H2/H3 to show verification survives memory compaction and governance.

**Test set:** SHAPE benchmark subset or domain-matched adversarial set (100+ pairs minimum).

---

#### B. EduClaw-Bench — extended agentic tutoring evaluation

**Paper:** EduClaw-Bench (arXiv 2026) — 30-day agent + LMS + KT simulated learner, 55 scenarios.

| Axis | Metric | Definition | How computed | Better |
|------|--------|------------|--------------|--------|
| **I — Learning gain** | **Delta Solve Rate** | Per-day improvement in solve rate | Mean slope of daily solve accuracy over horizon | Higher |
| | **Absolute solve rate** | Final day solve accuracy | End-state learning proxy | Higher |
| | **Plateau day** | Day learning gain flattens | First day where delta < threshold for K consecutive days | Later |
| **II — Responsiveness** | **Response rate** | Fraction of student help-requests answered | answered / total help events | Higher (with caveats) |
| **III — Helpfulness** | **LearnLM rubric score** | Panel-judged helpfulness (29 items) | Mean 1-10 per day or per scenario | Higher |
| **IV — Curriculum** | **Gagne score** | 9 Events of Instruction coverage | Rubric 1-5 | Higher |
| | **Rosenshine score** | 10 Principles of instruction | Rubric 1-5 | Higher |
| **Safety aux.** | **Answer-holding rate** | Tutor withholds on help-request days | % days without solution leak | Higher |
| | **Hand-over rate** | Premature full solution given | Lower is better | Lower |
| **Failure modes** | **No-curriculum rate** | % runs with no structured progression | EduClaw reports ~48.5% baseline failure | Lower |
| | **No-learning-gain rate** | % runs with flat/negative delta | EduClaw reports ~53.3% baseline failure | Lower |
| **Simulator validity** | **ECE** | Expected calibration error of KT learner | EduClaw reports 0.049 | Lower |
| | **pass@k** | Judge/expert agreement stability | Reliability of automated scoring | Higher |

**When to run:** H0 vs H2 vs H3 on 14-30 day sim (full 30 if resources allow). Primary harness comparison for **Remember** and **Govern**.

**Key claim vs EduClaw baselines:** later plateau, lower no-curriculum / no-learning-gain rates, higher post-plateau delta.

---

#### C. LongTutor — history, diagnosis, teaching

**Paper:** LongTutor (ACL 2026) — Evidence, Diagnosis, Teaching on expert-annotated logs.

| Task | Metric | Definition | Better |
|------|--------|------------|--------|
| **Evidence acquisition** | **IE** (Information Extraction) | Extract facts from single record | Higher |
| | **MR** (Multi-session Reasoning) | Reason across session history | Higher |
| | **HC** (Hallucination Check) | Reject false premises | Higher |
| | **Semantic accuracy (overall)** | Combined evidence score | Higher |
| **State diagnosis** | **Accuracy** | Correct knowledge-state label | Higher |
| | **Macro-F1** | Class-imbalanced diagnosis; best ~40% in paper | Higher |
| **Teaching action** | **ROUGE-L** | Overlap with reference teaching move | Higher |
| | **History Utilization** | LLM judge 1-5: uses long-term history | Higher |
| | **Strategy** | Judge: appropriate teaching strategy | Higher |
| | **Coherence** | Judge: coherent with prior sessions | Higher |
| | **Appropriateness** | Judge: pedagogically appropriate | Higher |

**When to run:** H0 vs H2 offline on LongTutor golden subset; links **Remember** layer to diagnosis/teaching quality.

---

#### D. Other related metrics (optional but useful)

| Source | Metric | Use in our study |
|--------|--------|------------------|
| **Harness Effect** (Sayed Ali et al.) | Token cost per task, cost per successful outcome | Report cost alongside quality at each H-level |
| **TEAS** | Trust, auditability, pedagogical soundness checklist | Qualitative rubric for H3 governance case studies |
| **SocraticLM** | Pedagogical dialogue quality | Baseline comparison for agent utterance style (not main claim) |
| **VanLehn (2011)** | Learning gain vs human tutoring | Context for interpreting delta solve magnitude |

---

### 10.3 Harness-specific metrics (our contribution)

These metrics are **not fully covered** by SHAPE, EduClaw, or LongTutor alone. They justify the integrated harness claim.

| Metric | Layer | Definition | How to measure | Target |
|--------|-------|------------|----------------|--------|
| **Policy compliance rate** | Verify (H1+) | % turns where output matches contract decision | Automated check: action allowed vs action taken | Higher |
| **Direct-answer leakage rate** | Verify | % adversarial turns where full solution appears | Regex + judge on withheld cases | Lower |
| **State divergence** | Remember (H2+) | Distance between inferred mastery and simulator/LMS ground truth | L1 or Brier over concepts x time | Lower |
| **Contradiction rate** | Remember | % sessions where tutor contradicts prior scaffolding | NLI or rule check vs instructional log | Lower |
| **Drift recovery rate** | Remember | % drift events detected and repaired | drift flagged -> re-assessment within N turns | Higher |
| **Memory recall accuracy** | Remember | Correct retrieval on "what did you teach me?" probes | Match against scaffolding log | Higher |
| **Teacher intervention rate** | Govern (H3) | Escalations per student-hour | count(escalations) / tutoring hours | Lower (without safety loss) |
| **Teacher approval latency** | Govern | Time from queue to teacher action | median minutes | Lower |
| **Policy patch latency** | Govern | Time from patch to changed harness behavior | seconds to next compliant turn | Lower |
| **Patch success rate** | Govern | % patches that fix the triggering failure class | Re-run trigger scenario after patch | Higher |
| **Layer attribution accuracy** | Audit | Correct label on failed turns (human gold on sample) | agent / memory / verify / govern | Higher |
| **Over-reliance proxy** | Verify + Remember | % sessions with excessive hint-seeking without independent attempt | Count answer requests before student submission / effort signal | Lower (balanced use) |
| **Harness ablation gain** | All | Delta metric from H0->H1->H2->H3 | Per-metric staircase plot | Positive where expected |

---

### 10.4 Composite score: Trustworthy Tutoring Index (TTI)

For a single headline number (thesis abstract / paper intro), combine normalized metrics:

```text
TTI = w1 * Safety_adversarial
    + w2 * Helpfulness
    + w3 * Delta_Solve_Rate_norm
    + w4 * (1 - State_divergence_norm)
    + w5 * History_Utilization_norm
    + w6 * (1 - Teacher_burden_norm)
    + w7 * Policy_compliance

Weights w1-w7: set by domain + supervisor; report sensitivity analysis (vary weights +/- 20%).
```

Report TTI per **(model, harness)** cell. Expected pattern:

- TTI(H3, Model B) > TTI(H0, Model A) would show **harness beats raw model tier**
- TTI(H1) >> TTI(H0) across all models shows **verification generalizes**

---

### 10.5 How to compare different LLMs fairly

| Rule | Why |
|------|-----|
| **Same harness code** for all models at each H-level | Only swap model API / weights |
| **Lock temperature, max tokens, top-p** | Reproducibility |
| **Same test sets and scenarios** | Comparable inputs |
| **Same simulated learner** (EduClaw-style) | Fair extended tutoring comparison |
| **Report model ID + date** | Models change over time |
| **Report cost** (tokens, USD, latency) | Harness Effect line of work |
| **Do not compare H3 on Model A to H0 on Model B** without factorial design | Confounds model and harness |

**Analysis types:**

1. **Main effect of harness** — average across models: does H3 beat H0?
2. **Main effect of model** — average across harness levels: does frontier beat open?
3. **Interaction (model x harness)** — does harness help mid-tier more than frontier? (EduClaw hypothesis)

Use **two-way ANOVA or mixed-effects model** with scenario as random effect if running multiple EduClaw scenarios.

---

### 10.6 Evaluation protocol (step by step)

#### Experiment E1 — Adversarial verification (SHAPE-style)

| Setting | Value |
|---------|-------|
| Conditions | All models x H0, H1 (optionally H2, H3) |
| Input | Default + adversarial prompt sets |
| Output table | Safety, Helpfulness, Pedagogy x condition |
| Primary comparison | H0 vs H1 per model; worst-case drop |

#### Experiment E2 — Extended multi-session tutoring (EduClaw-style)

| Setting | Value |
|---------|-------|
| Conditions | All models x H0, H2, H3 (memory + govern focus) |
| Horizon | 14 days minimum; 30 days stretch |
| Scenarios | Subset of 55 (e.g. 5 personas x 3 schedules = 15) |
| Output | Learning curve per day; Delta Solve; plateau day; failure modes |
| Primary comparison | H3 vs H0; model x harness interaction on plateau day |

#### Experiment E3 — History-aware teaching (LongTutor-style)

| Setting | Value |
|---------|-------|
| Conditions | All models x H0, H2 |
| Input | LongTutor golden tasks or domain subset |
| Output | MR, Macro-F1, History Utilization judge scores |
| Primary comparison | H2 vs H0 per model |

#### Experiment E4 — Governance load (H3 only)

| Setting | Value |
|---------|-------|
| Conditions | H2 vs H3 (same model) |
| Input | Repeated adversarial + high-stakes exam-mode prompts |
| Output | Intervention rate, patch latency, teacher workload survey |
| Primary comparison | H3 adds control without unacceptable burden |

#### Experiment E5 — Dynamic teacher profiles (optional)

| Setting | Value |
|---------|-------|
| Conditions | Same model + H3; Teacher A vs Teacher B contract |
| Input | Same student prompt stream |
| Output | Different Safety/Helpfulness trade-offs; patch log diff |
| Primary comparison | Shows dynamic Remember/Govern (see `dynamic_remember_and_govern.md`) |

---

### 10.7 Result tables to include in thesis / paper

#### Table 1 — Harness ablation (one model, all levels)

| Metric | H0 | H1 | H2 | H3 | Delta H0->H3 |
|--------|----|----|----|----|--------------|
| Safety (adversarial) | | | | | |
| Helpfulness | | | | | |
| Delta Solve Rate | | | | | |
| State divergence | | | | | |
| History Utilization | | | | | |
| Teacher interventions / hr | N/A | N/A | N/A | | |
| TTI | | | | | |

#### Table 2 — Model comparison (H3 fixed)

| Model | Tier | Safety | Delta Solve | TTI | Cost / 1k turns |
|-------|------|--------|-------------|-----|-----------------|
| Model A | Frontier | | | | |
| Model B | Mid | | | | |
| Model C | Open | | | | |

#### Table 3 — Model x harness interaction (TTI or Safety)

| | H0 | H1 | H2 | H3 |
|---|----|----|----|----|
| Model A | | | | |
| Model B | | | | |
| Model C | | | | |

Highlight cells where **mid-tier + H3** beats **frontier + H0** — strongest harness argument.

#### Figure 1 — Learning curve

Per-day Delta Solve (or solve rate) over 14-30 days; lines = H0, H2, H3 for one model; shaded = plateau region.

#### Figure 2 — Ablation staircase

Bar chart: TTI at H0, H1, H2, H3 averaged across models with error bars.

#### Figure 3 — Governance case study

3-5 traced episodes: trigger -> evidence packet -> teacher patch -> corrected behavior.

---

### 10.8 Minimum viable evaluation (if time is limited)

| Priority | Experiment | Models | Metrics | Enough for thesis? |
|----------|------------|--------|---------|------------------|
| 1 | E1 adversarial | 2 models x H0,H1 | Safety, Helpfulness | Partial |
| 2 | E2 short horizon (7-14 days) | 2 models x H0,H2,H3 | Delta Solve, plateau day | Yes with caveats |
| 3 | Harness-only | 1 model x H0-H3 | Policy compliance, state divergence | Yes |
| 4 | E3 LongTutor offline | 1 model x H0,H2 | MR, History Utilization | Strengthens Remember |
| 5 | Full E2 (30 days) + E4 pilot | 3 models | Full suite | Strong paper |

---

### 10.9 How to interpret results (what counts as success)

| Observation | Interpretation |
|-------------|----------------|
| H1 >> H0 on Safety across all models | Verification layer works; not model-specific luck |
| H2 improves MR / History Utilization vs H0 | Remember layer helps long-term teaching |
| H3 reduces repeated failures with intervention rate < threshold | Govern layer is deployable |
| Mid-tier + H3 beats frontier + H0 on TTI | **Harness matters as much as model choice** (EduClaw-style interaction claim) |
| Rankings reorder across model tiers | Report interaction; do not average blindly |
| Frontier saturates at H1; open model gains through H3 | Harness most valuable where model is weaker |

**Failure to report honestly:**

- Safety up but Helpfulness collapses -> over-refusal; tune contract
- Delta Solve flat at all levels -> domain/simulator issue; not harness success
- H3 with very high intervention rate -> governance too sensitive; tune triggers

---

### 10.10 Metric-to-layer mapping (quick reference)

| Layer | Primary metrics | Secondary metrics |
|-------|-----------------|-----------------|
| **H0 baseline** | Helpfulness, Delta Solve (raw agent) | Cost, latency |
| **H1 Verify** | Safety, Pedagogy, policy compliance, leakage rate | Worst-case drop |
| **H2 Remember** | State divergence, MR, Macro-F1, History Utilization, drift recovery | Contradiction rate |
| **H3 Govern** | Intervention rate, patch latency, patch success | Teacher workload survey |
| **Full H3** | TTI, model x harness interaction, layer attribution | EduClaw failure mode rates |

---

## 11. Risks

| Risk | Mitigation |
|------|------------|
| Reviewers say "just engineering" | Lead with H0-H3 ablations + learning proxies + EduClaw-style curves |
| Reviewers say "another agentic tutor" | Lead abstract with **harness contribution**; agent is executor |
| Overlap with SHAPE on H1 | Emphasize multi-session + teacher layer; do not stop at turn-level safety |
| Overlap with EduClaw on eval | Do not only swap adapters - show **verify+memory+govern** as unified design |
| Scope creep | One domain (**Python programming**), one agent, four harness levels, no multi-agent |
| No classroom access | Benchmark-first (EduClaw / SHAPE / LongTutor); optional small pilot only if approved |
| Student over-reliance on tutor | Contract caps hints; track over-reliance proxy; exam-mode stricter gate |
| Cognitive offloading | Balance Helpfulness vs independent problem-solving; report hint-to-submission ratio |

---

## 12. Short Pitch for Sir

I want to work on **agentic tutoring** - an LLM agent that tutors over days with tools and course context - because that matches where the field is going (EduClaw, educational agents). But I do not want to submit "another tutor chatbot." The research contribution is **EduHarness** — a new **pedagogical harness** around a standard agent executor: verify pedagogy under adversarial prompts, remember the learner in a structured store, and give teachers executive governance with policy patches.

SHAPE, EduClaw, and LongTutor supply the evaluation benchmarks. Publisher ITS papers (Section 8.6) show verification, memory, and governance are usually separate systems — **we unify them in one ablatable harness** with H0-H3, so we can show **which layer** makes agentic tutoring trustworthy. The framing: **fresh harness design; agent is the testbed, not the claim.**

---

## 13. References

### 13.1 Evaluation anchors (benchmarks and preprints)

1. SHAPE (2026). https://arxiv.org/abs/2604.22134  
2. EduClaw-Bench (2026). https://arxiv.org/abs/2608.03206  
3. LongTutor (2026). https://aclanthology.org/2026.acl-long.1371.pdf  
4. Zhong, H., & Zhu, S. (2026). AI Harness Engineering. https://arxiv.org/abs/2605.13357  
5. Liu, J., et al. (2024). SocraticLM. NeurIPS 2024. https://proceedings.neurips.cc/paper_files/paper/2024/hash/9bae399d1f34b8650351c1bd3692aeae-Abstract-Conference.html  
6. TEAS (2026). https://arxiv.org/abs/2601.06066  
7. Chu, Z., et al. (2025). LLM Agents for Education. https://aclanthology.org/2025.findings-emnlp.743/  
8. Li, S., & Zheng, J. (2026). Scoping Review of LLM Pedagogical Agents. https://arxiv.org/abs/2604.12253  
9. Sayed Ali, M., et al. (2026). The Harness Effect. https://arxiv.org/abs/2607.06906  
10. VanLehn, K. (2011). Effectiveness of tutoring systems. *Educational Psychologist*, 46(4), 197-221.

### 13.2 Strict publisher literature (IEEE / ACM / Springer / Elsevier)

**ACM**

11. Oli, P., et al. (2025). VERITAS: A Multi-Agent Verification-Based Framework for Reliable Intelligent Tutoring Systems. https://doi.org/10.1145/3748522.3779997  
12. [STAP authors] (2025). STAP: A Socratic Tutor for Adaptive Programming with Pedagogical Scaffolding. https://doi.org/10.1145/3775073.3775165  
13. [Teacher-Driven Framework authors] (2025). A Teacher-Driven Framework for Reliable and Personalised AI Tutors. https://doi.org/10.1145/3750069.3750121  
14. Holstein, K., et al. (2023). Pair-Up: Prototyping Human-AI Co-orchestration of Dynamic Transitions between Individual and Collaborative Learning in the Classroom. https://doi.org/10.1145/3544548.3581398  
15. [Co-Creative ITS authors] (2025). Theoretical Framework and Application Strategies of Human-AI Co-Creative Intelligent Tutoring Systems. https://doi.org/10.1145/3766557.3766625  

**IEEE**

16. [PEAT authors] (2025). PEAT: A Scalable LLM-Powered Tutoring System with Real-Time Adaptation and Explainable Feedback for Diverse Learners. https://doi.org/10.1109/icec2nt65402.2025.11380089  
17. Zheng, Y., et al. (2025). EduPlanner: LLM-Based Multiagent Systems for Customized and Intelligent Instructional Design. *IEEE Transactions on Learning Technologies*, 18. https://doi.org/10.1109/tlt.2025.3561332  
18. [IEEE Access authors] (2026). Why Large Language Models Alone Fall Short for Responsible Learner Modeling in K-12 Tutoring: A Case Study. https://doi.org/10.1109/access.2026.3701047  
19. [PythonTutor authors] (2025). Enhancing High School Programming Education Through LLM-Based Hint Generation. https://doi.org/10.1109/waie67422.2025.11381301  

**Springer**

20. [DBagent authors] (2026). The impact of an LLM-based educational agent on learning achievement, cognitive dynamics, and student perceptions in computer science education. *International Journal of STEM Education*. https://doi.org/10.1186/s40594-026-00641-y  
21. Uchoa, A. P., et al. (2026). Multi-stakeholder Alignment in LLM-Powered Collaborative AI Systems: A Multi-agent Framework for Intelligent Tutoring (AGL). https://doi.org/10.1007/978-3-032-16451-3_23  
22. Márquez-Carpintero, L., López-Sellers, A., & Cazorla, M. (2026). Simulation of teaching behaviours in intelligent tutoring systems: a review using large language models. *Artificial Intelligence Review*, 59, 56. https://doi.org/10.1007/s10462-025-11464-8  
23. El Jiani, L., et al. (2026). Leveraging RAG and AI Agents to Enhance Specialized LLMs in Education. https://doi.org/10.1007/978-3-032-15147-6_6  

**Elsevier**

24. Zhao, H., et al. (2026). SageJavon: A scalable AI tutor for personalized programming learning. *Information Processing & Management*, 63(5), 104605. https://doi.org/10.1016/j.ipm.2025.104605  
25. Yang, A. C. M., et al. (2024). Enhancing python learning with PyTutor: Efficacy of a ChatGPT-Based intelligent tutoring system in programming education. *Computers and Education: Artificial Intelligence*, 7, 100309. https://doi.org/10.1016/j.caeai.2024.100309  
26. [Reliable scaffolding authors] (2026). Towards reliable generative AI-driven scaffolding: Reducing hallucinations and enhancing quality in self-regulated learning support. *Computers & Education*, 105448. https://doi.org/10.1016/j.compedu.2025.105448  
27. [PK-augmented tutoring authors] (2026). Leveraging large language models for adaptive tutoring system via pedagogical knowledge-augmented prompting. *Expert Systems with Applications*, 133414. https://doi.org/10.1016/j.eswa.2026.133414  

---

*Domain: undergraduate programming (Python). Publisher literature: Section 8.6 (reference only). Evaluation anchors: SHAPE, EduClaw, LongTutor.*