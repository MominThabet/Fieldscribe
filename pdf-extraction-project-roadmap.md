# PDF Data Extraction Project — Build Roadmap

**Goal:** users upload PDFs, define their own extraction fields, get structured data back, save it to a database, and export it to Excel.

**Repo structure:** one repo, two folders.
```
project-root/
  backend/   (FastAPI, Python)
  frontend/  (React)
```
Auth and deployment are deferred to the end, as agreed.

---

## Phase 0 — Environment setup
**Goal:** everything runs locally before you write real logic.

- Set up `backend/` with a virtualenv, FastAPI, uvicorn
- Set up `frontend/` with a basic React app (Vite is fastest to start)
- Confirm frontend can hit a "hello world" backend endpoint (CORS configured)
- Get an Anthropic API key working with a simple test script

**Checkpoint:** `curl localhost:8000/ping` works, and a button in the React app can call it and show the response.

---

## Phase 1 — Hardcoded extraction (prove the core idea works)
**Goal:** one fixed extraction, no dynamic fields yet, no UI yet. Just a script.

- Extract raw text from a PDF (start with text-based PDFs, not scanned)
- Send that text + a **fixed** list of fields (e.g. name, date, total) to the LLM
- Use structured output / tool-use so the response is guaranteed valid JSON
- Print the JSON to console

**Skills:** PDF text extraction, prompt construction, structured LLM output.

**Checkpoint:** running `python extract.py sample.pdf` prints clean JSON with your 3 hardcoded fields.

---

## Phase 2 — Dynamic fields (the core differentiator)
**Goal:** the field list comes from the caller, not hardcoded.

- Turn the script into a FastAPI endpoint: `POST /extract`
  - Request body: PDF file + a list of `{name, type, description}` field definitions
- Backend builds the JSON schema / tool definition **at runtime** from that list
- Same structured-output call as Phase 1, just schema built dynamically
- Handle the case where a field isn't found in the document (return null, don't hallucinate)

**Skills:** dynamic schema generation, API design, defensive prompting.

**Checkpoint:** you can call the API with two totally different field lists (e.g. invoice fields vs resume fields) against two different PDFs, and get back correctly-shaped JSON both times, with zero code changes between calls.

---

## Phase 3 — Storage: database + Excel
**Goal:** persist results, don't just print them.

- Add a database (start with SQLite — zero setup — move to Postgres later if you want)
- Tables: `extractions` (the results), `templates` (saved field-definition sets)
- `POST /extract` now also writes the result to the DB
- Add `GET /export` — pulls records from DB, builds an Excel file with pandas + openpyxl, returns it as a download

**Skills:** basic schema design, ORM or raw SQL, pandas/openpyxl.

**Checkpoint:** extract a few PDFs, then download an Excel file containing all of them as rows.

---

## Phase 4 — Frontend: the actual web app
**Goal:** replace curl/Postman with a real UI.

- Upload page: drag-and-drop or file picker for PDFs
- Schema builder: a form to add/remove fields (name, type, description) before extracting
- Results view: table showing extracted records, with an "Export to Excel" button
- Wire it all to the backend endpoints from Phases 2–3

**Skills:** React state management, forms, file upload handling, calling a backend API from the frontend.

**Checkpoint:** you can do the entire flow — upload PDF, define fields in the browser, see results in a table, download Excel — without touching the terminal.

---

## Phase 5 — Templates (reuse field sets)
**Goal:** don't make the user redefine fields every time.

- "Save this field set as a template" button, named by the user (e.g. "Invoice fields")
- Template picker on the upload page — load a saved template instead of building fields from scratch
- CRUD endpoints for templates (`GET/POST/DELETE /templates`)

**Skills:** basic CRUD, UI state for select/reuse patterns.

**Checkpoint:** create a template once, reuse it across 5 different PDF uploads.

---

## Phase 6 — Analysis features (polish)
**Goal:** make the stored data actually useful, not just a pile of rows.

- Simple aggregate view: counts, sums, trends across saved extractions (e.g. total spend if it's invoices)
- Basic charting on the frontend (a bar/line chart of numeric fields over time)
- Optional: filtering/search over past extractions

**Skills:** basic data analysis, simple charting library integration.

**Checkpoint:** a dashboard-ish view showing something meaningful about the data you've accumulated.

---

## Phase 7 — Deferred (do later, once the above is solid)
- Auth (so it's multi-user, not just you)
- Dockerize backend + frontend
- Deploy (e.g. Railway/Fly.io for backend, Vercel for frontend)
- Handle scanned/image PDFs via OCR
- Background job queue if PDFs get large or numerous

---

## Suggested order of attack
Phases 0 → 1 → 2 are the meat of the "AI engineering" learning — don't rush them.
Phase 3 → 4 → 5 turn it into a real product.
Phase 6 → 7 are genuinely optional polish; stop earlier if you're short on time and still have a strong portfolio piece.
