# Frontend Design Improvement Plan (Material UI Dashboard)

## Goal
Transform the current functional UI into a cohesive, high-clarity dashboard experience across Student, Teacher, and Researcher workflows.

## Phase A - Foundation (Completed)
- Add Material UI core and icons.
- Define a shared app theme (colors, typography, spacing, radius).
- Add a reusable app shell with:
  - top app bar
  - persistent left navigation
  - unified content container

## Phase B - Dashboard Experience (Completed)
- Upgrade landing page into a role-based dashboard entry point.
- Upgrade Student page into a card-based workspace:
  - harness mode selector
  - chat + code sandbox
  - mastery intelligence panel
- Upgrade Teacher page into a governance dashboard:
  - queue state chip
  - primary call to action for escalation simulation
  - live queue cards
- Upgrade Researcher page into experiment dashboard:
  - experiment launch panel
  - run status panel

## Phase C - UX Polish (Next)
- Replace remaining inline styles in all teacher/researcher subpages with MUI components.
- Add consistent KPI tiles for:
  - interventions
  - TTI
  - cost
  - safety
- Add responsive behavior for smaller screens (temporary drawer mode).
- Add loading skeletons and empty states per module.

## Phase D - Trust & Usability (Next)
- Add route guards for role-specific access (student/teacher/researcher).
- Add error surfaces (snackbar + retry actions).
- Add accessibility pass (contrast, tab order, aria labels).
- Add analytics hooks for key user actions.

## Success Criteria
- Every major route uses the same visual system (theme + shell + cards).
- User can navigate role workflows in <= 2 clicks from home.
- Dashboard surfaces key status/metrics without opening raw JSON pages.
