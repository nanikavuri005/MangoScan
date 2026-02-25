from io import BytesIO
from fastapi import FastAPI, File, UploadFile, HTTPException
from PIL import Image, ImageStat, UnidentifiedImageError

app = FastAPI(title="MangoScan AI Service", version="1.1.0")


def simple_disease_inference(image: Image.Image) -> dict:
    """Demo inference strategy based on average RGB values."""
    rgb_image = image.convert("RGB")
    stats = ImageStat.Stat(rgb_image)
    avg_r, avg_g, avg_b = stats.mean[:3]

    if avg_g > avg_r + 8 and avg_g > avg_b:
        return {
            "diagnosis": "Healthy",
            "confidence": 0.87,
            "recommendedAction": "Continue current irrigation and monitoring schedule.",
            "modelVersion": "demo-v1",
        }

    if avg_r > avg_g + 5:
        return {
            "diagnosis": "Anthracnose (suspected)",
            "confidence": 0.79,
            "recommendedAction": "Remove infected leaves and apply copper-based fungicide.",
            "modelVersion": "demo-v1",
        }

    return {
        "diagnosis": "Powdery Mildew (suspected)",
        "confidence": 0.74,
        "recommendedAction": "Improve airflow and apply sulfur spray as advised.",
        "modelVersion": "demo-v1",
    }


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "mangoscan-ai"}


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
        pil_image = Image.open(BytesIO(data))
    except UnidentifiedImageError as exc:
        raise HTTPException(status_code=400, detail=f"Invalid image: {exc}") from exc

    return simple_disease_inference(pil_image)
