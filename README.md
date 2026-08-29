# Skill Gap Analyzer — HTML + Google Gemini

FastAPI backend + HTML frontend. The app includes dashboard skill-gap analysis, Gemini roadmap generation, a Skills Library backed by `data/knowledge_base`, and individual Gemini skill analysis.

## Setup

1. Create a virtual environment:

```bash
python -m venv .venv
```

2. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and set `GOOGLE_API_KEY`.

4. Run:

```bash
python -m uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/`.

## API

- `GET /api/roles`
- `POST /api/analyze`
- `POST /api/roadmap`
- `GET /api/skills`
- `GET /api/skills/{skill_name}`
- `POST /api/skill-analyze`

Add Markdown skill files to `data/knowledge_base/`; the Skills Library discovers them automatically.
