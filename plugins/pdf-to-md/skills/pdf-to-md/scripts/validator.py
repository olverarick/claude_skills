"""
validator.py — Quality validation for pdf-to-md conversions.

Reads either:
  a) A Markdown file + its _audit.md  (post-conversion validation)
  b) A Layout IR JSON file            (pre-render structural validation)

Produces a machine-readable quality report (JSON) and a human-readable
summary (printed to stdout / written to file).

Usage:
    # Validate a finished conversion
    python validator.py output.md [--audit output_audit.md] [--report report.json]

    # Validate raw IR only
    python validator.py --ir ir.json [--report report.json]

Quality score: 0–100 (same formula as pdf_to_md.py)
  estructura  20%  — at least one heading detected
  texto       20%  — non-blank-page coverage > 80%
  imagenes    15%  — caption ratio (images with captions / total images)
  tablas      10%  — N/A if no tables; 100 if any table was extracted
  ocr         10%  — average OCR confidence (or 100 if no OCR pages)
  layout      25%  — penalty for hard fallbacks and blank/total page ratio

Exit codes:
  0  — score ≥ 80 (PASS)
  1  — score 60–79 (WARN)
  2  — score < 60 (FAIL)
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Optional


# ---------------------------------------------------------------------------
# Markdown-based validation
# ---------------------------------------------------------------------------

def _count_headings(md: str) -> int:
    return len(re.findall(r"^#{1,3} .+", md, re.MULTILINE))


def _count_images(md: str) -> int:
    return len(re.findall(r"!\[", md))


def _count_captioned_images(md: str) -> int:
    """Images followed by an italic caption line (not the default boilerplate)."""
    pattern = re.compile(
        r"!\[.*?\]\(.*?\)\n\*(?!Imagen de página \d+ — ver auditoría).+?\*",
        re.MULTILINE,
    )
    return len(pattern.findall(md))


def _count_tables(md: str) -> int:
    return len(re.findall(r"^\|.+\|$", md, re.MULTILINE))


def _count_blank_page_markers(md: str) -> int:
    return md.count("[Página") and md.count("en blanco en el documento original")


def _parse_audit_confidence(audit_md: str) -> float:
    """Extract average OCR confidence from audit markdown."""
    match = re.search(r"Confianza OCR promedio[:\s]+([0-9.]+)%", audit_md)
    if match:
        return float(match.group(1))
    return -1.0


def _parse_audit_pages(audit_md: str) -> dict:
    """Return {'total': N, 'ocr': N, 'blank': N, 'native': N, 'fallback': N}."""
    result = {"total": 0, "ocr": 0, "blank": 0, "native": 0, "fallback": 0}
    m = re.search(r"Páginas totales[:\s]+(\d+)", audit_md)
    if m:
        result["total"] = int(m.group(1))
    m = re.search(r"Páginas procesadas con OCR[:\s]+(\d+)", audit_md)
    if m:
        result["ocr"] = int(m.group(1))
    m = re.search(r"Páginas en blanco[:\s]+(\d+)", audit_md)
    if m:
        result["blank"] = int(m.group(1))
    result["native"] = result["total"] - result["ocr"] - result["blank"]
    m = re.search(r"Fallback a OCR[:\s]+(\d+)", audit_md)
    if m:
        result["fallback"] = int(m.group(1))
    return result


# ---------------------------------------------------------------------------
# IR-based validation
# ---------------------------------------------------------------------------

def _validate_ir(ir: list) -> dict:
    """Compute quality metrics from a Layout IR list."""
    total_pages  = len(ir)
    blank_pages  = sum(1 for p in ir if p.get("type") == "blank")
    ocr_pages    = sum(1 for p in ir if p.get("type") == "ocr")
    content_pages = total_pages - blank_pages

    all_blocks = [b for p in ir for b in p.get("blocks", [])]
    headings   = [b for b in all_blocks if b["kind"] == "heading"]
    images     = [b for b in all_blocks if b["kind"] == "image"]
    captioned  = [b for b in images if b.get("caption", "").strip()]
    tables     = [b for b in all_blocks if b["kind"] == "table"]
    paragraphs = [b for b in all_blocks if b["kind"] == "paragraph"]

    has_headings    = len(headings) > 0
    text_coverage   = 1.0 if content_pages == 0 else min(1.0, len(paragraphs) / max(content_pages, 1) / 3)
    image_cap_ratio = len(captioned) / max(len(images), 1)
    has_tables      = len(tables) > 0
    blank_ratio     = blank_pages / max(total_pages, 1)

    return {
        "total_pages": total_pages,
        "blank_pages": blank_pages,
        "ocr_pages": ocr_pages,
        "headings": len(headings),
        "images": len(images),
        "captioned_images": len(captioned),
        "tables": len(tables),
        "paragraphs": len(paragraphs),
        "has_headings": has_headings,
        "text_coverage": text_coverage,
        "image_cap_ratio": image_cap_ratio,
        "has_tables": has_tables,
        "blank_ratio": blank_ratio,
        "ocr_confidence": -1.0,  # not available from IR alone
        "fallback_pages": 0,
    }


# ---------------------------------------------------------------------------
# Score computation
# ---------------------------------------------------------------------------

def compute_score(metrics: dict) -> dict:
    """
    Compute the 6-dimension quality score (0–100).

    Returns a dict with per-dimension scores and the weighted total.
    """
    # 1. Estructura — has at least one heading
    s_estructura = 100.0 if metrics.get("has_headings") else 0.0

    # 2. Texto — content page coverage
    cov = metrics.get("text_coverage", 0.0)
    s_texto = min(100.0, cov * 100.0)

    # 3. Imágenes — caption ratio
    cap_ratio = metrics.get("image_cap_ratio", 1.0)
    if metrics.get("images", 0) == 0:
        s_imagenes = 100.0  # no images → not penalized
    else:
        s_imagenes = cap_ratio * 100.0

    # 4. Tablas — extracted at least one (or no tables present)
    has_tables = metrics.get("has_tables", False)
    table_count = metrics.get("tables", 0)
    s_tablas = 100.0 if (table_count == 0 or has_tables) else 0.0

    # 5. OCR confidence
    conf = metrics.get("ocr_confidence", -1.0)
    if conf < 0:
        s_ocr = 100.0  # unknown → assume fine
    elif conf >= 90:
        s_ocr = 100.0
    elif conf >= 70:
        s_ocr = 70.0 + (conf - 70.0) * 1.5
    else:
        s_ocr = conf

    # 6. Layout — penalize fallbacks and high blank ratio
    blank_ratio    = metrics.get("blank_ratio", 0.0)
    fallback_pages = metrics.get("fallback_pages", 0)
    total_pages    = max(metrics.get("total_pages", 1), 1)
    fallback_ratio = fallback_pages / total_pages
    s_layout = max(0.0, 100.0 - blank_ratio * 20.0 - fallback_ratio * 30.0)

    weights = {
        "estructura": 0.20,
        "texto":      0.20,
        "imagenes":   0.15,
        "tablas":     0.10,
        "ocr":        0.10,
        "layout":     0.25,
    }
    scores = {
        "estructura": round(s_estructura, 1),
        "texto":      round(s_texto, 1),
        "imagenes":   round(s_imagenes, 1),
        "tablas":     round(s_tablas, 1),
        "ocr":        round(s_ocr, 1),
        "layout":     round(s_layout, 1),
    }
    total = sum(scores[k] * weights[k] for k in weights)
    scores["total"] = round(total, 1)
    scores["weights"] = weights
    return scores


def _score_label(score: float) -> str:
    if score >= 80:
        return "🟢 PASS"
    if score >= 60:
        return "🟡 WARN"
    return "🔴 FAIL"


def _score_emoji(score: float) -> str:
    if score >= 80:
        return "🟢"
    if score >= 60:
        return "🟡"
    return "🔴"


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def _render_report(metrics: dict, scores: dict, source: str) -> str:
    total = scores["total"]
    lines = [
        f"# Reporte de calidad — {source}",
        "",
        f"**Score total: {total}/100  {_score_label(total)}**",
        "",
        "## Dimensiones",
        "",
        "| Dimensión   | Score | Peso | Contribución |",
        "|-------------|------:|-----:|-------------:|",
    ]
    weights = scores["weights"]
    for dim in ("estructura", "texto", "imagenes", "tablas", "ocr", "layout"):
        s = scores[dim]
        w = weights[dim]
        contrib = round(s * w, 1)
        lines.append(f"| {dim:<11} | {s:>5.1f} | {w*100:>3.0f}% | {contrib:>11.1f} |")

    lines += [
        "",
        "## Métricas",
        "",
        f"- Páginas totales:       {metrics.get('total_pages', '?')}",
        f"- Páginas en blanco:     {metrics.get('blank_pages', '?')}",
        f"- Páginas OCR:           {metrics.get('ocr_pages', '?')}",
        f"- Encabezados:           {metrics.get('headings', '?')}",
        f"- Imágenes:              {metrics.get('images', '?')}",
        f"  - Con caption:         {metrics.get('captioned_images', '?')}",
        f"- Tablas:                {metrics.get('tables', '?')}",
        f"- Párrafos:              {metrics.get('paragraphs', '?')}",
    ]
    conf = metrics.get("ocr_confidence", -1.0)
    if conf >= 0:
        lines.append(f"- Confianza OCR:         {conf:.1f}%")

    fallback = metrics.get("fallback_pages", 0)
    if fallback:
        lines.append(f"- Fallback a OCR:        {fallback} páginas")

    lines += ["", "---", f"*Generado por validator.py — pdf-to-md skill*"]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Entry points
# ---------------------------------------------------------------------------

def validate_markdown(md_path: str, audit_path: Optional[str] = None) -> tuple:
    """Validate a finished conversion.  Returns (metrics, scores)."""
    md_text = Path(md_path).read_text(encoding="utf-8")
    audit_text = ""
    if audit_path and Path(audit_path).exists():
        audit_text = Path(audit_path).read_text(encoding="utf-8")

    headings   = _count_headings(md_text)
    images     = _count_images(md_text)
    captioned  = _count_captioned_images(md_text)
    tables     = _count_tables(md_text)

    # Page counts from audit
    pages = _parse_audit_pages(audit_text) if audit_text else {}
    total_pages  = pages.get("total", 0)
    blank_pages  = pages.get("blank", 0)
    ocr_pages    = pages.get("ocr", 0)
    fallback     = pages.get("fallback", 0)
    content_pages = max(total_pages - blank_pages, 1)

    # Estimate text coverage from paragraph count (heuristic: ≥3 paras per content page)
    para_count = len(re.findall(r"\n\n(?!\[|\*\[|!\[|#{1,3} |---|<!--).+", md_text))
    text_coverage = min(1.0, para_count / max(content_pages * 2, 1))

    ocr_conf = _parse_audit_confidence(audit_text) if audit_text else -1.0

    metrics = {
        "total_pages": total_pages,
        "blank_pages": blank_pages,
        "ocr_pages": ocr_pages,
        "fallback_pages": fallback,
        "headings": headings,
        "images": images,
        "captioned_images": captioned,
        "tables": tables,
        "paragraphs": para_count,
        "has_headings": headings > 0,
        "text_coverage": text_coverage,
        "image_cap_ratio": captioned / max(images, 1) if images else 1.0,
        "has_tables": tables > 0,
        "blank_ratio": blank_pages / max(total_pages, 1),
        "ocr_confidence": ocr_conf,
    }
    scores = compute_score(metrics)
    return metrics, scores


def validate_ir(ir_path: str) -> tuple:
    """Validate from a Layout IR JSON.  Returns (metrics, scores)."""
    ir = json.loads(Path(ir_path).read_text(encoding="utf-8"))
    metrics = _validate_ir(ir)
    scores  = compute_score(metrics)
    return metrics, scores


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Validate pdf-to-md conversion quality.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("md",    nargs="?", default=None, help="Markdown output file")
    group.add_argument("--ir",  default="",              help="Layout IR JSON file")
    parser.add_argument("--audit",  default="", help="Audit markdown (for MD validation)")
    parser.add_argument("--report", default="", help="Write JSON report to this path")
    parser.add_argument("--md-report", default="", help="Write Markdown report to this path")
    args = parser.parse_args()

    if args.ir:
        source = args.ir
        metrics, scores = validate_ir(args.ir)
    elif args.md:
        source = args.md
        metrics, scores = validate_markdown(args.md, args.audit or None)
    else:
        parser.print_help()
        sys.exit(1)

    total = scores["total"]
    print(_render_report(metrics, scores, source))

    if args.report:
        data = {"metrics": metrics, "scores": scores}
        Path(args.report).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\nJSON report → {args.report}")

    if args.md_report:
        Path(args.md_report).write_text(
            _render_report(metrics, scores, source), encoding="utf-8"
        )
        print(f"MD report → {args.md_report}")

    # Exit code based on score
    if total >= 80:
        sys.exit(0)
    elif total >= 60:
        sys.exit(1)
    else:
        sys.exit(2)


if __name__ == "__main__":
    main()
