

from pathlib import Path
import json

import torch
import torch.nn as nn
from PIL import Image
from torchvision import transforms
from torchvision.models import mobilenet_v2


class PlantDiseasePredictor:
    def __init__(self, artifacts_dir):
        self.artifacts_dir = Path(artifacts_dir)
        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )

        checkpoint_path = (
            self.artifacts_dir / "mobilenetv2_best.pth"
        )
        class_names_path = (
            self.artifacts_dir / "class_names.json"
        )
        preprocessing_path = (
            self.artifacts_dir / "preprocessing.json"
        )

        with open(class_names_path, "r") as f:
            self.class_names = json.load(f)

        with open(preprocessing_path, "r") as f:
            self.preprocessing = json.load(f)

        self.model = mobilenet_v2(weights=None)
        self.model.classifier[1] = nn.Linear(
            self.model.classifier[1].in_features,
            len(self.class_names)
        )

        checkpoint = torch.load(
            checkpoint_path,
            map_location=self.device,
            weights_only=False
        )
        self.model.load_state_dict(checkpoint["model_state_dict"])
        self.model.to(self.device)
        self.model.eval()

        mean = self.preprocessing["normalization"]["mean"]
        std = self.preprocessing["normalization"]["std"]
        size = tuple(self.preprocessing["input_size"])

        self.transform = transforms.Compose([
            transforms.Resize(size),
            transforms.ToTensor(),
            transforms.Normalize(mean, std)
        ])

    @torch.inference_mode()
    def predict(self, image_path, top_k=3):
        with Image.open(image_path) as image:
            image = image.convert("RGB")
            tensor = self.transform(image).unsqueeze(0)
            tensor = tensor.to(self.device)

        logits = self.model(tensor)
        probabilities = torch.softmax(logits, dim=1)[0]

        k = min(top_k, len(self.class_names))
        scores, indices = torch.topk(probabilities, k=k)

        results = [
            {
                "class_name": self.class_names[index.item()],
                "confidence": round(score.item(), 6)
            }
            for score, index in zip(scores, indices)
        ]

        return {
            "predicted_class": results[0]["class_name"],
            "confidence": results[0]["confidence"],
            "top_predictions": results
        }
