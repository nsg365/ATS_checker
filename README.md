# 🐒 ResumeLens

**Know your resume's ATS score in 30 seconds.** ResumeLens analyzes a resume (and optionally a job description) and returns a 0–100 Applicant Tracking System (ATS) compatibility score with prioritized, actionable fixes.

It combines LLM-based resume parsing, semantic skill validation, and keyword matching to tell you not just *what's wrong*, but *what to fix first*.

---

## Overview

ResumeLens is a two-tier application:

- **Backend** — a FastAPI service that parses resumes, scores them across five dimensions, compares them against job descriptions, generates feedback, and renders downloadable PDF reports.
- **Frontend** — a Streamlit web app with a landing page, the scorer, analysis history, and a resources guide. Authentication and per-user history are handled via Supabase (email/password + Google OAuth).

```
┌──────────────┐      HTTPS (JWT)      ┌──────────────┐
│   Streamlit  │  ─────────────────▶   │   FastAPI    │
│   frontend   │                       │   backend    │
│ (auth, UI)   │  ◀─────────────────   │ (analysis)   │
└──────┬───────┘     JSON / PDF        └──────┬───────┘
       │                                      │
       │ Supabase Auth + DB                   │ Groq LLM (parsing)
       ▼                                      │ spaCy + SentenceTransformers
┌──────────────┐                             ▼
│   Supabase   │ ◀──── analyses table ──── (history saved per user)
└──────────────┘
```

---

## Features

- **5-dimension ATS scoring** — formatting, keywords, content quality, skill validation, and ATS compatibility.
- **LLM resume parsing** — uses Groq (`llama-3.3-70b-versatile`) to extract structured data (skills, experience, projects, education, contact info) from raw resume text.
- **Semantic skill validation** — verifies each listed skill is actually backed by a project or experience bullet, using sentence-embedding similarity.
- **Job-description matching** — match percentage, missing keywords, and skills gap via fuzzy + semantic comparison.
- **Prioritized recommendations** — a ranked to-do list with estimated score impact.
- **Detailed, severity-grouped feedback** — each issue includes an explanation, where it appears, how to fix it, action items, and an example.
- **PDF report export** — multi-section report rendered with WeasyPrint.
- **Per-user history** — every analysis is saved to your account and can be reopened, re-exported as PDF, or deleted.
- **Accounts** — email/password and Google OAuth via Supabase; history is private to each user.
- **Light/dark mode** — defaults to dark.

---

## How the ATS score works

Each component is scored on its own scale, then combined into the overall 0–100 score.

| Component          | Max points | What it measures                                              |
|--------------------|:----------:|--------------------------------------------------------------|
| Formatting         | 20         | Standard sections, bullet points, structure                  |
| Keywords           | 25         | Keyword/skill density; JD keyword match when a JD is provided |
| Content            | 25         | Action verbs and quantified achievements                     |
| Skill Validation   | 15         | Share of skills backed by projects/experience                |
| ATS Compatibility  | 15         | Parse-ability, privacy/location penalties, special chars     |

Bonuses (e.g. strong skill validation, error-free grammar) and penalties (e.g. missing JD keywords, location-privacy risks) are applied on top, and the final score is clamped to 0–100.

---

## Tech stack

- **Backend:** FastAPI, Uvicorn, Pydantic
- **NLP/ML:** spaCy (`en_core_web_md`), Sentence-Transformers (`all-MiniLM-L6-v2`), RapidFuzz, NumPy
- **LLM:** Groq API (`llama-3.3-70b-versatile`)
- **Parsing:** pdfplumber, PyPDF2, python-docx, python-magic
- **Reports:** Jinja2 + WeasyPrint
- **Auth/DB:** Supabase (Auth + Postgres via REST), PyJWT
- **Frontend:** Streamlit, Requests

---

## Project structure

```
ATS_checker/
├── backend/
│   ├── main.py                 # FastAPI app + model loading (lifespan)
│   ├── api/
│   │   ├── routes.py           # /api/v1 endpoints
│   │   └── auth.py             # Supabase JWT verification (JWKS / HS256)
│   ├── core/config.py          # Settings, score weights, model names
│   ├── database/supabase_db.py # save / fetch / delete analyses (REST)
│   ├── models/schemas.py       # Pydantic request/response models
│   ├── services/
│   │   ├── resume_parser.py    # File validation + text extraction
│   │   ├── groq_parser.py      # LLM parsing of resume + JD
│   │   ├── resume_analyzer.py  # Orchestrates the full pipeline
│   │   ├── ats_scorer.py       # Scoring + skill/location analysis
│   │   ├── jd_matcher.py       # JD keyword + semantic matching
│   │   ├── feedback_engine.py  # Per-issue detailed feedback
│   │   ├── recommendation_engine.py # Ranked recommendations
│   │   ├── report_generator.py # HTML report rendering
│   │   └── pdf_export.py       # HTML → PDF (WeasyPrint)
│   ├── templates/              # Jinja2 report templates
│   └── requirements.txt
└── frontend/
    ├── streamlit_app.py        # Entry point, routing, auth panel, theming
    ├── views/                  # landing, scorer, history, resources
    ├── components/             # dashboard + result widgets
    ├── services/               # api_client (backend), supabase_client (auth)
    ├── assets/styles.css       # Theme variables
    ├── .streamlit/             # config.toml + secrets.toml (gitignored)
    └── requirements.txt
```

