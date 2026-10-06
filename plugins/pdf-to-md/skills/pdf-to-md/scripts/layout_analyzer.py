"""
layout_analyzer.py — Layout Intermediate Representation (IR) builder for pdf-to-md.

Reads a PDF with pdfplumber and produces a JSON IR where every page is a list of
typed blocks:

    heading | paragraph | list_item | footnote | page_number | image | caption | table | blank_page

This IR is consumed by pdf_to_md.py (when --save-ir is passed) and can also be
used independently for debugging layout extraction.

Usage:
    python layout_analyzer.py input.pdf [--output ir.json] [--pages 1-5]

Output schema (one object per page):
    {
      "page": 3,
      "width": 595.0,
      "height": 842.0,
      "rotation": 0,
      "type": "native",          // native | ocr | blank
      "blocks": [
        {
          "kind": "heading",
          "level": 2,            // 1 | 2 | 3  (only for heading)
          "text": "Introducción",
          "bbox": [x0, y0, x1, y1],
          "font_size": 14.0
        },
        {
          "kind": "paragraph",
          "text": "El Instituto...",
          "bbox": [x0, y0, x1, y1]
        },
        {
          "kind": "image",
          "bbox": [x0, y0, x1, y1],
          "caption": "Figura 1. ..."   // empty string if not found
        },
        ...
      ]
    }
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Optional

try:
    import pdfplumber
except ImportError:
    sys.exit("pdfplumber not found. Install: pip install pdfplumber --break-system-packages")

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
PAGE_NUM_RE = re.compile(r"^\s*([IVXLCDM]{1,8}|\d{1,4})\s*$", re.IGNORECASE)
BULLET_RE   = re.compile(r"^[•–—\-\*]\s+\S")
NUMBERED_RE = re.compile(r"^(\d+|[a-z])\.\s+\S")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get_body_font_size(page) -> float:
    sizes = [round(c.get("size", 0)) for c in page.chars if c.get("size", 0) > 4]
    if not sizes:
        return 10.0
    return float(Counter(sizes).most_common(1)[0][0])


def _words_to_lines(words: list) -> list:
    """Group words into visual lines by Y proximity (±4 pt)."""
    if not words:
        return []
    lines: list = []
    words = sorted(words, key=lambda w: (round(w["top"] / 4), w["x0"]))
    current_line: list = [words[0]]
    for w in words[1:]:
        if abs(w["top"] - current_line[-1]["top"]) <= 4:
            current_line.append(w)
        else:
            lines.append(current_line)
            current_line = [w]
    lines.append(current_line)
    result = []
    for ln in lines:
        ln_sorted = sorted(ln, key=lambda w: w["x0"])
        text = " ".join(w["text"] for w in ln_sorted)
        result.append({
            "text": text,
            "top":  ln_sorted[0]["top"],
            "bottom": max(w["bottom"] for w in ln_sorted),
            "x0":   ln_sorted[0]["x0"],
            "x1":   ln_sorted[-1]["x1"],
        })
    return result


def _find_caption(figure_bbox, words, margin: float = 28.0) -> str:
    fx0, fy0, fx1, fy1 = figure_bbox
    cap_words = [
        w for w in words
        if fy1 < w["top"] < fy1 + margin
        and fx0 - 15 < (w["x0"] + w["x1"]) / 2 < fx1 + 15
    ]
    if not cap_words:
        return ""
    cap_sorted = sorted(cap_words, key=lambda w: (w["top"], w["x0"]))
    return " ".join(w["text"] for w in cap_sorted)


def _is_blank(page) -> bool:
    text = (page.extract_text() or "").strip()
    images = page.images or []
    rects  = [o for o in (page.rects or []) if o.get("width", 0) > 5 and o.get("height", 0) > 5]
    return not text and not images and len(rects) <= 2


def _classify_page(page) -> str:
    if _is_blank(page):
        return "blank"
    text = page.extract_text() or ""
    if len(text.strip()) > 50:
        return "native"
    return "ocr"


def _heading_level(font_size: float, body_size: float) -> Optional[int]:
    diff = font_size - body_size
    if diff >= 4:
        return 1
    if diff >= 2:
        return 2
    if diff >= 0.5:
        return 3
    return None


def _build_page_ir(page, page_num: int) -> dict:
    ptype = _classify_page(page)

    if ptype == "blank":
        return {
            "page": page_num,
            "width": float(page.width),
            "height": float(page.height),
            "rotation": page.rotation or 0,
            "type": "blank",
            "blocks": [{"kind": "blank_page", "text": "", "bbox": [0, 0, float(page.width), float(page.height)]}],
        }

    body_size = _get_body_font_size(page)
    words = page.extract_words(extra_attrs=["fontname", "size"]) or []
    lines = _words_to_lines(words)

    # Build a size-per-line lookup
    line_sizes: dict = {}
    for ln in lines:
        y_bucket = round(ln["top"] / 4) * 4
        ln_words = [w for w in words if abs(w["top"] - ln["top"]) <= 4]
        sizes = [w.get("size", body_size) for w in ln_words if w.get("size", 0) > 4]
        line_sizes[y_bucket] = float(sum(sizes) / len(sizes)) if sizes else body_size

    blocks: list = []
    h = float(page.height)

    for ln in lines:
        text = ln["text"].strip()
        if not text:
            continue

        y_ratio = ln["top"] / h
        y_bucket = round(ln["top"] / 4) * 4
        font_size = line_sizes.get(y_bucket, body_size)
        bbox = [ln["x0"], ln["top"], ln["x1"], ln["bottom"]]

        # Page number
        if (y_ratio < 0.08 or y_ratio > 0.92) and PAGE_NUM_RE.match(text):
            blocks.append({"kind": "page_number", "text": text, "bbox": bbox})
            continue

        # Footnote
        if y_ratio > 0.82 and font_size < body_size - 0.5:
            blocks.append({"kind": "footnote", "text": text, "bbox": bbox, "font_size": font_size})
            continue

        # Heading
        level = _heading_level(font_size, body_size)
        if level:
            blocks.append({"kind": "heading", "level": level, "text": text, "bbox": bbox, "font_size": font_size})
            continue

        # List item
        if BULLET_RE.match(text) or NUMBERED_RE.match(text):
            blocks.append({"kind": "list_item", "text": text, "bbox": bbox})
            continue

        # Default paragraph
        blocks.append({"kind": "paragraph", "text": text, "bbox": bbox})

    # Images with captions
    figures = page.images or []
    for fig in figures:
        fx0 = float(fig.get("x0", 0))
        fy0 = float(fig.get("y0", 0))
        fx1 = float(fig.get("x1", 0))
        fy1 = float(fig.get("y1", 0))
        fig_bbox = [fx0, fy0, fx1, fy1]
        caption = _find_caption(fig_bbox, words)
        blocks.append({"kind": "image", "bbox": fig_bbox, "caption": caption})

    # Tables (bboxes only — extraction done separately)
    try:
        for tbl in (page.find_tables() or []):
            b = tbl.bbox
            blocks.append({"kind": "table", "bbox": [b[0], b[1], b[2], b[3]]})
    except Exception:
        pass

    # Sort blocks top-to-bottom
    def _sort_key(block):
        b = block.get("bbox", [0, 0, 0, 0])
        return b[1]  # y0

    blocks.sort(key=_sort_key)

    return {
        "page": page_num,
        "width": float(page.width),
        "height": float(page.height),
        "rotation": page.rotation or 0,
        "type": ptype,
        "blocks": blocks,
    }


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def build_ir(pdf_path: str, page_range: Optional[tuple] = None) -> list:
    """
    Build and return the Layout IR for a PDF.

    Args:
        pdf_path:   Path to the PDF file.
        page_range: Optional (start, end) 1-indexed inclusive tuple.

    Returns:
        List of page dicts following the IR schema described at the top.
    """
    ir_pages: list = []
    with pdfplumber.open(pdf_path) as pdf:
        total = len(pdf.pages)
        start = (page_range[0] - 1) if page_range else 0
        end   = page_range[1] if page_range else total
        for i, page in enumerate(pdf.pages[start:end], start=start + 1):
            ir_pages.append(_build_page_ir(page, i))
    return ir_pages


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _parse_range(s: str) -> tuple:
    if "-" in s:
        parts = s.split("-", 1)
        return (int(parts[0]), int(parts[1]))
    n = int(s)
    return (n, n)


def main():
    parser = argparse.ArgumentParser(
        description="Build Layout IR JSON from a PDF.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("pdf", help="Input PDF file")
    parser.add_argument("--output", "-o", default="", help="Output JSON path (default: <pdf>_ir.json)")
    parser.add_argument("--pages", "-p", default="", help="Page range, e.g. 1-5 or 3")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON")
    args = parser.parse_args()

    pdf_path = Path(args.pdf)
    if not pdf_path.exists():
        sys.exit(f"File not found: {pdf_path}")

    page_range = _parse_range(args.pages) if args.pages else None
    ir = build_ir(str(pdf_path), page_range=page_range)

    out_path = Path(args.output) if args.output else pdf_path.with_suffix("_ir.json")
    indent = 2 if args.pretty else None
    out_path.write_text(json.dumps(ir, ensure_ascii=False, indent=indent), encoding="utf-8")
    print(f"IR guardado en: {out_path}  ({len(ir)} páginas)")


if __name__ == "__main__":
    main()
