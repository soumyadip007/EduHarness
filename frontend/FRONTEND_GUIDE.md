# Frontend Guide

## Stack
- Next.js App Router
- React + TypeScript
- Material UI (MUI)

## Architecture
- `src/app/layout.tsx`
  - Global root layout
  - Wraps all pages with:
    - `AppThemeProvider` (MUI theme + CssBaseline)
    - `AppShell` (top bar + side nav + content area)
- `src/theme/theme.ts`
  - Centralized visual tokens (palette, typography, shape)
- `src/lib/api.ts`
  - API base and request helpers (`getJson`, `postJson`)

## Core Flows

### Student Flow
- Route: `/student`
- Hook: `useChat` for tutoring turns
- Hook: `useMastery` for mastery snapshot and refresh after each message
- Components:
  - chat panel + input
  - code sandbox
  - mastery summary side panel

### Teacher Flow
- Route: `/teacher`
- Hook: `useEscalation`
  - fetches queue from API
  - listens to `/ws/escalation` for live queue updates
- Components:
  - escalation cards
  - queue status chip
  - simulate escalation action

### Researcher Flow
- Route: `/researcher`
- Triggers Phase 6 experiment runs via API
- Tracks experiment state and latest run time
- Linked pages:
  - `/researcher/results`
  - `/researcher/traces`
  - `/researcher/costs`
  - `/researcher/annotate`

## How Data Moves
1. User action on dashboard page.
2. UI calls backend via `getJson`/`postJson`.
3. API returns typed JSON payload.
4. Page or hook updates local state.
5. UI re-renders cards/charts/tables.

## Local Run
```bash
cd frontend
npm install
npm run dev
```

Set API endpoint if needed:
```bash
export NEXT_PUBLIC_API_BASE=http://localhost:8000
```

## Frontend Conventions
- Use MUI components first; avoid new inline CSS for new pages.
- Keep API calls in hooks or page-level fetch functions.
- Prefer card-based sections with clear headings and one primary CTA.
- Keep role workflows separated by route (`/student`, `/teacher`, `/researcher`).
