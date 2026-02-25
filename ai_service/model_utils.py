from pathlib import Path
from typing import Tuple

import torch
from PIL import Image
from torchvision import models, transforms

MODEL_PATH = Path(__file__).parent / "model" / "mango_disease_model.pt"
CLASSES_PATH = Path(__file__).parent / "model" / "classes.txt"

TRANSFORM = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])


def _read_classes() -> list[str]:
    if not CLASSES_PATH.exists():
        return []
    return [line.strip() for line in CLASSES_PATH.read_text().splitlines() if line.strip()]


def _build_model(num_classes: int):
    model = models.resnet18(weights=None)
    model.fc = torch.nn.Linear(model.fc.in_features, num_classes)
    return model


def load_model_and_classes():
    if not MODEL_PATH.exists():
        return None, []

    checkpoint = torch.load(MODEL_PATH, map_location="cpu")
    classes = checkpoint.get("classes") or _read_classes()
    if not classes:
        return None, []

    model = _build_model(len(classes))
    model.load_state_dict(checkpoint["state_dict"])
    model.eval()
    return model, classes


def predict_disease(model, classes: list[str], image: Image.Image) -> Tuple[str, float, list[dict]]:
    tensor = TRANSFORM(image.convert("RGB")).unsqueeze(0)
    with torch.no_grad():
        logits = model(tensor)
        probs = torch.softmax(logits, dim=1).squeeze(0)

    confidence, idx = torch.max(probs, dim=0)
    top_k = min(3, probs.numel())
    top_values, top_indices = torch.topk(probs, k=top_k)

    top_predictions = []
    for score, class_idx in zip(top_values.tolist(), top_indices.tolist()):
        label = classes[class_idx] if class_idx < len(classes) else f"class_{class_idx}"
        top_predictions.append({"label": label, "confidence": round(float(score), 4)})

    class_idx = int(idx.item())
    disease = classes[class_idx] if class_idx < len(classes) else f"class_{class_idx}"
    return disease, float(confidence.item()), top_predictions
