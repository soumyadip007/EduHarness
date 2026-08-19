# Setup & Run

## Prerequisites

- Python 3.11+
- Node.js 18+ and npm
- Git

## Backend setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Optional API keys:

```bash
export OPENAI_API_KEY=your_key
export ANTHROPIC_API_KEY=your_key
```

Run backend:

```bash
uvicorn api.main:app --reload --port 8000
```

## Frontend setup

```bash
cd frontend
npm install
export NEXT_PUBLIC_API_BASE=http://localhost:8000
npm run dev
```

Open:

- `http://localhost:3000/` (dashboard home)
- `http://localhost:3000/student`
- `http://localhost:3000/teacher`
- `http://localhost:3000/researcher`

## Run tests

From repo root:

```bash
source .venv/bin/activate
pytest -q
```

## Run evaluation pipeline

```bash
source .venv/bin/activate
python evaluation/run_full_phase6.py
python scripts/export_results.py
```

## Build frontend

```bash
cd frontend
npm run build
```

## Run docs (MkDocs)

Install doc dependencies:

```bash
source .venv/bin/activate
pip install mkdocs mkdocs-material
```

Serve docs:

```bash
mkdocs serve
```

Build static docs:

```bash
mkdocs build
```
