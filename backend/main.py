"""
BrailleScript – FastAPI backend

Provides REST endpoints for Spanish-to-Braille transcription, PNG export,
and PDF export.
"""

from __future__ import annotations

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel

from braille.encoder import encode_text, cells_to_unicode
from braille.renderer import render_png, render_pdf

# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------

app = FastAPI(
    title="BrailleScript API",
    description="Spanish → Braille transcription and visual signage export",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Request / Response models
# ---------------------------------------------------------------------------

class TranscribeRequest(BaseModel):
    text: str
    show_labels: bool = True


class CellOut(BaseModel):
    char: str
    dots: list[int]
    type: str


class TranscribeResponse(BaseModel):
    original: str
    cells: list[CellOut]
    unicode_braille: str


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/api/health")
async def health():
    return {"status": "ok"}


@app.post("/api/transcribe", response_model=TranscribeResponse)
async def transcribe(req: TranscribeRequest):
    cells = encode_text(req.text)
    unicode_braille = cells_to_unicode(cells)
    return TranscribeResponse(
        original=req.text,
        cells=[CellOut(**c) for c in cells],
        unicode_braille=unicode_braille,
    )


@app.get("/api/export/image")
async def export_image(
    text: str = Query(..., description="Text to transcribe"),
    show_labels: bool = Query(True),
    format: str = Query("png"),
):
    png_bytes = render_png(text, show_labels=show_labels)
    return Response(
        content=png_bytes,
        media_type="image/png",
        headers={
            "Content-Disposition": 'attachment; filename="braillescript.png"',
        },
    )


@app.get("/api/export/pdf")
async def export_pdf(
    text: str = Query(..., description="Text to transcribe"),
    show_labels: bool = Query(True),
):
    pdf_bytes = render_pdf(text, show_labels=show_labels)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": 'attachment; filename="braillescript.pdf"',
        },
    )
