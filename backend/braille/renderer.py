"""
BrailleScript – Image & PDF renderer

Uses Pillow for PNG and ReportLab for PDF generation.
"""

from __future__ import annotations

import io
import math
from pathlib import Path
from typing import Sequence

from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from .encoder import encode_text, cells_to_unicode

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

CELL_W = 60
CELL_H = 90
LABEL_H = 20        # extra height for label below cell
DOT_RADIUS = 10
DOT_FILLED = (30, 30, 30)
DOT_EMPTY = (200, 200, 200)
BG_COLOR = (255, 255, 255)
BORDER_COLOR = (180, 180, 180)
LABEL_COLOR = (80, 80, 80)
CELL_PAD = 6        # padding between cells
MAX_CELLS_PER_ROW = 20

# Dot center positions inside a cell (dot 1–6)
DOT_POSITIONS = {
    1: (15, 15),
    4: (45, 15),
    2: (15, 45),
    5: (45, 45),
    3: (15, 75),
    6: (45, 75),
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _try_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    """Try to load a TrueType font; fall back to default."""
    for name in (
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
        "/usr/share/fonts/truetype/freefont/FreeMono.ttf",
    ):
        try:
            return ImageFont.truetype(name, size)
        except (OSError, IOError):
            continue
    return ImageFont.load_default()


def _find_unicode_font() -> str | None:
    """Find a system TrueType font that supports Unicode Braille patterns."""
    candidates = [
        # Common Linux fonts
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
        # Common Windows fonts
        "C:/Windows/Fonts/seguisym.ttf",
        "C:/Windows/Fonts/arialuni.ttf",
        "C:/Windows/Fonts/DejaVuSans.ttf",
        # Common macOS fonts
        "/System/Library/Fonts/Apple Symbols.ttf",
    ]
    for path_str in candidates:
        path = Path(path_str)
        if path.is_file():
            return str(path)
    return None


def _register_unicode_pdf_font() -> str:
    """Register and return a PDF font name for Unicode Braille output."""
    font_name = "BrailleUnicode"
    if font_name in pdfmetrics.getRegisteredFontNames():
        return font_name

    font_path = _find_unicode_font()
    if font_path is None:
        return "Courier"

    pdfmetrics.registerFont(TTFont(font_name, font_path))
    return font_name


# ---------------------------------------------------------------------------
# PNG renderer
# ---------------------------------------------------------------------------


def render_png(
    text: str,
    show_labels: bool = True,
    max_per_row: int = MAX_CELLS_PER_ROW,
) -> bytes:
    """Render encoded Braille cells to a PNG image and return bytes."""
    cells = encode_text(text)
    if not cells:
        # Return a tiny blank image
        img = Image.new("RGB", (CELL_W, CELL_H), BG_COLOR)
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return buf.getvalue()

    n_cells = len(cells)
    cols = min(n_cells, max_per_row)
    rows = math.ceil(n_cells / max_per_row)

    cell_total_h = CELL_H + (LABEL_H if show_labels else 0)
    img_w = cols * (CELL_W + CELL_PAD) + CELL_PAD
    img_h = rows * (cell_total_h + CELL_PAD) + CELL_PAD

    img = Image.new("RGB", (img_w, img_h), BG_COLOR)
    draw = ImageDraw.Draw(img)
    font = _try_font(12)

    for idx, cell in enumerate(cells):
        col = idx % max_per_row
        row = idx // max_per_row
        x0 = CELL_PAD + col * (CELL_W + CELL_PAD)
        y0 = CELL_PAD + row * (cell_total_h + CELL_PAD)

        # Cell background & border
        draw.rounded_rectangle(
            [x0, y0, x0 + CELL_W, y0 + CELL_H],
            radius=6,
            outline=BORDER_COLOR,
            width=1,
        )

        # Draw dots
        raised = set(cell["dots"])
        for dot_num, (dx, dy) in DOT_POSITIONS.items():
            cx = x0 + dx
            cy = y0 + dy
            if dot_num in raised:
                draw.ellipse(
                    [cx - DOT_RADIUS, cy - DOT_RADIUS,
                     cx + DOT_RADIUS, cy + DOT_RADIUS],
                    fill=DOT_FILLED,
                )
            else:
                draw.ellipse(
                    [cx - DOT_RADIUS, cy - DOT_RADIUS,
                     cx + DOT_RADIUS, cy + DOT_RADIUS],
                    outline=DOT_EMPTY,
                    width=1,
                )

        # Label
        if show_labels:
            label = cell["char"]
            bbox = font.getbbox(label)
            tw = bbox[2] - bbox[0]
            lx = x0 + (CELL_W - tw) // 2
            ly = y0 + CELL_H + 2
            draw.text((lx, ly), label, fill=LABEL_COLOR, font=font)

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


# ---------------------------------------------------------------------------
# PDF renderer
# ---------------------------------------------------------------------------


def render_pdf(text: str, show_labels: bool = True) -> bytes:
    """Render encoded Braille cells to a PDF and return bytes."""
    cells = encode_text(text)
    unicode_str = cells_to_unicode(cells)

    buf = io.BytesIO()
    page_w, page_h = A4
    c = canvas.Canvas(buf, pagesize=A4)

    margin = 20 * mm
    y_cursor = 0
    cell_w_pt = CELL_W * 0.75   # scale for PDF points
    cell_h_pt = CELL_H * 0.75
    label_h_pt = LABEL_H * 0.6
    pad_pt = 4
    max_col = int((page_w - 2 * margin) / (cell_w_pt + pad_pt))
    cell_block_h = cell_h_pt + label_h_pt + pad_pt

    def draw_header() -> None:
        nonlocal y_cursor
        y_cursor = page_h - margin
        c.setFont("Helvetica-Bold", 16)
        c.drawString(margin, y_cursor, "BrailleScript – Transcripción Braille")
        y_cursor -= 10 * mm

        c.setFont("Helvetica", 11)
        c.drawString(margin, y_cursor, f"Texto original: {text[:120]}{'…' if len(text) > 120 else ''}")
        y_cursor -= 7 * mm

        c.setFont(unicode_font_name, 10)
        c.drawString(margin, y_cursor, f"Braille Unicode: {unicode_str[:100]}{'…' if len(unicode_str) > 100 else ''}")
        y_cursor -= 12 * mm

    unicode_font_name = _register_unicode_pdf_font()
    draw_header()
    rows_per_page = max(1, int((y_cursor - margin + pad_pt) / cell_block_h))
    cells_per_page = max_col * rows_per_page
    page_cell_index = 0

    for cell in cells:
        if page_cell_index >= cells_per_page:
            c.showPage()
            draw_header()
            page_cell_index = 0

        col = page_cell_index % max_col
        row = page_cell_index // max_col
        x0 = margin + col * (cell_w_pt + pad_pt)
        y0 = y_cursor - row * cell_block_h

        c.setStrokeColorRGB(0.7, 0.7, 0.7)
        c.setLineWidth(0.5)
        c.roundRect(x0, y0 - cell_h_pt, cell_w_pt, cell_h_pt, 3)

        raised = set(cell["dots"])
        scale = 0.75
        for dot_num, (dx, dy) in DOT_POSITIONS.items():
            cx = x0 + dx * scale
            cy = y0 - dy * scale
            r = DOT_RADIUS * scale * 0.8
            if dot_num in raised:
                c.setFillColorRGB(0.12, 0.12, 0.12)
                c.circle(cx, cy, r, fill=1, stroke=0)
            else:
                c.setFillColorRGB(1, 1, 1)
                c.setStrokeColorRGB(0.78, 0.78, 0.78)
                c.circle(cx, cy, r, fill=0, stroke=1)

        if show_labels:
            c.setFillColorRGB(0.3, 0.3, 0.3)
            c.setFont("Helvetica", 7)
            c.drawCentredString(
                x0 + cell_w_pt / 2,
                y0 - cell_h_pt - label_h_pt + 2,
                cell["char"],
            )

        page_cell_index += 1

    c.save()
    return buf.getvalue()
