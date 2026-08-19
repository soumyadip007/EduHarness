# Frontend Guide (Dashboard UX)

## Frontend stack

- Next.js App Router
- React + TypeScript
- Material UI

## Role-based routes

- `/student` -> learner tutoring workspace
- `/teacher` -> governance queue and interventions
- `/researcher` -> experiment operations

Supporting views:

- `/student/progress`
- `/student/sessions`
- `/teacher/*` detail pages
- `/researcher/results`
- `/researcher/traces`
- `/researcher/costs`
- `/researcher/annotate`

## Visual architecture

- Global shell:
  - top app bar
  - persistent side navigation
  - content container
- Shared design tokens in `src/theme/theme.ts`
- Card-based page sections for scannability

## Frontend data flow

1. Page/hook makes API call (`getJson` / `postJson`).
2. Backend returns structured JSON.
3. React state updates.
4. UI sections redraw.

## Realtime path

- Teacher queue uses websocket updates from `/ws/escalation`.
- On update event, queue hook refetches state.

## How to improve UI further

- Add role guards and auth context.
- Add loading skeletons and error boundaries.
- Add global notification system (snackbar).
- Add richer charting library for analytics pages.
- Add dark mode toggle and saved preferences.
