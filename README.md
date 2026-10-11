# CropGaurd

CropGaurd is a local web application for classifying crop leaf images with a trained MobileNetV2 model. The FastAPI backend validates image uploads, runs inference, maps the model label to a crop and disease, and returns matching care information from a static catalog. A React and Vite frontend lets a user upload an image and review the result.

The classifier has 15 output classes for pepper, potato, and tomato; their names follow PlantVillage label conventions. Saved evaluation metrics are strong, but do not establish performance on field photographs. This is a classification aid, not a confirmed diagnosis.

## Features

- MobileNetV2 inference using the checked-in checkpoint and inference configuration.
- JPEG, PNG, and WEBP upload validation, image integrity checking, and metadata extraction.
- Disease information lookup for all 15 model classes, including healthy classes.
- Disease catalog browsing and scan history endpoints.
- Responsive upload and results interface, with file-type and size checks and a leaf-image confirmation prompt.
- Optional MongoDB persistence; the application can run with an in-memory history fallback when MongoDB is unavailable.

## Project layout

```text
CropGaurd/
├── backend/
│   ├── app/                 # FastAPI routes, schemas, settings, and services
│   ├── tests/               # Backend tests
│   └── .env.example         # Backend configuration template
├── frontend/
│   ├── src/                 # React application and API client
│   └── test/                # Frontend unit tests
├── ml/
│   ├── src/predict.py       # PyTorch model loading and inference
│   └── artifacts/           # Checkpoint, class labels, preprocessing, and metrics
├── requirements.txt         # Python dependencies
└── package.json             # Root shortcuts for frontend dev/build/lint/preview
```

## Requirements

- Python 3.10 or newer and a PyTorch/Torchvision build compatible with your Python and hardware. The current project environment has been run with Python 3.13.
- Node.js and npm (the current frontend environment uses Node 22).
- MongoDB is optional. Without a reachable MongoDB server, prediction history is kept in process memory and is lost when the backend stops.

## Run locally on Windows PowerShell

From the repository root, create and populate the backend virtual environment:

```powershell
Set-Location C:\CropGaurd
py -3.13 -m venv .\backend\.venv
.\backend\.venv\Scripts\python.exe -m pip install --upgrade pip
.\backend\.venv\Scripts\python.exe -m pip install -r .\requirements.txt
if (-not (Test-Path .\backend\.env)) { Copy-Item .\backend\.env.example .\backend\.env }
```

The copy command is for initial setup. If `backend\.env` already exists, keep it and update its values as needed. Without MongoDB variables, the backend defaults to `mongodb://localhost:27017`; connection failure is handled by the in-memory history fallback.

Start the backend in one terminal. Run Uvicorn from the `backend` directory so `backend/.env` is loaded:

```powershell
Set-Location C:\CropGaurd\backend
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

Start the frontend in a second terminal:

```powershell
Set-Location C:\CropGaurd\frontend
npm ci
npm run dev
```

Open the Vite URL printed in the terminal, normally `http://localhost:5173`. Vite proxies `/api` to `http://127.0.0.1:8000` and removes the `/api` prefix. The frontend health badge requests `/health`; analysis sends multipart field `file` to `/predict`.

For a different backend target, set `VITE_BACKEND_URL` in the environment before launching Vite. For a frontend that calls an API directly, set `VITE_API_URL` to the API base URL (without a trailing slash); otherwise the client uses `/api`.

## Configuration

Backend settings are loaded from `backend/.env` when the server runs with `backend/` as its working directory. The supported values include:

| Variable | Default | Purpose |
|---|---|---|
| `PROJECT_NAME` | `AI Crop Disease Detection API` | API title |
| `ALLOWED_ORIGINS` | localhost ports 3000 and 5173 | Comma-separated CORS origins |
| `MONGODB_URL` | `mongodb://localhost:27017` | MongoDB connection string; `MONGODB_URI` is also accepted |
| `DATABASE_NAME` | `crop_disease_db` | Database name; `MONGODB_DB_NAME` is also accepted |
| `MAX_IMAGE_SIZE_MB` | `10` | Backend upload size limit |
| `ALLOWED_IMAGE_EXTENSIONS` | `.jpg,.jpeg,.png,.webp` | Accepted filename suffixes |
| `ALLOWED_IMAGE_MIME_TYPES` | `image/jpeg,image/png,image/webp` | Accepted declared MIME types |

`HOST`, `PORT`, and `DEBUG` appear in the example file but are not used to configure the application server; pass host/port options to Uvicorn. The commented MongoDB and JWT lines in `.env.example` are marked as planned settings, not active JWT functionality.

## Prediction flow and API

