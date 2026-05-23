# BrailleScript

**Transcriptor de texto en español a escritura Braille con exportación visual de señalización.**

BrailleScript is a full-stack web application that converts Spanish text into Braille notation, renders interactive Braille cells in the browser, and exports the result as PNG images or PDF documents.

---

## Architecture

| Layer    | Tech          | Port  |
|----------|---------------|-------|
| Backend  | Python/FastAPI| 8000  |
| Frontend | React/Vite    | 5173  |

The frontend proxies `/api` requests to the backend via Vite's dev server proxy.

---

## Quick Start

### 1. Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173` in your browser.

---

## Docker

Run the entire stack with a single command:

```bash
docker compose up --build
```

| Service  | URL                    |
|----------|------------------------|
| Frontend | http://localhost:3000   |
| Backend  | http://localhost:8000   |

The frontend nginx container reverse-proxies `/api` requests to the backend.

---

## API Endpoints

| Method | Path                | Description                  |
|--------|---------------------|------------------------------|
| POST   | `/api/transcribe`   | Transcribe text to Braille   |
| GET    | `/api/export/image` | Export Braille as PNG image   |
| GET    | `/api/export/pdf`   | Export Braille as PDF         |
| GET    | `/api/health`       | Health check                 |

### POST /api/transcribe

```json
{
  "text": "Hola Mundo 123",
  "show_labels": true
}
```

Response:

```json
{
  "original": "Hola Mundo 123",
  "cells": [
    { "char": "⠠", "dots": [6], "type": "prefix" },
    { "char": "H", "dots": [1,2,5], "type": "letter" },
    ...
  ],
  "unicode_braille": "⠠⠓⠕⠇⠁ ⠠⠍⠥⠝⠙⠕ ⠼⠁⠃⠉"
}
```

---

## Braille System

Implements the complete Spanish Braille standard including:
- Full alphabet (a–z) across three series
- Accented vowels: á, é, í, ó, ú
- Special characters: ñ, ü, w
- Number sign prefix for digit runs
- Uppercase sign prefix for capitals
- Basic punctuation and mathematical signs

---

## License

MIT
