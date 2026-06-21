# Claude PR Reviewer Dashboard

A live metrics dashboard for [claude-pr-reviewer](https://github.com/esingh25/claude-pr-reviewer) —
an AI-powered GitHub/GitLab/Bitbucket pull request reviewer built with Claude. This is a portfolio
project demonstrating a full-stack app: FastAPI + Postgres backend, Next.js frontend, deployed
free on Vercel + Neon.

## Architecture

```
backend/    FastAPI + SQLAlchemy, deployed as Vercel Python serverless functions
  app/
    main.py            FastAPI app, CORS
    database.py         SQLAlchemy engine (Postgres in prod, SQLite for local dev)
    models.py            ReviewRun ORM model
    schemas.py            Pydantic request/response models
    auth.py               API-key dependency for the write endpoint
    routes_metrics.py      POST /api/metrics (write, API-key protected)
                            GET /api/metrics, /api/metrics/summary (public read)
  api/index.py          Vercel entrypoint (re-exports the FastAPI app)

frontend/   Next.js (App Router) + Tailwind + Recharts, deployed on Vercel
  src/app/page.tsx       Dashboard: stat cards, severity chart, trend chart, recent runs table
  src/lib/api.ts          Server-side fetch helpers
```

Data flow: `claude-pr-reviewer` (running locally or in CI) optionally POSTs each review run's
metrics to this backend (opt-in, via `DASHBOARD_URL`/`DASHBOARD_API_KEY` env vars on that repo) →
stored in Postgres → the frontend fetches and charts it on every page load (no caching, always
fresh).

## Local development

**Backend:**
```bash
cd backend
python -m venv .venv && .venv/Scripts/activate   # .venv/bin/activate on macOS/Linux
pip install -r requirements-dev.txt
INGEST_API_KEY=devkey uvicorn app.main:app --reload --port 8000
pytest   # 9 tests, no DB setup needed (uses a temp SQLite file)
```
With no `DATABASE_URL` set, it uses a local `dev.db` SQLite file automatically.

**Frontend:**
```bash
cd frontend
npm install
API_BASE_URL=http://localhost:8000 npm run dev
```

## Deployment (free tier, no cost)

### 1. Database — Neon
1. Sign up at [neon.tech](https://neon.tech), create a project.
2. Copy the connection string (starts with `postgresql://`).

### 2. Backend — Vercel
1. Push this repo to GitHub.
2. In Vercel, "Add New Project" → import this repo → set **Root Directory** to `backend`.
3. Environment variables: `DATABASE_URL` (from Neon), `INGEST_API_KEY` (generate any random
   string — this is the secret `claude-pr-reviewer` will use to POST data), `ALLOWED_ORIGINS`
   (the frontend's Vercel URL, set after step 3 — update and redeploy).
4. Deploy. Note the resulting URL (e.g. `https://your-backend.vercel.app`).

### 3. Frontend — Vercel
1. "Add New Project" again → same repo → **Root Directory** set to `frontend`.
2. Environment variable: `API_BASE_URL` = the backend URL from step 2.
3. Deploy. This is the public dashboard URL.
4. Go back to the backend project's `ALLOWED_ORIGINS` and set it to this frontend URL, redeploy.

### 4. Wire up claude-pr-reviewer to send real data
In whichever repo/workflow runs `claude-pr-reviewer` (or when running the CLI locally), set:
```
DASHBOARD_URL=https://your-backend.vercel.app
DASHBOARD_API_KEY=<the INGEST_API_KEY you generated above>
```
Every review run will then POST its metrics here automatically (best-effort — a dashboard outage
never fails the actual PR review).

## License

[MIT](LICENSE)
