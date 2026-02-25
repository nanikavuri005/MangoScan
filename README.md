# MangoScan

MangoScan is a starter platform for crop disease detection with:
- `backend/` – Node.js REST API (JWT auth, image analysis workflow, MongoDB persistence)
- `ai_service/` – FastAPI ML inference service (demo inference)
- `docker-compose.yml` – run all services together

## Architecture

1. Mobile app calls backend auth APIs and upload endpoints.
2. Backend validates JWT, receives image upload, and forwards file to AI service.
3. AI service returns diagnosis payload.
4. Backend stores analysis history in MongoDB and returns response.

## Quick start (Docker)

```bash
cp backend/.env.example backend/.env
docker compose up --build
```

Services:
- Backend: `http://localhost:4000`
- AI service: `http://localhost:8000`
- MongoDB: `mongodb://localhost:27017`

## API overview

### Backend
- `GET /health`
- `POST /api/auth/register`
- `POST /api/auth/login`
- `POST /api/analyze` (JWT required, multipart form field `image`)
- `GET /api/analyze` (JWT required)

### AI service
- `GET /health`
- `POST /analyze` (multipart form field `image`)

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

## Automated checks

### Backend syntax checks
```bash
cd backend
npm run check
```

### AI service tests
```bash
cd ai_service
pytest
```

## Notes

- `ai_service/main.py` contains a demo heuristic (`simple_disease_inference`) for development.
- Replace the demo inference with your trained model pipeline for production usage.
- Set a secure `JWT_SECRET` in production.
