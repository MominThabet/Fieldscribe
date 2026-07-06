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

## Phase 1 — hardcoded extraction script

A sample invoice PDF is included at `backend/sample_data/sample_invoice.pdf`
so you can test immediately without needing your own document yet.

```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt        # picks up the new pdfplumber dependency
python scripts/extract.py sample_data/sample_invoice.pdf
```

Expected output: a JSON object with `sender_name`, `date`, and `total_amount`
pulled out of the sample invoice.

Once that works, try it against a real PDF of your own (any text-based PDF —
scanned/image PDFs need OCR, which comes later). If the fields don't match
your real-world document (e.g. it's not an invoice), that's fine for now —
Phase 2 makes the field list dynamic instead of hardcoded.
