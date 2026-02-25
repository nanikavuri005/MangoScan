# MangoScan

Production-ready starter stack for a crop-disease detection platform with:
- **Node.js backend API** (auth, upload, analysis history)
- **Python AI service** (image analysis endpoint)
- **MongoDB** persistence

## Architecture

1. Mobile client calls backend `/api/auth/*` and `/api/analyze`.
2. Backend verifies JWT token and accepts image upload.
3. Backend forwards image to AI service (`POST /analyze`).
4. AI service returns diagnosis result.
5. Backend stores result in MongoDB and returns response to client.

## Project structure

- `backend/` – Node.js REST API
- `ai_service/` – FastAPI ML inference service (demo inference)
- `docker-compose.yml` – run all services together

## Quick start (Docker)

```bash
cp backend/.env.example backend/.env
docker compose up --build
```

Services:
- Backend: `http://localhost:4000`
- AI service: `http://localhost:8000`
- MongoDB: `mongodb://localhost:27017`

## Backend API

### Health

- `GET /health`

### Register

- `POST /api/auth/register`
- Body:

```json
{
  "name": "Farmer One",
  "email": "farmer@example.com",
  "password": "strongpassword"
}
```

### Login

- `POST /api/auth/login`
- Body:

```json
{
  "email": "farmer@example.com",
  "password": "strongpassword"
}
```

Response returns JWT token:

```json
{
  "token": "<jwt>"
}
```

### Analyze image

- `POST /api/analyze`
- Headers: `Authorization: Bearer <jwt>`
- Content-Type: `multipart/form-data`
- Field name: `image`

Example:

```bash
curl -X POST http://localhost:4000/api/analyze \
  -H "Authorization: Bearer <jwt>" \
  -F "image=@/path/to/mango_leaf.jpg"
```

### Get analysis history

- `GET /api/analyze`
- Headers: `Authorization: Bearer <jwt>`

## Local development (without Docker)

### Backend

```bash
cd backend
npm install
cp .env.example .env
npm run dev
```

### AI Service

```bash
cd ai_service
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## Notes

- The AI inference in `ai_service/main.py` is a **demo heuristic**.
- Replace `simple_disease_inference` with your trained model pipeline.
- Never use the sample JWT secret in production.
