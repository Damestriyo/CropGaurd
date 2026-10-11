# CropGaurd FastAPI backend

This service validates uploaded images, runs the trained MobileNetV2 classifier, resolves its class to a crop/disease catalog entry, and records prediction metadata. It does not return simulated predictions: the model is required and loaded during application startup.

## Requirements and setup

Use Python 3.10 or newer with a compatible PyTorch and Torchvision build. The project dependency list is at the repository root. From `C:\CropGaurd` in PowerShell:

```powershell
py -3.13 -m venv .\backend\.venv
.\backend\.venv\Scripts\python.exe -m pip install --upgrade pip
.\backend\.venv\Scripts\python.exe -m pip install -r .\requirements.txt
if (-not (Test-Path .\backend\.env)) { Copy-Item .\backend\.env.example .\backend\.env }
```

Only copy `.env.example` during initial setup. Keep and edit an existing `backend/.env` rather than overwriting it. Start the service from `backend/` so `python-dotenv` reads that directory's `.env` file:

```powershell
Set-Location C:\CropGaurd\backend
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

The model and configuration files are resolved relative to the source tree. Startup requires `ml/src/predict.py` and `ml/artifacts/mobilenetv2_best.pth`, `class_names.json`, and `preprocessing.json`. A missing or invalid model artifact stops startup.

Open `http://localhost:8000/docs` for Swagger UI or `http://localhost:8000/redoc` for ReDoc. `GET /health` returns service health and whether MongoDB is connected.

## Configuration

The settings used by the backend are:

| Variable | Default | Notes |
|---|---|---|
| `PROJECT_NAME` | `AI Crop Disease Detection API` | FastAPI title |
| `ALLOWED_ORIGINS` | localhost/127.0.0.1 ports 3000 and 5173 | Comma-separated CORS origin list |
| `MONGODB_URL` | `mongodb://localhost:27017` | `MONGODB_URI` is accepted as an alias |
| `DATABASE_NAME` | `crop_disease_db` | `MONGODB_DB_NAME` is accepted as an alias |
| `MAX_IMAGE_SIZE_MB` | `10` | Maximum upload size |
| `ALLOWED_IMAGE_EXTENSIONS` | `.jpg,.jpeg,.png,.webp` | Case-insensitive suffix allowlist |
| `ALLOWED_IMAGE_MIME_TYPES` | `image/jpeg,image/png,image/webp` | Declared MIME allowlist |

`HOST`, `PORT`, and `DEBUG` are present in `.env.example` but are not read to configure Uvicorn or application behavior; configure the server with Uvicorn options. The MongoDB settings in `.env.example` are commented out as planned values, but the backend itself attempts the configured/default MongoDB connection at startup. JWT example settings are placeholders; authentication is not implemented.

MongoDB connection failure is logged and the API remains available. Prediction history then uses a process-local buffer capped at 100 records; these records are lost when the process exits. The disease catalog is a static Python dictionary and does not depend on MongoDB.

## Prediction endpoint

`POST /predict` accepts multipart form data with a required `file` field. `POST /predict/` is an equivalent alias. The service checks the filename extension, optional declared MIME type, configured size limit, and whether Pillow can verify/decode the uploaded bytes. It extracts filename, content type, byte size, dimensions, format, mode, and channel count before inference.

| Status | Meaning |
|---:|---|
| `200` | Image was classified and the prediction record was handled |
| `400` | Missing filename, empty upload, or corrupt/non-decodable image |
| `413` | Upload exceeds `MAX_IMAGE_SIZE_MB` |
| `415` | Unsupported extension or declared MIME type |
| `422` | FastAPI request validation failure, such as a missing `file` field |
| `503` | Model inference failed for the request |

The response contains `id`, `success`, `message`, `image_metadata`, `prediction`, and nullable `disease_info`. `prediction` holds `crop`, `disease`, `confidence`, `severity`, and `is_healthy`. `disease_info` is resolved through `DiseaseService` and includes catalog ID, scientific name when known, typical severity, symptoms, causes, prevention, and management. An unmatched class leaves the catalog field empty rather than hardcoding disease data in the route.

The model softmax score is returned as a percentage and is not calibrated diagnostic certainty. The classifier does not estimate an individual plant's disease severity: diseased classes use `prediction.severity="Unknown"`; healthy classes use `"None"`. `disease_info.severity` is a typical disease-level category, not an assessment of the uploaded plant.

Pillow checks that content is an image; it cannot verify that the image contains a leaf. The frontend asks for user confirmation that the main subject is a crop leaf, but direct API callers can bypass that prompt. Automated non-leaf rejection requires a separate evaluated leaf/non-leaf validation model.

## Other routes

| Method | Path | Behavior |
|---|---|---|
| `GET` | `/` | Project/version status and database connection status |
| `GET` | `/health` | Health and database connection status |
| `GET` | `/diseases?crop=Tomato` | List static disease catalog entries, optionally filtered by exact crop name ignoring case |
| `GET` | `/diseases/{id}` | Retrieve a catalog entry by ID; `404` if absent |
| `GET` | `/history?limit=20&skip=0` | List prediction metadata, newest first; limit 1–100 and skip >= 0 |
| `GET` | `/history/{id}` | Retrieve one record; `404` if absent |
| `DELETE` | `/history/{id}` | Delete one record; `404` if absent |

History currently has no authentication or per-user access control. Records contain prediction and image metadata, not image bytes.

## Model labels and artifacts

The backend reads the model's class order from `ml/artifacts/class_names.json`. `PredictorService.CLASS_MAPPING` maps all 15 labels to canonical crop, disease, and healthy values. `DiseaseService.get_info_for_prediction()` matches normalized crop and disease names against the catalog; all current model labels resolve, including healthy classes.

`ml/src/predict.py` builds MobileNetV2 with `weights=None`, changes its classifier output width to match the class list, then loads the saved checkpoint. Input preprocessing uses the saved configuration: RGB, 224 × 224, ImageNet channel mean and standard deviation normalization. The inference code does not prove how the weights were initialized during training.

The model's reported individual-plant severity is not inferred from the disease class. The catalog includes additional non-model entries, but only the 15 labels in `class_names.json` are supported by the classifier.

## Tests

Run the backend tests from this directory:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

For the focused class mapping/catalog regression checks:

```powershell
.\.venv\Scripts\python.exe -m pytest -q tests/test_diseases.py::test_tomato_leaf_mold_prediction_lookup_is_case_insensitive tests/test_diseases.py::test_unlisted_prediction_still_has_no_catalog_entry tests/test_diseases.py::test_class_names_file_is_fully_covered_by_expected_catalog_ids tests/test_diseases.py::test_each_model_class_resolves_to_its_catalog_entry tests/test_prediction.py::test_all_model_labels_have_explicit_crop_and_disease_mapping tests/test_prediction.py::test_tomato_bacterial_spot_prediction_resolves_catalog_entry
```

The focused checks cover class labels, disease catalog IDs, healthy-class flags/severity, lookup normalization, and the Tomato Bacterial Spot mapping.
