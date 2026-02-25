# MangoScan

MangoScan is a crop disease detection platform with:
- `backend/` – Node.js REST API (JWT auth, upload flow, MongoDB persistence)
- `ai_service/` – FastAPI inference service for mango leaf disease classification
- `docker-compose.yml` – run all services together

## Architecture

1. Farmer app sends login and analysis requests to backend.
2. Backend validates JWT and forwards uploaded image to AI service.
3. AI service predicts disease class and returns practical treatment recommendations.
4. Backend stores diagnosis, confidence, and recommended practices in MongoDB.

## Dataset and training (Kaggle)

This project is designed for the Kaggle dataset:
`https://www.kaggle.com/datasets/aryashah2k/mango-leaf-disease-dataset`

### 1) Download dataset

Use Kaggle CLI (after setting up `~/.kaggle/kaggle.json`):

```bash
kaggle datasets download -d aryashah2k/mango-leaf-disease-dataset
unzip mango-leaf-disease-dataset.zip -d data/mango_leaf_disease_dataset
```

Ensure extracted structure contains:
- `train/<class_name>/*.jpg`
- `valid/<class_name>/*.jpg`

### 2) Train model

From repo root:

```bash
python ai_service/scripts/train_model.py \
  --dataset-dir data/mango_leaf_disease_dataset \
  --epochs 8 \
  --batch-size 32 \
  --output-dir ai_service/model
```

The script saves:
- `ai_service/model/mango_disease_model.pt`
- `ai_service/model/classes.txt`

### 3) Start services

```bash
cp backend/.env.example backend/.env
docker compose up --build
```

## API output for farmers

`POST /api/analyze` returns:

```json
{
  "id": "...",
  "diagnosis": "Anthracnose",
  "confidence": 0.9123,
  "recommendedAction": "Prune and destroy infected leaves...",
  "practices": [
    "Prune and destroy infected leaves/twigs to reduce inoculum.",
    "Spray copper oxychloride or carbendazim as per local agricultural guidance.",
    "Avoid overhead irrigation late in the day to reduce leaf wetness."
  ],
  "createdAt": "2026-01-01T00:00:00.000Z"
}
```

This gives each farmer both disease name and actionable practices.


## Improving wrong predictions

If predictions are wrong on some images, MangoScan now returns:
- `lowConfidence` flag when score is below threshold
- `topPredictions` (top-3 labels with confidence)
- `rawPrediction` + normalized final `diagnosis`

You can tune the threshold via AI service env var:

```bash
MIN_CONFIDENCE=0.65
```

For better accuracy:
1. Train with more epochs and image augmentations.
2. Ensure dataset class names are clean and consistent.
3. Capture clear leaf close-ups in daylight (single leaf per image).

## Quick start (Docker)

```bash
cp backend/.env.example backend/.env
docker compose up --build
```

Services:
- Backend: `http://localhost:4000`
- AI service: `http://localhost:8000`
- MongoDB: `mongodb://localhost:27017`

## Local development

### Backend
```bash
cd backend
npm install
cp .env.example .env
npm run start
```

### AI service
```bash
cd ai_service
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## Validation commands

```bash
cd backend && npm run check
cd ai_service && pytest
```

## Notes

- If trained model files are missing, AI service falls back to a heuristic classifier.
- Replace recommendation text with region-specific agronomy guidance for production.
