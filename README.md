# CodeAtlas — Open Source Mentor

> **From first visit to first PR in minutes.**
> A repository onboarding & contribution intelligence platform powered by [Cognee](https://www.cognee.ai).

---

## What is CodeAtlas?

CodeAtlas ingests a GitHub repository's entire history — README, Issues, PRs, Discussions, Contributors — into a **Cognee knowledge graph**, then surfaces AI-driven mentoring to help developers go from newcomers to contributors.

### 9 AI-Powered Features

| # | Feature | Description |
|---|---------|-------------|
| 1 | **Onboarding Guide** | Step-by-step guide covering project purpose, culture, key maintainers, and reading path |
| 2 | **Find My First Issue** | AI-matched issues based on your experience level and interests |
| 3 | **Contribution Assistant** | Detailed contribution plan for any issue with maintainer expectations |
| 4 | **Maintainer Brain** | Review patterns, preferences, DO/DON'T lists from actual maintainer behavior |
| 5 | **Decision Explorer** | Trace WHY decisions were made through discussions, PRs, and reviews |
| 6 | **Repository Q&A** | Ask anything — answers backed by real issues, PRs, and discussions |
| 7 | **Knowledge Graph** | Interactive React Flow visualization of entities and relationships |
| 8 | **Project Timeline** | Chronological evolution of features, decisions, and milestones |
| 9 | **Learning Path** | Personalized learning path based on the repo's tech stack and your goals |

### Cognee Memory Lifecycle

CodeAtlas uses all four Cognee lifecycle operations:
- **Remember** — Ingest repository data into the knowledge graph
- **Recall** — Query the knowledge graph for context
- **Improve** — Feed user feedback back to improve retrieval
- **Forget** — Delete repository memory on demand

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                 MONOREPO: codeatlas/                     │
│                                                         │
│  ┌─────────────────────┐    ┌────────────────────────┐  │
│  │   frontend/          │    │   backend/              │  │
│  │   Next.js 16         │    │   FastAPI + Python      │  │
│  │   TypeScript         │    │   Cognee SDK            │  │
│  │   TailwindCSS        │    │   PyGithub              │  │
│  │   React Flow         │    │   httpx (GraphQL)       │  │
│  │   TanStack Query     │    │   SQLAlchemy (async)    │  │
│  │   Framer Motion      │    │   Alembic               │  │
│  └────────┬────────────┘    └──────────┬─────────────┘  │
│           │                            │                 │
│           │      REST API calls        │                 │
│           └────────────────────────────┘                 │
│                        │                                 │
│              ┌─────────┴──────────┐                      │
│              │                    │                       │
│        ┌─────▼─────┐     ┌───────▼──────┐               │
│        │ PostgreSQL │     │ Cognee Cloud │               │
│        │ (metadata) │     │ (knowledge   │               │
│        │            │     │  graph +     │               │
│        │ Users      │     │  memory)     │               │
│        │ Repos      │     │              │               │
│        │ Jobs       │     │ Entities     │               │
│        │ Feedback   │     │ Relations    │               │
│        └────────────┘     │ Vectors      │               │
│                           └──────────────┘               │
└─────────────────────────────────────────────────────────┘
```

---

## Prerequisites

- **Node.js** ≥ 18
- **Python** ≥ 3.11
- **PostgreSQL** (local or hosted)
- **API Keys**:
  - Cognee Cloud — `COGNEE_API_URL` + `COGNEE_API_KEY` ([platform.cognee.ai](https://platform.cognee.ai))
  - GitHub Personal Access Token — `GITHUB_TOKEN` (scopes: `repo`, `read:discussion`)
  - OpenAI or Gemini API key — for LLM features

---

## Quick Start

### 1. Clone & Setup Backend

```bash
cd codeatlas/backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your credentials

# Run database migrations (or let dev mode auto-create tables)
alembic upgrade head

# Start the backend
uvicorn app.main:app --reload --port 8000
```

### 2. Setup Frontend

```bash
cd codeatlas/frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env.local
# Edit .env.local if backend is not on localhost:8000

# Start dev server
npm run dev
```

### 3. Open the App

Visit **http://localhost:3000**, paste a GitHub repo URL, and start exploring!

---

## Environment Variables

### Backend (`backend/.env`)

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DATABASE_URL` | ✅ | `postgresql+asyncpg://...` | PostgreSQL connection string |
| `COGNEE_API_URL` | ✅ | — | Cognee Cloud tenant URL |
| `COGNEE_API_KEY` | ✅ | — | Cognee Cloud API key |
| `GITHUB_TOKEN` | ✅ | — | GitHub PAT for API access |
| `LLM_PROVIDER` | ✅ | `openai` | `openai` or `gemini` |
| `OPENAI_API_KEY` | ⚡ | — | Required if `LLM_PROVIDER=openai` |
| `GEMINI_API_KEY` | ⚡ | — | Required if `LLM_PROVIDER=gemini` |
| `JWT_SECRET_KEY` | ✅ | `change-this` | JWT signing secret |
| `FRONTEND_URL` | — | `http://localhost:3000` | CORS allowed origin |
| `MAX_ISSUES` | — | `500` | Max issues to ingest per repo |
| `MAX_PRS` | — | `200` | Max PRs to ingest per repo |
| `MAX_DISCUSSIONS` | — | `200` | Max discussions to ingest |

### Frontend (`frontend/.env.local`)

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `NEXT_PUBLIC_API_URL` | — | `http://localhost:8000` | Backend API URL |

---

## API Endpoints

### Repositories
| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/repositories/` | Add a repo (fetches GitHub metadata) |
| `GET` | `/api/repositories/` | List all repos |
| `GET` | `/api/repositories/{id}` | Get repo details |
| `GET` | `/api/repositories/{id}/dashboard` | Dashboard data with memory stats |
| `DELETE` | `/api/repositories/{id}` | Delete repo + Cognee memory |

### Ingestion
| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/repositories/{id}/ingest` | Start ingestion pipeline |
| `GET` | `/api/repositories/{id}/ingestion-status` | Poll ingestion status |
| `GET` | `/api/repositories/{id}/ingestion-stream` | SSE real-time progress |
| `DELETE` | `/api/repositories/{id}/memory` | Forget all memory (Cognee) |

### AI Mentor Features
| Method | Path | Feature |
|--------|------|---------|
| `GET` | `/api/repositories/{id}/onboarding` | 1. Onboarding Guide |
| `POST` | `/api/repositories/{id}/find-first-issue` | 2. Find My First Issue |
| `POST` | `/api/repositories/{id}/analyze-issue` | 3. Contribution Assistant |
| `GET` | `/api/repositories/{id}/maintainer-brain` | 4. Maintainer Brain |
| `POST` | `/api/repositories/{id}/explore-decision` | 5. Decision Explorer |
| `POST` | `/api/repositories/{id}/ask` | 6. Repository Q&A |
| `GET` | `/api/repositories/{id}/graph` | 7. Knowledge Graph |
| `GET` | `/api/repositories/{id}/timeline` | 8. Timeline |
| `POST` | `/api/repositories/{id}/learning-path` | 9. Learning Path |

### Feedback
| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/repositories/{id}/feedback` | Submit 👍/👎 feedback |
| `GET` | `/api/repositories/{id}/feedback` | List feedback |

---

## Tech Stack

**Frontend**: Next.js 16, React 19, TypeScript, TailwindCSS 4, React Flow, TanStack Query, Framer Motion, Zustand, Lucide Icons

**Backend**: FastAPI, Python 3.11+, SQLAlchemy 2 (async), Alembic, Cognee SDK, PyGithub, httpx, OpenAI / Google GenAI, Pydantic v2

**Data**: PostgreSQL (metadata), Cognee Cloud (knowledge graph + vectors)

---

## License

MIT
