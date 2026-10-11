# CropGaurd frontend

The frontend is a React application bundled and served in development by Vite. It calls the FastAPI backend through the API client in `src/api.js`.

## Run locally

After installing the backend dependencies, launch Uvicorn from `backend/`:

```powershell
Set-Location C:\CropGaurd\backend
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

In another terminal, install JavaScript dependencies and start Vite:

```powershell
Set-Location C:\CropGaurd\frontend
npm ci
npm run dev
```

Open the local URL printed by Vite, usually `http://localhost:5173`. The development proxy forwards `/api/*` to `http://127.0.0.1:8000/*` and strips the `/api` prefix.

## API configuration

By default, `src/api.js` uses `/api` as its API base. Set `VITE_API_URL` to a different API base URL (without a trailing slash) when the frontend should call an API directly. The Vite development proxy target can be changed by setting `VITE_BACKEND_URL` before running Vite. The API client calls `GET /health` for the status badge and sends `POST /predict` with a multipart `file` field for analysis.

## Upload and result behavior

The upload accepts JPEG, PNG, and WEBP images. The browser checks extension, MIME type, and a 10 MB size limit before submission; this matches the backend default `MAX_IMAGE_SIZE_MB=10`. If that backend setting is changed, keep the frontend's client-side size check aligned. The backend also checks the upload and is authoritative.

The UI includes a keyboard-accessible file picker, drag and drop, preview, loading and error messages, and a checkbox requiring the user to confirm that the image's main subject is a crop leaf. This checkbox is a user attestation, not image recognition. The disease classifier can still produce a confident but incorrect disease result for non-leaf images, and callers that use the API directly do not encounter the frontend confirmation.

Prediction results display the model's individual plant severity separately from the catalog's typical disease severity. Unknown individual severity is shown as “Not assessed”; catalog guidance is shown when the backend returns `disease_info`.

## Checks

Run from `frontend/`:

```powershell
npm run test
npm run lint
npm run build
```