---

## Prerequisites

- **Python 3.12** (the project is developed against 3.12)
- A **Supabase** project (free tier is fine)
- A **Groq API key** (free at <https://console.groq.com>)
- System libraries for two dependencies:
  - **libmagic** (for `python-magic` file-type detection)
  - **Pango/Cairo/GDK-Pixbuf** (for WeasyPrint PDF rendering)

On macOS (Homebrew):

```bash
brew install libmagic pango
```

On Debian/Ubuntu:

```bash
sudo apt-get install libmagic1 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0
```

---

## Setup

### 1. Clone

```bash
git clone https://github.com/nsg365/ATS_checker.git
cd ATS_checker
```

### 2. Create a virtual environment & install dependencies

```bash
python3.12 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt

# Download the spaCy model (falls back to en_core_web_sm if md is missing)
python -m spacy download en_core_web_md
```

### 3. Configure the backend

Create `backend/.env` (gitignored):

```env
GROQ_API_KEY=your_groq_api_key

SUPABASE_URL=https://YOUR-PROJECT-REF.supabase.co
SUPABASE_KEY=your_supabase_anon_public_key
SUPABASE_JWT_SECRET=your_supabase_jwt_secret   # optional if using JWKS via SUPABASE_URL
```

### 4. Configure the frontend

Edit `frontend/.streamlit/secrets.toml` (gitignored):

```toml
[backend]
url = "http://localhost:8000"

[supabase]
SUPABASE_URL = "https://YOUR-PROJECT-REF.supabase.co"
SUPABASE_ANON_KEY = "your_supabase_anon_public_key"

[google_oauth]
redirect_uri = "http://localhost:8501"
```

> The frontend reads environment variables first, then falls back to `st.secrets`.

### 5. Set up Supabase

**a. Create the `analyses` table** (SQL editor):

```sql
create table public.analyses (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users (id),
  filename text,
  ats_score numeric,
  keyword_match numeric,
  missing_keywords jsonb default '[]',
  analysis_result jsonb,
  created_at timestamptz default now()
);

alter table public.analyses enable row level security;

create policy "Users manage their own analyses"
  on public.analyses for all
  using (auth.uid() = user_id)
  with check (auth.uid() = user_id);
```

**b. Enable auth providers:** in Supabase → Authentication → Providers, enable **Email** and (optionally) **Google**. For Google, add `http://localhost:8501` as a redirect URL in both Supabase and the Google Cloud OAuth consent screen.

---

## Running locally

Run both from the **repository root** (the backend uses absolute `backend.*` imports).

**Backend** (terminal 1):

```bash
uvicorn backend.main:app --reload --port 8000
# or: python -m backend.main
```

API docs available at <http://localhost:8000/docs>.

**Frontend** (terminal 2):

```bash
streamlit run frontend/streamlit_app.py
```

Open <http://localhost:8501>, sign in, and analyze a resume.

> First backend start downloads/loads the spaCy and Sentence-Transformer models, so it may take a little longer.

---

## Configuration reference

| Variable                     | Where            | Required | Purpose                                            |
|------------------------------|------------------|:--------:|----------------------------------------------------|
| `GROQ_API_KEY`               | backend          | ✅       | LLM parsing of resume / JD                          |
| `SUPABASE_URL`               | backend+frontend | ✅       | Supabase project URL (also used for JWKS)           |
| `SUPABASE_KEY`               | backend          | ✅       | Supabase anon key (REST apikey for history)         |
| `SUPABASE_ANON_KEY`          | frontend         | ✅       | Supabase anon key (client auth)                     |
| `SUPABASE_JWT_SECRET`        | backend          | ⬜       | Needed only for HS256 token verification            |
| `AUTH_REDIRECT_URL`          | frontend         | ⬜       | Google OAuth redirect (default `localhost:8501`)    |
| `SENTENCE_TRANSFORMER_MODEL` | backend          | ⬜       | Override embedding model (default `all-MiniLM-L6-v2`)|
| `JD_KEYWORD_WEIGHT` / `JD_SEMANTIC_WEIGHT` | backend | ⬜  | Tune JD match weighting                              |

---

## API reference

All endpoints are under `/api/v1` and require a `Authorization: Bearer <supabase_jwt>` header.

| Method | Endpoint                     | Description                                  |
|--------|------------------------------|----------------------------------------------|
| POST   | `/analyze-resume`            | Analyze a resume (PDF/DOCX) + optional JD     |
| GET    | `/history`                   | List the signed-in user's analyses            |
| DELETE | `/history/{id}`              | Delete one analysis                           |
| POST   | `/generate-pdf`              | Generate a PDF report from analysis data      |
| GET    | `/history/{id}/pdf`          | Generate a PDF for a saved analysis           |
| GET    | `/health`                    | Health check (models loaded)                  |

---

## Notes & limitations

- **Uploads:** PDF and DOCX, up to 10 MB. Legacy `.doc` is not supported (convert to `.docx`/PDF). PDFs must contain selectable text (no scanned images).
- **Job descriptions:** paste as text, or upload a `.txt` file.
- **Privacy:** resume text is sent to the Groq API for parsing and stored in your Supabase project; analyses are private to your account and deletable from History.
- **Grammar checks** are currently stubbed (the scoring pipeline uses neutral defaults for grammar).

---

## License

No license specified yet. Add one if you intend to share or open-source this project.
