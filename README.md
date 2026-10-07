# CropGuard crop disease detection

This project contains both applications in one folder: the FastAPI backend in `backend/` and the React/Vite frontend in `frontend/`.

## Run both locally

Start the backend in PowerShell:

```powershell
..\.venv\Scripts\python.exe -m uvicorn app.main:app --app-dir backend --reload --port 8000
```

In a second terminal, start the frontend:

```powershell
Set-Location .\frontend
npm run dev
```

Open the local URL printed by Vite (usually `http://localhost:5173`). Vite proxies `/api` requests to the backend on port 8000. The frontend health indicator checks `/health`; image analysis uploads the selected file to `/predict` and displays the returned prediction and disease guidance.

See [backend/README.md](backend/README.md) and [frontend/README.md](frontend/README.md) for setup details. The backend currently returns a contract simulation prediction until a trained model is configured.
