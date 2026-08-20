# API Keys and Model Configuration

EduHarness uses **environment variables** for provider credentials. Model profiles (which provider and model ID to call) are defined separately in YAML.

## Where to put API keys

### Primary location: `.env` file (recommended)

Copy the example file and fill in your keys:

```bash
cp .env.example .env
```

Edit `.env` in the **project root**:

```bash
# OpenAI (for mid_primary, frontier_reference)
OPENAI_API_KEY=sk-...

# Anthropic (optional)
ANTHROPIC_API_KEY=...

# Groq — hosted OSS models (mistral_groq profile)
GROQ_API_KEY=gsk_...

# OpenRouter — many OSS/commercial models (qwen_openrouter profile)
OPENROUTER_API_KEY=sk-or-...

# Ollama — local models (llama_local, gemma_ollama)
# No API key needed; ensure Ollama is running:
LOCAL_MODEL_BASE_URL=http://localhost:11434

# Which model profile to use by default
ACTIVE_MODEL_KEY=mid_primary
```

Load the file before starting the API:

```bash
set -a && source .env && set +a
uvicorn api.main:app --reload --port 8000
```

Or use `python-dotenv` if your startup script loads `.env` automatically.

### Reference template: `.env.example`

Path: `.env.example` — documents all supported variables (no secrets committed).

---

## Where model profiles are defined (not API keys)

Path: **`configs/models/model_registry.yaml`**

This file defines **named profiles** — not secrets:

```yaml
models:
  mid_primary:
    provider: openai
    model_id: gpt-4o-mini
  mistral_groq:
    provider: groq
    model_id: llama-3.1-8b-instant
    open_source: true
  llama_local:
    provider: ollama
    model_id: llama3.2
    open_source: true
```

Each profile's `provider` determines which **environment variable** is read at runtime:

| Provider in YAML | Required env variable |
|------------------|----------------------|
| `openai` | `OPENAI_API_KEY` |
| `anthropic` | `ANTHROPIC_API_KEY` |
| `groq` | `GROQ_API_KEY` |
| `openrouter` | `OPENROUTER_API_KEY` |
| `ollama` | None (uses `LOCAL_MODEL_BASE_URL`) |

---

## How to select the active model

Three ways (in priority order for a chat turn):

1. **Per-request** — `model_key` in `POST /api/student/message` or student UI dropdown
2. **Database setting** — `PUT /api/config/models/active` (Researcher dashboard → “Save global model”)
3. **Environment default** — `ACTIVE_MODEL_KEY=mid_primary` in `.env`

List available profiles:

```bash
curl http://localhost:8000/api/config/models
```

---

## Open-source setup examples

### Local Ollama (no cloud keys)

```bash
ollama pull llama3.2
export ACTIVE_MODEL_KEY=llama_local
export LOCAL_MODEL_BASE_URL=http://localhost:11434
```

### Groq (free tier, hosted OSS)

```bash
export GROQ_API_KEY=your_key_from_console.groq.com
export ACTIVE_MODEL_KEY=mistral_groq
```

### OpenRouter

```bash
export OPENROUTER_API_KEY=your_key_from_openrouter.ai
export ACTIVE_MODEL_KEY=qwen_openrouter
```

---

## Fallback behavior

If the selected profile's provider key is **missing**, EduHarness returns a deterministic stub tutor response so local development and tests still work. For production, ensure the correct key is set for your chosen `ACTIVE_MODEL_KEY`.

---

## Related docs

- [Configure Models](configure-models.md)
- [Improvement Plan](../../improvementplan.md)
