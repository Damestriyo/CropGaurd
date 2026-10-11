# CropGaurd model artifacts and inference

The ML directory contains a MobileNetV2 inference implementation and the saved model artifacts used by the backend. The backend loads the model once when FastAPI starts and uses the output order in `artifacts/class_names.json` to map predictions.

## Model and preprocessing

- Architecture: MobileNetV2 with the classifier output sized for 15 classes.
- Framework: PyTorch and Torchvision.
- Input: RGB image resized to 224 × 224.
- Normalization: means `[0.485, 0.456, 0.406]`; standard deviations `[0.229, 0.224, 0.225]`.
- Output: predicted class, softmax confidence, and top predictions.

`src/predict.py` constructs MobileNetV2 using `weights=None`, then loads the saved checkpoint state dictionary. The inference code does not download ImageNet weights. The files in this project do not establish how the checkpoint was initialized during training, so ImageNet pretraining is not claimed here.

## Saved evaluation

The saved `artifacts/metrics.json` reports these aggregate results for 3,094 test samples:

| Metric | Result |
|---|---:|
| Accuracy | 99.00% |
| Macro F1 | 98.79% |
| Weighted F1 | 99.00% |
| Test samples | 3,094 |

These metrics describe the saved test evaluation only. They do not guarantee equivalent performance on field photographs, different cameras, or images outside the supported classes. Softmax confidence is not calibrated diagnostic certainty. This classifier does not assess the severity of an individual plant and is not a leaf/non-leaf detector.

Project notes have described the test split as PlantVillage. The metrics file and available inference source do not record dataset provenance or how the split was produced, and no training pipeline is included here. Treat that dataset attribution as unverified project-reported information until training and evaluation records are available.

## Artifacts

- `src/predict.py` — model construction, checkpoint loading, transforms, and inference.
- `artifacts/mobilenetv2_best.pth` — saved state dictionary checkpoint.
- `artifacts/class_names.json` — exact 15-class output order.
- `artifacts/preprocessing.json` — saved architecture and preprocessing metadata.
- `artifacts/metrics.json` — aggregate evaluation metrics.
- `artifacts/test_classification_report.csv` — per-class and aggregate test report.
- `artifacts/training_history.csv` and `artifacts/finetuning_history.csv` — saved training-history records.

The repository includes inference code and training-history artifacts, but no training pipeline under `ml/src`.

## Inference example

Run from the repository root with the project Python dependencies installed:

```python
from ml.src.predict import PlantDiseasePredictor

predictor = PlantDiseasePredictor("ml/artifacts")
result = predictor.predict("path/to/leaf_image.jpg")
print(result)
```

The backend applies an API mapping from these model labels to canonical crop and disease names, then looks up disease information in its catalog. See [the backend README](../backend/README.md) for API setup and the list of supported labels.
