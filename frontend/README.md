# CropGuard frontend

React and Vite frontend for the FastAPI crop disease detection backend.

## Run the application locally

1. From the project root, start the backend:

   ```powershell
   .\.venv\Scripts\python.exe -m uvicorn app.main:app --app-dir backend --reload --port 8000
   ```

   If the project virtual environment is not installed, install the packages from the repository's `requirements.txt` first.

2. In a second terminal, start the frontend:

   ```powershell
   Set-Location .\frontend
   npm install
   npm run dev
   ```

3. Open the Vite URL shown in the terminal (usually `http://localhost:5173`). Vite forwards `/api/*` requests to `http://127.0.0.1:8000/*`.

The frontend checks `/health` and sends uploaded leaf images as multipart form data to `/predict`. To point it at a different API, create a `.env.local` file with `VITE_API_URL=https://your-api-host` (the value should not end in a slash). For local proxying to another backend port, set `VITE_BACKEND_URL` before starting Vite.

The backend currently runs in contract simulation mode until a trained model is configured, so its prediction is a development placeholder.
