from io import BytesIO
from fastapi import FastAPI, File, UploadFile, HTTPException
from PIL import Image

app = FastAPI(title="MangoScan AI Service", version="1.0.0")


def simple_disease_inference(image: Image.Image) -> dict:
    """
    Demo inference strategy based on average RGB values.
    Replace with your trained model inference pipeline in production.
    """
    rgb_image = image.convert("RGB")
    pixels = list(rgb_image.getdata())
    total = len(pixels)

    avg_r = sum(p[0] for p in pixels) / total
    avg_g = sum(p[1] for p in pixels) / total
    avg_b = sum(p[2] for p in pixels) / total

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
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Invalid image: {exc}") from exc

    result = simple_disease_inference(pil_image)
    return result
