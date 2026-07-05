# Fieldscribe — Phase 0 starter

Minimal skeleton to confirm frontend and backend can talk to each other.

## Backend setup

```bash
cd backend
python -m venv venv
source venv/bin/activate   # on Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env       # then paste your Anthropic API key into .env
uvicorn app.main:app --reload
```

Backend runs at http://localhost:8000 — visit http://localhost:8000/ping to confirm.

## Frontend setup

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at http://localhost:5173. Click "Ping backend" — you should see
"backend is alive" appear on the page.

## Checkpoint for Phase 0

If clicking the button shows the success message, both halves are wired up
correctly and you're ready for Phase 1 (hardcoded PDF extraction script).