The backend loads the checkpoint at startup. Missing or invalid model artifacts prevent startup rather than returning a placeholder prediction. The endpoint accepts an image upload, checks its extension, declared content type, size, and decodability, then runs the saved model and resolves the result through the disease catalog.

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/` | API name, version, online status, and database connection status |
| `GET` | `/health` | Health and database connection status |
| `POST` | `/predict` | Classify a multipart image upload with field `file`; `/predict/` is also accepted |
| `GET` | `/diseases?crop=Tomato` | List the static catalog, optionally filtered by crop |
| `GET` | `/diseases/{id}` | Get a catalog entry by ID |
| `GET` | `/history?limit=20&skip=0` | List recent prediction records |
| `GET` | `/history/{id}` | Get a prediction record |
| `DELETE` | `/history/{id}` | Delete a prediction record |

Interactive API documentation is available at `/docs`; ReDoc is at `/redoc`.

The prediction response has `id`, `success`, `message`, `image_metadata`, `prediction`, and nullable `disease_info`. `prediction` contains crop, disease, model confidence, severity, and `is_healthy`. `disease_info` contains the catalog ID, scientific name when known, typical disease severity, symptoms, causes, prevention, and management guidance.

The model confidence is a softmax score, not calibrated diagnostic certainty. For diseased predictions, individual plant severity is `Unknown`; for healthy predictions it is `None`. A catalog entry's severity is a typical disease-level category and is not an assessment of the uploaded plant.

Image validation confirms that the upload is a supported, decodable image; it does not determine whether the image depicts a crop leaf. The frontend asks the user to confirm that the image's main subject is a crop leaf. This is only a user confirmation and can be bypassed by direct API callers. Reliable automated leaf/non-leaf screening requires a separately evaluated validation model or equivalent classifier.

## Model and evaluation

The backend uses `ml/src/predict.py` and these artifacts:

- `ml/artifacts/mobilenetv2_best.pth` — saved model checkpoint.
- `ml/artifacts/class_names.json` — output class order (15 labels).
- `ml/artifacts/preprocessing.json` — model architecture and preprocessing configuration.
- `ml/artifacts/metrics.json` and `ml/artifacts/test_classification_report.csv` — saved evaluation results.

Inference uses MobileNetV2 with the saved state dictionary, RGB input resized to 224 × 224, and channel normalization with means `[0.485, 0.456, 0.406]` and standard deviations `[0.229, 0.224, 0.225]`. The inference constructor initializes the architecture without downloading pretrained weights (`weights=None`) before loading the project checkpoint. The available project files do not establish how the checkpoint was initialized during training.

The saved `metrics.json` reports the following on 3,094 test samples:

| Metric | Saved result |
|---|---:|
| Accuracy | 99.00% |
| Macro F1 | 98.79% |
| Weighted F1 | 99.00% |

These are dataset test metrics, not expected accuracy for arbitrary camera or field images. Field-image performance, calibration, and leaf/non-leaf rejection need separate evaluation.

Project notes have described this as a held-out PlantVillage test split, but `metrics.json` and the available inference source do not record the dataset provenance or split procedure. Treat PlantVillage as project-reported provenance until the training data and evaluation procedure can be verified.

### Model labels

The names below are read from `ml/artifacts/class_names.json`:

- Pepper: `Pepper__bell___Bacterial_spot`, `Pepper__bell___healthy`
- Potato: `Potato___Early_blight`, `Potato___Late_blight`, `Potato___healthy`
- Tomato: `Tomato_Bacterial_spot`, `Tomato_Early_blight`, `Tomato_Late_blight`, `Tomato_Leaf_Mold`, `Tomato_Septoria_leaf_spot`, `Tomato_Spider_mites_Two_spotted_spider_mite`, `Tomato__Target_Spot`, `Tomato__Tomato_YellowLeaf__Curl_Virus`, `Tomato__Tomato_mosaic_virus`, `Tomato_healthy`

## Tests and checks

Backend tests run from `backend/` with the project virtual environment:

```powershell
Set-Location C:\CropGaurd\backend
.\.venv\Scripts\python.exe -m pytest -q
```

Frontend checks run from `frontend/`:

```powershell
npm run test
npm run lint
npm run build
```

The root `package.json` provides shortcuts for `npm run dev`, `npm run build`, `npm run lint`, and `npm run preview`; it does not define a root `test` script.

## Current limitations and next steps

- Evaluate on independent field photographs and report metrics by crop, disease, lighting, and capture conditions.
- Add and evaluate a separate leaf/non-leaf image gate if automated rejection of people or other non-leaf images is required. The current disease classifier is not a reliable leaf detector.
- Calibrate confidence and evaluate abstention behavior before presenting scores as diagnostic certainty.
- Add authentication and authorization before exposing scan history beyond a trusted local environment. Current history routes have no user authentication.
- Configure MongoDB for persistence; the fallback history buffer is in-memory, limited to 100 records, and is lost when the process restarts.
- The current `ml/` directory supplies inference and saved artifacts; it does not contain a training pipeline.

## Troubleshooting

- **Backend exits during startup:** confirm the checkpoint, class-name JSON, preprocessing JSON, and `ml/src/predict.py` exist and can be loaded. The backend intentionally fails instead of serving simulated outputs.
- **Frontend cannot reach the API:** ensure Uvicorn is running on port 8000, then check the Vite proxy target or `VITE_API_URL`.
- **Upload rejected:** the backend accepts JPEG, PNG, and WEBP up to the configured `MAX_IMAGE_SIZE_MB` (10 MB by default). Both extension and declared MIME type are checked, and the content must decode as an image.
- **History does not survive restart:** configure a reachable MongoDB instance; in-memory fallback records are temporary.

## Additional documentation

- [Backend setup and API details](backend/README.md)
- [Frontend setup and behavior](frontend/README.md)
- [Model artifacts and inference](ml/README.md)
