# CropGuard — Plant Disease Classification

## Model
- Architecture: MobileNetV2
- Pretrained on: ImageNet
- Input: RGB image resized to 224 x 224
- Output: 15 plant disease and healthy classes
- Framework: PyTorch / Torchvision

## Evaluation

Evaluated on the held-out PlantVillage test split:
- Accuracy: 99.00%
- Macro F1: 98.79%
- Weighted F1: 99.00%
- Test images: 3,094

These results describe performance on the PlantVillage test set.
Real-world farm images may produce different results.

## Files

- `src/predict.py`: model loading and inference interface
- `artifacts/mobilenetv2_best.pth`: best fine-tuned checkpoint
- `artifacts/class_names.json`: output class order
- `artifacts/preprocessing.json`: inference preprocessing configuration
- `artifacts/metrics.json`: evaluation summary
- `artifacts/test_classification_report.csv`: per-class test metrics
- `artifacts/training_history.csv`: baseline training history
- `artifacts/finetuning_history.csv`: fine-tuning history

## Inference

The predictor returns:
- `predicted_class`
- `confidence`
- `top_predictions`

Example:

```python
from ml.src.predict import PlantDiseasePredictor

predictor = PlantDiseasePredictor("ml/artifacts")
result = predictor.predict("path/to/leaf_image.jpg")
print(result)
```

Install compatible versions of PyTorch, Torchvision, Pillow, and pandas
as required by the project environment. The model inference code also
requires the checkpoint and JSON configuration files listed above.

Softmax confidence is not a guarantee of correctness. This model should
not be treated as a definitive field diagnosis without real-world validation.
