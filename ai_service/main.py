import os
from io import BytesIO

from fastapi import FastAPI, File, HTTPException, UploadFile
from PIL import Image, ImageStat, UnidentifiedImageError

from disease_practices import normalize_disease_name, practices_for
from model_utils import load_model_and_classes, predict_disease

app = FastAPI(title="MangoScan AI Service", version="2.1.0")

MODEL, CLASSES = load_model_and_classes()
MIN_CONFIDENCE = float(os.getenv("MIN_CONFIDENCE", "0.65"))


def fallback_inference(image: Image.Image) -> tuple[str, float, list[dict]]:
    """Fallback heuristic used if a trained model is unavailable."""
    rgb_image = image.convert("RGB")
    stats = ImageStat.Stat(rgb_image)
    avg_r, avg_g, avg_b = stats.mean[:3]

    if avg_g > avg_r + 8 and avg_g > avg_b:
        return "Healthy", 0.70, [{"label": "Healthy", "confidence": 0.7}]
    if avg_r > avg_g + 5:
        return "Anthracnose", 0.65, [{"label": "Anthracnose", "confidence": 0.65}]
    return "Powdery Mildew", 0.62, [{"label": "Powdery Mildew", "confidence": 0.62}]


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "mangoscan-ai",
        "model_loaded": MODEL is not None,
        "num_classes": len(CLASSES),
        "min_confidence": MIN_CONFIDENCE,
    }


@app.post("/analyze")
async def analyze(image: UploadFile = File(...)):
    if not image.content_type or not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file must be an image")

    data = await image.read()
    if not data:
        raise HTTPException(status_code=400, detail="Empty file")

    try:
        pil_image = Image.open(BytesIO(data))
        pil_image.verify()
        pil_image = Image.open(BytesIO(data)).convert("RGB")
    except UnidentifiedImageError as exc:
        raise HTTPException(status_code=400, detail=f"Invalid image: {exc}") from exc

    if MODEL is not None and CLASSES:
        disease, confidence, top_predictions = predict_disease(MODEL, CLASSES, pil_image)
        model_version = "kaggle-mango-resnet18-v1"
    else:
        disease, confidence, top_predictions = fallback_inference(pil_image)
        model_version = "fallback-heuristic-v1"

    disease = normalize_disease_name(disease)
    low_confidence = confidence < MIN_CONFIDENCE

    if low_confidence:
        diagnosed = "Uncertain"
        warning = (
            "Low-confidence prediction. Please retake a clearer image and re-submit. "
            "Use this diagnosis only as preliminary guidance."
        )
    else:
        diagnosed = disease
        warning = None

    return {
        "diagnosis": diagnosed,
        "rawPrediction": disease,
        "confidence": round(confidence, 4),
        "minConfidence": MIN_CONFIDENCE,
        "lowConfidence": low_confidence,
        "topPredictions": [
            {
                "label": normalize_disease_name(item["label"]),
                "confidence": item["confidence"],
            }
            for item in top_predictions
        ],
        "recommendedAction": " ; ".join(practices_for(diagnosed)),
        "practices": practices_for(diagnosed),
        "warning": warning,
        "modelVersion": model_version,
    }
