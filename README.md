# SafeRide Airport Taxis (website)

FastAPI backend + React (Vite) frontend in one repo, deployed as ONE service.
FastAPI serves the API under `/api/*` and also serves the built React app for every other URL.

## Folder layout
```
car247/
├── backend/
│   ├── config.py      # reads every setting from env vars / .env
│   ├── main.py        # API routes + serves React build
│   └── content.py     # site text (vehicles, locations, blog...); brand details come from env
├── frontend/
│   ├── src/
│   │   ├── components/  # Header, Footer, QuoteForm, ContactForm...
│   │   ├── pages/       # Home, Book, Vehicles, Airport, Location, Blog...
│   │   └── styles.css   # colours and fonts at the top
│   └── public/          # put images/logo here, use them as /logo.png
├── .env.example       # every setting, copy to .env (run.bat does it for you)
├── run.bat            # one-click local run on Windows
├── requirements.txt
├── build.sh           # Render build step
└── render.yaml
```

## Run locally (Windows)

Double-click `run.bat` (or run it from a terminal). On first run it:
1. creates `.env` from `.env.example` if it is missing,
2. creates a Python virtual env in `.venv` and installs `requirements.txt` (again only when that file changes),
3. runs `npm install` in `frontend/` if `node_modules` is missing,
4. opens two windows: FastAPI (`API_PORT`, default 8000) and Vite (`FRONTEND_PORT`, default 5173), then opens the site in your browser.

`run.bat prod` builds React and serves everything from FastAPI, like on Render.

All settings (ports, admin key, CORS, brand name, phone, email, address, links) live in `.env`.
Both the backend (`backend/config.py`) and Vite (`frontend/vite.config.js`) read the same file. Never commit `.env`.

## Deploy on Render
1. Push this folder to GitHub.
2. On Render: New > Blueprint, pick the repo (it reads `render.yaml`).
   Or New > Web Service with:
   - Runtime: Python
   - Build command: `./build.sh`
   - Start command: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
3. Set the same variables as in `.env.example` under Environment (leave `CORS_ORIGINS` empty, `ENABLE_API_DOCS=false`).
4. Done. Frontend and API live on the same URL.

## API
| Method | Path | What it does |
|---|---|---|
| GET | /api/health | health check |
| GET | /api/site | all site content |
| POST | /api/quotes | quote/booking request |
| POST | /api/messages | contact, business and driver forms |
| GET | /api/quotes, /api/messages | view submissions (needs `x-admin-key` header = ADMIN_KEY env var) |

API docs: /docs (only when `ENABLE_API_DOCS=true`)

## Notes
- Submissions are stored in memory and are lost on restart. Add Postgres (or send an email) when you need to keep them.
- Brand details are in `.env`. To edit other content, change `backend/content.py`. To change colours, edit the variables at the top of `styles.css`.
