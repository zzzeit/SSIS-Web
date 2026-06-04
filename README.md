#  SSIS-Web

A two-tier web application: a Next.js frontend and a Flask backend. The frontend is a React/Next app that can use Supabase for client-side features; the backend is a Flask API that serves the built frontend from `backend/static` and connects to a PostgreSQL database.

## Technologies

- **Backend:** Python 3.13, Flask, psycopg2, Flask-Bcrypt, Flask-JWT-Extended, Pipenv
- **Frontend:** Next.js 15.5.3, React 19.1.0, Tailwind/PostCSS, @supabase/supabase-js, lottie-react
- **Dev tooling:** Node/npm, Pipenv, PowerShell build script (`build-frontend.ps1`), ESLint

## Setup

### Prerequisites

- Install Python 3.13 and Pipenv
- Install Node.js and npm
- Have a PostgreSQL database available and a `DATABASE_URL`

### Environment files

- **Backend:** copy `backend/env` to `backend/.env` and fill all 9 variables:
- **Frontend:** copy `frontend/env copy.local` to `frontend/.env.local` and fill `NEXT_PUBLIC_SUPABASE_URL` and `NEXT_PUBLIC_SUPABASE_ANON_KEY`

## Run (development)

- Backend (from repo root):
```powershell
cd backend
pipenv install
# create backend/.env with DATABASE_URL and JWT_SECRET_KEY
pipenv run python app.py
```

- Frontend (from repo root):
```powershell
cd frontend
npm install
# create frontend/.env.local from env copy.local
npm run dev
```

The frontend dev server runs (default port 3000) and expects the API at `NEXT_PUBLIC_API_URL` (default `http://localhost:5000`). The Flask backend listens on `BACKEND_HOST`/`BACKEND_PORT` (defaults: `localhost:5000`).

## Build (production)

From the repository root run the PowerShell build script which builds the Next app and copies the static output into the backend:

```powershell
.\build-frontend.ps1
```

That script runs `npm run build` in `frontend`, copies `.next` to `backend/static/.next`, and copies `frontend/public` to `backend/static/media`.

Then start the backend (ensure `backend/.env` has production `DATABASE_URL` and `JWT_SECRET_KEY`):

```powershell
cd backend
pipenv install --deploy --ignore-pipfile
pipenv run python app.py
```

#### Notes

- The backend serves the built frontend from `backend/static`.