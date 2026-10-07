# AI Crop Disease Detection - Backend API

FastAPI-based backend service for deep learning crop disease detection from leaf images.

## Features Implemented

* **FastAPI Core**: Modular architecture with versioned API structure, asynchronous lifespan connection management, and automatic interactive Swagger documentation.
* **CORS Support**: Configured for cross-origin requests from frontend clients (React/Vite).
* **Database Layer (MongoDB & Motor)**:
  * Asynchronous MongoDB connection pool with connection retry and graceful offline fallback.
  * Auto-indexing on `predictions` (timestamp and user), `users` (unique email), and `diseases` (slug and crop).
  * Storage optimization: saves technical metadata and image references without bloating MongoDB with binary image blobs.
* **Phase 2 Image Validation & Inspection**:
  * Allowed extensions (`.jpg`, `.jpeg`, `.png`, `.webp`)
  * MIME type validation (`image/jpeg`, `image/png`, `image/webp`)
  * File size limits (default: 10MB)
  * Pillow verification to detect corrupted byte streams
  * Extraction of image metadata (dimensions, format, color mode, channels, byte size)
  * Clean HTTP error codes (`400 Bad Request`, `413 Payload Too Large`, `415 Unsupported Media Type`)
* **Phase 5 & 9 Disease Knowledge Base & Contract Simulation**:
  * Full prediction response contract returning crop diagnosis, confidence, severity, and health status.
  * Clinical enrichment: symptoms, causes, prevention, and chemical/organic management guidelines.
  * Dedicated disease catalog endpoints with optional crop filtering (`/diseases?crop=Tomato`).
* **Phase 6 & 8 Scan History & Persistence**:
  * Prediction scans are automatically persisted into database.
  * History endpoints to query past scans (`GET /history`), view details (`GET /history/{id}`), or delete records (`DELETE /history/{id}`).
* **Automated Test Suite**: 17 unit and integration tests passing (`pytest` and `httpx`).

---

## Project Structure

```text
backend/
├── app/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py            # App settings & environment variables
│   │   └── database.py          # MongoDB async lifecycle & index manager
│   ├── models/
│   │   ├── __init__.py
│   │   ├── prediction.py        # MongoDB prediction document schema
│   │   ├── user.py              # MongoDB user document schema (Phase 7 prep)
│   │   └── disease.py           # MongoDB disease document schema
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── prediction.py        # /predict route handlers
│   │   ├── diseases.py          # /diseases catalog route handlers
│   │   └── history.py           # /history scan history route handlers
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── disease.py           # Disease catalog Pydantic schemas
│   │   ├── history.py           # Scan history Pydantic schemas
│   │   └── prediction.py        # Prediction request/response Pydantic models
│   ├── services/
│   │   ├── __init__.py
│   │   ├── disease_service.py   # Curated crop disease knowledge repository
│   │   ├── history_service.py   # Scan persistence and retrieval service
│   │   ├── predictor.py         # Inference abstraction & clinical enrichment
│   │   └── image_processor.py   # Validation, inspection & preprocessing service
│   ├── __init__.py
│   └── main.py                  # FastAPI application entrypoint & lifespan
├── tests/
│   ├── __init__.py
│   ├── test_prediction.py       # Validation and prediction test cases
│   ├── test_diseases.py         # Disease catalog query test cases
│   └── test_history.py          # Database scan history test cases
├── .env.example                 # Environment variables template
├── .env                         # Local environment settings (ignored by Git)
├── .gitignore                   # Ignore rules for venv, cache, models, secrets
├── requirements.txt             # Python dependencies
└── README.md
```

---

## Getting Started

### 1. Prerequisites

* Python 3.10+ (Python 3.11 recommended)
* MongoDB (Local `mongod` or MongoDB Atlas URI)
* Git

### 2. Environment Setup

From the `backend/` directory:

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create `.env` from `.env.example`:

```bash
# Windows PowerShell
Copy-Item .env.example .env

# Linux / macOS
cp .env.example .env
```

Configure MongoDB settings in `.env`:
```env
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=crop_disease_db
```
*(If MongoDB is not running, the application will automatically fall back to an in-memory buffer without crashing).*

### 4. Run the Development Server

From the `backend/` directory:

```bash
uvicorn app.main:app --reload --port 8000
```

Open your browser to:
* **API Documentation (Swagger UI)**: [http://localhost:8000/docs](http://localhost:8000/docs)
* **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
* **Health Check**: [http://localhost:8000/health](http://localhost:8000/health)

---

## Running Automated Tests

Run the test suite from the `backend/` directory:

```bash
pytest tests/ -v
```

---

## API Endpoints

| Method | Endpoint | Description | Status Codes |
|---|---|---|---|
| `GET` | `/` | Root service info (shows DB status) | `200` |
| `GET` | `/health` | Uptime health check & DB status | `200` |
| `POST` | `/predict` | Leaf upload, disease detection, & DB persistence | `200`, `400`, `413`, `415` |
| `GET` | `/history` | List previous prediction scans (paginated) | `200` |
| `GET` | `/history/{id}` | Get single historical scan detail | `200`, `404` |
| `DELETE` | `/history/{id}` | Remove a scan record from history | `200`, `404` |
| `GET` | `/diseases` | List cataloged diseases (supports `?crop=CropName`) | `200` |
| `GET` | `/diseases/{id}` | Get clinical details, causes, symptoms, and treatment | `200`, `404` |
