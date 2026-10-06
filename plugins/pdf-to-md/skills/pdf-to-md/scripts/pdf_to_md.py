#!/usr/bin/env python3
"""
pdf_to_md.py — Extrae contenido de PDFs y genera Markdown + auditoría.

Maneja:
  - PDFs con texto nativo (pdfplumber)
  - PDFs escaneados / imagen-only (pdf2image + tesseract OCR)
  - PDFs mixtos (por página)
  - Tablas, imágenes embebidas, multi-columna, encabezados por font size
  - Filtrado de números de página y notas al pie
  - Extracción de captions bajo figuras
  - De-hifenación tipográfica

Salida:
  <output>/<output>.md              — Markdown del contenido
  <output>/<output>_audit.md       — Reporte de auditoría con quality score
  <output>/images/                 — Imágenes extraídas
"""

import argparse
import os
import sys
import re
import json
from pathlib import Path
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from typing import Optional

try:
    import pdfplumber
except ImportError:
    sys.exit("ERROR: pdfplumber no instalado. Corre: pip install pdfplumber")

try:
    from pdf2image import convert_from_path
except ImportError:
    sys.exit("ERROR: pdf2image no instalado. Corre: pip install pdf2image")

try:
    import pytesseract
    from PIL import Image, ImageEnhance, ImageFilter
except ImportError:
    sys.exit("ERROR: pytesseract o pillow no instalados.")


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class PageResult:
    page_num: int        # 1-based
    method: str          # "native", "ocr", "ocr_enhanced", "empty", "blank"
    text: str
    tables: list = field(default_factory=list)          # list of str (markdown tables)
    images: list = field(default_factory=list)          # list of image paths saved
    image_captions: list = field(default_factory=list)  # caption per image (parallel to images)
    ocr_confidence: Optional[float] = None
    columns_detected: int = 1
    headings_found: int = 0
    warnings: list = field(default_factory=list)
    errors: list = field(default_factory=list)


@dataclass
class ConversionAudit:
    pdf_path: str
    total_pages: int
    pdf_type: str        # "text", "scanned", "mixed", "text-with-ocr-fallback"
    lang: str
    pages_native: list = field(default_factory=list)
    pages_ocr: list = field(default_factory=list)
    pages_failed: list = field(default_factory=list)
    pages_blank: list = field(default_factory=list)
    tables_converted: int = 0
    images_extracted: int = 0
    headings_total: int = 0
    captions_total: int = 0
    two_col_pages: list = field(default_factory=list)
    warnings: list = field(default_factory=list)
    errors: list = field(default_factory=list)
    notes: list = field(default_factory=list)
    quality_scores: dict = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Basic helpers
# ---------------------------------------------------------------------------

# Regex para detectar números de página (dígitos o romanos, solos en una línea)
PAGE_NUM_RE = re.compile(r'^\s*([IVXLCDM]{1,8}|\d{1,4})\s*$', re.IGNORECASE)


def is_text_page(page, min_chars: int = 50) -> bool:
    """Retorna True si la página tiene texto nativo extraíble."""
    try:
        text = page.extract_text() or ""
        return len(text.strip()) >= min_chars
    except Exception:
        return False


def text_quality_score(text: str) -> float:
    """Estima la calidad del texto: 0.0 (ilegible) a 1.0 (limpio)."""
    if not text or len(text.strip()) < 10:
        return 0.0
    total = len(text)
    good = sum(
        1 for c in text
        if c.isalnum() or c in " \n\t.,;:()¿?¡!\"'/-_@%$#*+&áéíóúÁÉÍÓÚüÜñÑ"
    )
    return good / total


def page_rotation(page) -> int:
    """Retorna la rotación de la página en grados (0, 90, 180, 270)."""
    try:
        return int(page.rotation or 0)
    except Exception:
        return 0


def has_font_encoding_artifacts(text: str) -> bool:
    """
    Detecta artefactos de fuentes personalizadas (logo/icon fonts) donde los
    glifos visuales no coinciden con los Unicode del stream.
    """
    first_words = text.split()[:5]
    suspicious_count = 0
    for word in first_words:
        if re.search(r'[A-Z]{2,}[a-z]|[a-z][A-Z][a-z]', word):
            suspicious_count += 1
        if re.search(r'\d[a-z]{2,}', word):
            suspicious_count += 1
    return suspicious_count >= 2


def has_cid_encoding(text: str) -> tuple:
    """
    Detecta tokens CID sin mapeo Unicode como '(cid:0)', '(cid:32)'.
    Retorna (True, razón) si >10% de los caracteres son CID.
    """
    cid_matches = re.findall(r'\(cid:\d+\)', text)
    cid_count = len(cid_matches)
    if cid_count == 0:
        return False, ""
    total_chars = max(len(text.strip()), 1)
    cid_chars = sum(len(m) for m in cid_matches)
    ratio = cid_chars / total_chars
    if ratio > 0.10 or cid_count > 5:
        return True, f"Encoding CID sin mapeo Unicode ({cid_count} tokens CID)"
    return False, ""


def needs_ocr_fallback(text: str, rotation: int, quality_threshold: float = 0.75) -> tuple:
    """Decide si una página con texto nativo debería procesarse por OCR."""
    if rotation != 0:
        return True, f"Página rotada {rotation}° — extracción nativa poco confiable"
    cid_detected, cid_reason = has_cid_encoding(text)
    if cid_detected:
        return True, cid_reason
    score = text_quality_score(text)
    if score < quality_threshold and len(text.strip()) > 20:
        return True, f"Calidad de texto baja ({score:.0%}) — posible encoding corrupto"
    if has_font_encoding_artifacts(text):
        return True, "Artefactos de fuente personalizada detectados — OCR más fiel"
    return False, ""


def preprocess_image_for_ocr(img: "Image.Image") -> "Image.Image":
    """Mejora la imagen para OCR: contraste, escala de grises, sharpening."""
    img = img.convert("L")
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2.0)
    img = img.filter(ImageFilter.SHARPEN)
    return img


def table_to_markdown(table: list) -> str:
    """Convierte una tabla de pdfplumber (list of list) a Markdown."""
    if not table or not table[0]:
        return ""
    cleaned = []
    for row in table:
        cleaned.append([str(cell).strip() if cell is not None else "" for cell in row])
    if not cleaned:
        return ""
    header = cleaned[0]
    sep = ["---"] * len(header)
    rows = cleaned[1:]
    lines = [
        "| " + " | ".join(header) + " |",
        "| " + " | ".join(sep) + " |",
    ]
    for row in rows:
        while len(row) < len(header):
            row.append("")
        lines.append("| " + " | ".join(row[:len(header)]) + " |")
    return "\n".join(lines)


def ocr_page(img: "Image.Image", lang: str, enhance: bool = False) -> tuple:
    """OCR sobre una imagen. Retorna (texto, confianza_promedio 0-100)."""
    if enhance:
        img = preprocess_image_for_ocr(img)
    try:
        data = pytesseract.image_to_data(img, lang=lang, output_type=pytesseract.Output.DICT)
        texts, confs = [], []
        for i, conf in enumerate(data["conf"]):
            try:
                c = int(conf)
            except (ValueError, TypeError):
                continue
            if c > 0:
                confs.append(c)
                texts.append(data["text"][i])
        avg_conf = sum(confs) / len(confs) if confs else 0.0
        text = " ".join(t for t in texts if t.strip())
        return text, avg_conf
    except Exception:
        try:
            text = pytesseract.image_to_string(img, lang=lang)
            return text, -1.0
        except Exception:
            return "", 0.0


# ---------------------------------------------------------------------------
# Layout analysis helpers
# ---------------------------------------------------------------------------

def dehyphenate(text: str) -> str:
    """Resuelve guiones tipográficos de justificación al final de línea.
    'estableci-\nmiento' → 'establecimiento\n'
    """
    return re.sub(r'(\w)-\n(\w)', r'\1\2\n', text)


def detect_columns(page) -> int:
    """
    Detecta si la página tiene 1 o 2 columnas de texto.
    Estrategia: si ambas mitades (±20pt del centro) tienen ≥5 palabras
    y la mitad derecha tiene al menos 30% de palabras que la izquierda → 2 columnas.
    """
    try:
        words = page.extract_words()
        if len(words) < 10:
            return 1
        mid = float(page.width) / 2.0
        left_words  = sum(1 for w in words if (w['x0'] + w['x1']) / 2 < mid - 20)
        right_words = sum(1 for w in words if (w['x0'] + w['x1']) / 2 > mid + 20)
        if (left_words >= 5 and right_words >= 5
                and right_words / max(left_words, 1) > 0.3):
            return 2
        return 1
    except Exception:
        return 1


def get_body_font_size(page) -> float:
    """Retorna el font size más frecuente de la página (= cuerpo del texto)."""
    try:
        sizes = [round(c.get('size', 0)) for c in page.chars if c.get('size', 0) > 4]
        if not sizes:
            return 10.0
        return float(Counter(sizes).most_common(1)[0][0])
    except Exception:
        return 10.0


def build_line_size_map(page) -> dict:
    """
    Construye mapa {top_y_bucket → font_size_promedio} usando page.chars.
    Permite saber el font size de cualquier línea dada su coordenada Y.
    """
    line_sizes = defaultdict(list)
    try:
        for c in page.chars:
            top = c.get('top', 0)
            size = c.get('size', 0)
            if size > 4:
                key = round(top / 2) * 2   # bucket 2pt
                line_sizes[key].append(size)
    except Exception:
        pass
    return {k: sum(v) / len(v) for k, v in line_sizes.items()}


def is_list_bullet(text: str) -> bool:
    """Detecta si una línea comienza con un marcador de lista."""
    stripped = text.strip()
    # Viñetas: •, –, —, -, *
    if re.match(r'^[•–—\-\*]\s+\S', stripped):
        return True
    # Listas numeradas: "1. texto", "a. texto"
    if re.match(r'^(\d+|[a-z])\.\s+\S', stripped):
        return True
    return False


def normalize_bullet(text: str) -> str:
    """Normaliza distintos tipos de viñeta al formato Markdown '- '."""
    # Viñeta tipográfica → dash
    text = re.sub(r'^[•–—]\s+', '- ', text.strip())
    # Guión simple → dash (si ya empieza con -)
    if text.startswith('- '):
        return text
    # Listas numeradas: mantener tal cual
    return text


def words_to_lines(words: list) -> list:
    """
    Agrupa palabras de pdfplumber en líneas lógicas por proximidad Y (±4pt).
    Retorna lista de dicts: {text, top, x0, x1, bottom}
    """
    if not words:
        return []
    words_sorted = sorted(words, key=lambda w: (round(w['top'] / 3) * 3, w['x0']))
    lines = []
    curr_top = None
    curr_line = []
    for w in words_sorted:
        wtop = round(w['top'] / 3) * 3
        if curr_top is None or abs(wtop - curr_top) > 4:
            if curr_line:
                text = ' '.join(cw['text'] for cw in curr_line)
                lines.append({
                    'text': text,
                    'top': curr_line[0]['top'],
                    'x0': min(cw['x0'] for cw in curr_line),
                    'x1': max(cw['x1'] for cw in curr_line),
                    'bottom': max(cw['bottom'] for cw in curr_line),
                })
            curr_line = [w]
            curr_top = wtop
        else:
            curr_line.append(w)
    if curr_line:
        text = ' '.join(cw['text'] for cw in curr_line)
        lines.append({
            'text': text,
            'top': curr_line[0]['top'],
            'x0': min(cw['x0'] for cw in curr_line),
            'x1': max(cw['x1'] for cw in curr_line),
            'bottom': max(cw['bottom'] for cw in curr_line),
        })
    return lines


def layout_extract_text(page, num_cols: int, table_bboxes: list = None) -> tuple:
    """
    Extrae texto respetando el layout de la página:
    - Separación de columnas (1 o 2)
    - Encabezados detectados por font size (##, ###)
    - Filtrado de números de página (top/bottom 8%)
    - Notas al pie como blockquote (área inferior + font size menor)
    - Listas/viñetas detectadas
    Retorna (texto_markdown, headings_count)
    """
    body_size = get_body_font_size(page)
    line_size_map = build_line_size_map(page)
    page_height = float(page.height)
    page_mid_x = float(page.width) / 2.0

    try:
        words = page.extract_words(x_tolerance=3, y_tolerance=3)
    except Exception:
        raw = page.extract_text() or ""
        return raw, 0

    # Filtrar palabras en zonas de tablas para evitar duplicados
    if table_bboxes:
        def _in_table(w):
            wx0, wy0, wx1, wy1 = w['x0'], w['top'], w['x1'], w['bottom']
            return any(
                tx0 <= wx0 and ty0 <= wy0 and wx1 <= tx1 and wy1 <= ty1
                for (tx0, ty0, tx1, ty1) in table_bboxes
            )
        words = [w for w in words if not _in_table(w)]

    # Separar en columnas
    if num_cols == 2:
        col1_words = [w for w in words if (w['x0'] + w['x1']) / 2 < page_mid_x]
        col2_words = [w for w in words if (w['x0'] + w['x1']) / 2 >= page_mid_x]
        all_lines = words_to_lines(col1_words) + words_to_lines(col2_words)
    else:
        all_lines = words_to_lines(words)

    output_parts = []
    headings_count = 0

    for line in all_lines:
        text = line['text'].strip()
        if not text:
            continue

        top = line['top']
        y_ratio = top / page_height if page_height > 0 else 0.5

        # ── Filtrar números de página (franja top/bottom 8%) ────────────
        if PAGE_NUM_RE.match(text) and (y_ratio < 0.08 or y_ratio > 0.92):
            continue

        # ── Obtener font size de la línea ───────────────────────────────
        line_key = round(top / 2) * 2
        line_font_size = line_size_map.get(line_key, body_size)

        # ── Notas al pie: área inferior >82% y font size menor al body ──
        if y_ratio > 0.82 and line_font_size < body_size - 0.5:
            output_parts.append(f"> {text}")
            continue

        # ── Listas / viñetas ────────────────────────────────────────────
        if is_list_bullet(text):
            output_parts.append(normalize_bullet(text))
            continue

        # ── Headings por font size ──────────────────────────────────────
        if line_font_size > body_size + 4:
            output_parts.append(f"# {text}")
            headings_count += 1
        elif line_font_size > body_size + 2:
            output_parts.append(f"## {text}")
            headings_count += 1
        elif line_font_size > body_size + 0.5:
            output_parts.append(f"### {text}")
            headings_count += 1
        else:
            output_parts.append(text)

    return '\n\n'.join(output_parts), headings_count


def find_caption(figure_bbox: tuple, words: list, margin: float = 28.0) -> str:
    """
    Encuentra el texto inmediatamente debajo de una figura (dentro de `margin` puntos).
    Retorna el texto del caption o cadena vacía.
    """
    fx0, fy0, fx1, fy1 = figure_bbox
    caption_words = [
        w for w in words
        if fy1 < w['top'] < fy1 + margin
        and fx0 - 15 < (w['x0'] + w['x1']) / 2 < fx1 + 15
    ]
    if not caption_words:
        return ""
    caption_sorted = sorted(caption_words, key=lambda w: (round(w['top'] / 3) * 3, w['x0']))
    return ' '.join(w['text'] for w in caption_sorted)


# ---------------------------------------------------------------------------
# Image clustering helpers
# ---------------------------------------------------------------------------

MIN_IMAGE_SIDE = 40        # pt — por debajo de esto son viñetas o bordes
MIN_IMAGE_AREA = 5000      # pt² — descarta franjas delgadas
CLUSTER_GAP = 6            # pt — separación máxima entre fragmentos de la misma figura
CROP_DPI = 150             # DPI para recortar figuras del render de página


def _boxes_are_related(a: tuple, b: tuple, gap: float = CLUSTER_GAP) -> bool:
    """True si dos bboxes se solapan o están lo bastante cerca."""
    ax0, ay0, ax1, ay1 = a
    bx0, by0, bx1, by1 = b
    overlap_x = ax0 - gap <= bx1 and bx0 - gap <= ax1
    overlap_y = ay0 - gap <= by1 and by0 - gap <= ay1
    return overlap_x and overlap_y


def cluster_image_regions(page_images: list) -> list:
    """
    Agrupa objetos-imagen en figuras visuales y retorna un bbox por figura.
    Usa union-find para agrupar fragmentos adyacentes.
    """
    boxes = []
    for img in page_images:
        try:
            x0, top = img.get("x0", 0), img.get("top", 0)
            x1, bottom = img.get("x1", 0), img.get("bottom", 0)
            if x1 <= x0 or bottom <= top:
                continue
            boxes.append((float(x0), float(top), float(x1), float(bottom)))
        except Exception:
            continue

    if not boxes:
        return []

    parent = list(range(len(boxes)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    def union(i, j):
        ri, rj = find(i), find(j)
        if ri != rj:
            parent[rj] = ri

    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            if _boxes_are_related(boxes[i], boxes[j]):
                union(i, j)

    groups = {}
    for idx, box in enumerate(boxes):
        root = find(idx)
        if root not in groups:
            groups[root] = list(box)
        else:
            g = groups[root]
            g[0] = min(g[0], box[0])
            g[1] = min(g[1], box[1])
            g[2] = max(g[2], box[2])
            g[3] = max(g[3], box[3])

    regions = []
    for g in groups.values():
        w, h = g[2] - g[0], g[3] - g[1]
        if w < MIN_IMAGE_SIDE or h < MIN_IMAGE_SIDE:
            continue
        if w * h < MIN_IMAGE_AREA:
            continue
        regions.append(tuple(g))

    regions.sort(key=lambda r: (round(r[1]), r[0]))
    return regions


def crop_regions_from_page(page, page_render, regions: list,
                           images_dir: Path, page_num: int) -> list:
    """
    Recorta cada región del render de la página y la guarda como PNG.
    Retorna las rutas relativas guardadas.
    """
    saved = []
    if page_render is None or not regions:
        return saved

    scale_x = page_render.width / float(page.width)
    scale_y = page_render.height / float(page.height)

    for idx, (x0, top, x1, bottom) in enumerate(regions):
        try:
            box = (
                max(0, int(x0 * scale_x)),
                max(0, int(top * scale_y)),
                min(page_render.width, int(x1 * scale_x)),
                min(page_render.height, int(bottom * scale_y)),
            )
            if box[2] - box[0] < 10 or box[3] - box[1] < 10:
                continue
            crop = page_render.crop(box)
            fname = f"fig_p{page_num}_{idx + 1}.png"
            crop.save(images_dir / fname)
            saved.append(f"images/{fname}")
        except Exception:
            continue
    return saved


def save_image_from_page(img_obj, images_dir: Path, page_num: int, idx: int) -> Optional[str]:
    """Guarda una imagen extraída de pdfplumber. Retorna la ruta relativa."""
    try:
        if hasattr(img_obj, "stream"):
            data = img_obj.stream.get_data()
        elif "stream" in img_obj:
            data = img_obj["stream"].get_data()
        else:
            return None
        fname = f"img_p{page_num}_{idx}.png"
        fpath = images_dir / fname
        with open(fpath, "wb") as f:
            f.write(data)
        return f"images/{fname}"
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Core extraction
# ---------------------------------------------------------------------------

def extract_page_native(page, page_num: int, images_dir: Path, extract_images: bool,
                        page_render=None) -> PageResult:
    """Extrae contenido de una página con texto nativo con análisis de layout."""
    result = PageResult(page_num=page_num, method="native", text="")

    # --- Tablas primero ---
    table_bboxes = []
    try:
        tables = page.extract_tables()
        if tables:
            for t in tables:
                md_table = table_to_markdown(t)
                if md_table:
                    result.tables.append(md_table)
        for finder in (page.find_tables() if hasattr(page, "find_tables") else []):
            table_bboxes.append(finder.bbox)
    except Exception as e:
        result.warnings.append(f"No se pudieron extraer tablas: {e}")

    # --- Texto con análisis de layout (columnas, encabezados, filtros) ---
    try:
        num_cols = detect_columns(page)
        result.columns_detected = num_cols
        text, headings_count = layout_extract_text(page, num_cols, table_bboxes)
        text = dehyphenate(text)
        result.text = text.strip()
        result.headings_found = headings_count
    except Exception as e:
        result.warnings.append(f"Análisis de layout falló ({e}), usando extracción básica")
        # Fallback al método original
        try:
            if table_bboxes:
                words = page.extract_words(x_tolerance=3, y_tolerance=3)
                filtered_words = []
                for w in words:
                    wx0, wy0, wx1, wy1 = w["x0"], w["top"], w["x1"], w["bottom"]
                    in_table = any(
                        tx0 <= wx0 and ty0 <= wy0 and wx1 <= tx1 and wy1 <= ty1
                        for (tx0, ty0, tx1, ty1) in table_bboxes
                    )
                    if not in_table:
                        filtered_words.append(w["text"])
                text = " ".join(filtered_words)
            else:
                text = page.extract_text(x_tolerance=3, y_tolerance=3) or ""
            result.text = text.strip()
        except Exception as e2:
            result.errors.append(f"Error extrayendo texto: {e2}")
            result.text = ""

    # --- Figuras embebidas ---
    if extract_images:
        try:
            page_words = page.extract_words()  # para encontrar captions
            regions = cluster_image_regions(page.images)

            if regions and page_render is not None:
                saved = crop_regions_from_page(page, page_render, regions, images_dir, page_num)
                result.images.extend(saved)
                # Extraer caption para cada figura guardada
                for region in regions[:len(saved)]:
                    cap = find_caption(region, page_words)
                    result.image_captions.append(cap)
            elif regions:
                # Fallback: extraer streams individuales
                for idx, img in enumerate(page.images):
                    saved_path = save_image_from_page(img, images_dir, page_num, idx)
                    if saved_path:
                        result.images.append(saved_path)
                        result.image_captions.append("")
            # Asegurar que image_captions tenga el mismo largo que images
            while len(result.image_captions) < len(result.images):
                result.image_captions.append("")

        except Exception as e:
            result.warnings.append(f"No se pudieron extraer figuras: {e}")

    return result


def is_blank_page(page) -> bool:
    """
    Determina si una página está genuinamente en blanco.
    Sin texto, sin imágenes, sin elementos vectoriales significativos.
    """
    try:
        text = (page.extract_text() or "").strip()
        if text:
            return False
        if len(page.images) > 0:
            return False
        if len(page.rects) + len(page.curves) + len(page.lines) > 2:
            return False
        return True
    except Exception:
        return False


def blank_page_result(page_num: int) -> PageResult:
    """Resultado para una página en blanco: no es error ni advertencia."""
    return PageResult(page_num=page_num, method="blank", text="")


def extract_page_ocr(page_image: "Image.Image", page_num: int, lang: str) -> PageResult:
    """Extrae contenido de una página escaneada mediante OCR."""
    text, conf = ocr_page(page_image, lang, enhance=False)

    if conf < 60 and conf >= 0:
        text2, conf2 = ocr_page(page_image, lang, enhance=True)
        if conf2 > conf:
            text, conf = text2, conf2
            method = "ocr_enhanced"
        else:
            method = "ocr"
    else:
        method = "ocr"

    result = PageResult(
        page_num=page_num,
        method=method,
        text=text.strip(),
        ocr_confidence=round(conf, 1) if conf >= 0 else None,
    )

    if not result.text:
        result.method = "blank"
        result.ocr_confidence = None
        return result

    if conf >= 0 and conf < 50:
        result.warnings.append(f"Confianza OCR baja ({conf:.0f}%). Posibles errores.")
    if conf >= 0 and conf < 30:
        result.errors.append("Confianza OCR muy baja (<30%). Imagen de baja calidad.")

    return result


# ---------------------------------------------------------------------------
# Main converter
# ---------------------------------------------------------------------------

def convert_pdf(
    pdf_path: str,
    output_name: str,
    lang: str = "spa+eng",
    dpi: int = 300,
    ocr_only: bool = False,
    extract_images: bool = True,
    save_ir: bool = False,
) -> tuple:
    """
    Convierte un PDF a Markdown con análisis de layout.
    Retorna (ruta_md, ruta_audit_md).
    """
    pdf_path = Path(pdf_path).resolve()
    output_dir = pdf_path.parent / output_name
    output_dir.mkdir(parents=True, exist_ok=True)

    images_dir = output_dir / "images"
    if extract_images:
        images_dir.mkdir(exist_ok=True)

    md_path    = output_dir / f"{output_name}.md"
    audit_path = output_dir / f"{output_name}_audit.md"
    ir_path    = output_dir / "ir.json" if save_ir else None

    audit = ConversionAudit(
        pdf_path=str(pdf_path),
        total_pages=0,
        pdf_type="unknown",
        lang=lang,
    )

    page_results = []
    blank_pages = set()

    # --- Abrir PDF ---
    try:
        pdf = pdfplumber.open(str(pdf_path))
    except Exception as e:
        error_msg = str(e).lower()
        if "encrypt" in error_msg or "password" in error_msg:
            audit.errors.append("El PDF está protegido/encriptado. Desbloquearlo antes de convertir.")
        else:
            audit.errors.append(f"No se pudo abrir el PDF: {e}")
        _write_failed_outputs(md_path, audit_path, audit)
        return str(md_path), str(audit_path)

    audit.total_pages = len(pdf.pages)

    # --- Determinar tipo de PDF ---
    if ocr_only:
        audit.pdf_type = "scanned (forzado por --ocr-only)"
        text_pages = []
        scan_pages = list(range(len(pdf.pages)))
        rotation_info = {}
    else:
        rotation_info = {}
        ocr_forced_pages = set()
        text_pages_raw = []

        for i, p in enumerate(pdf.pages):
            if is_blank_page(p):
                blank_pages.add(i)
                continue

            rot = page_rotation(p)
            rotation_info[i] = rot
            if rot != 0:
                audit.warnings.append((i + 1, f"Página rotada {rot}° — se usará OCR"))

            if is_text_page(p):
                preview = (p.extract_text() or "")[:500]
                force_ocr, reason = needs_ocr_fallback(preview, rot)
                if force_ocr:
                    ocr_forced_pages.add(i)
                    audit.warnings.append((i + 1, f"Fallback a OCR: {reason}"))
                else:
                    text_pages_raw.append(i)

        text_pages = text_pages_raw
        scan_pages = [
            i for i in range(len(pdf.pages))
            if i not in text_pages and i not in blank_pages
        ]

        if not scan_pages:
            audit.pdf_type = "text"
        elif not text_pages:
            audit.pdf_type = "scanned" if not ocr_forced_pages else "text-with-ocr-fallback"
        else:
            audit.pdf_type = "mixed"

        if ocr_forced_pages:
            audit.notes.append(
                f"Páginas con fallback OCR: {sorted(p+1 for p in ocr_forced_pages)}"
            )

    audit.notes.append(
        f"Tipo detectado: {audit.pdf_type} — "
        f"{len(text_pages)} pág. con texto nativo, "
        f"{len(scan_pages)} pág. procesadas por OCR"
    )

    # --- Renderizar para OCR ---
    page_images = {}
    if scan_pages:
        try:
            audit.notes.append(f"Renderizando {len(scan_pages)} pág. para OCR a {dpi} DPI…")
            all_images = convert_from_path(str(pdf_path), dpi=dpi)
            for i in scan_pages:
                if i < len(all_images):
                    page_images[i] = all_images[i]
        except Exception as e:
            audit.errors.append(f"No se pudieron renderizar páginas para OCR: {e}")

    # --- Renderizar páginas con figuras para recorte limpio ---
    figure_renders = {}
    if extract_images and text_pages:
        pages_with_figures = [i for i in text_pages if len(pdf.pages[i].images) > 0]
        if pages_with_figures:
            try:
                audit.notes.append(
                    f"Renderizando {len(pages_with_figures)} pág. con figuras a {CROP_DPI} DPI…"
                )
                first = min(pages_with_figures) + 1
                last  = max(pages_with_figures) + 1
                rendered = convert_from_path(
                    str(pdf_path), dpi=CROP_DPI, first_page=first, last_page=last
                )
                for i in pages_with_figures:
                    offset = i - (first - 1)
                    if 0 <= offset < len(rendered):
                        figure_renders[i] = rendered[offset]
            except Exception as e:
                audit.warnings.append(
                    (0, f"No se pudieron renderizar figuras ({e}). Se extraerán fragmentos.")
                )

    # --- Extraer página por página ---
    ir_data = []  # para --save-ir
    for i, page in enumerate(pdf.pages):
        page_num = i + 1

        if i in blank_pages:
            res = blank_page_result(page_num)
            audit.pages_blank.append(page_num)
        elif i in text_pages:
            res = extract_page_native(
                page, page_num, images_dir, extract_images,
                page_render=figure_renders.get(i)
            )
            audit.pages_native.append(page_num)
            if res.columns_detected == 2:
                audit.two_col_pages.append(page_num)
        elif i in page_images:
            res = extract_page_ocr(page_images[i], page_num, lang)
            if res.method == "blank":
                audit.pages_blank.append(page_num)
            else:
                audit.pages_ocr.append(page_num)
        else:
            res = PageResult(page_num=page_num, method="empty", text="")
            res.warnings.append("Sin texto nativo ni imagen para OCR.")
            audit.pages_failed.append(page_num)

        audit.images_extracted += len(res.images)
        audit.tables_converted += len(res.tables)
        audit.headings_total += res.headings_found
        audit.captions_total += sum(1 for c in res.image_captions if c)
        audit.warnings.extend([(page_num, w) for w in res.warnings])
        audit.errors.extend([(page_num, e) for e in res.errors])

        page_results.append(res)

        # IR debug
        if save_ir:
            ir_data.append({
                "page": page_num,
                "method": res.method,
                "columns": res.columns_detected,
                "headings": res.headings_found,
                "images": res.images,
                "image_captions": res.image_captions,
                "text_preview": res.text[:300] if res.text else "",
            })

    pdf.close()

    # --- Calcular quality scores ---
    audit.quality_scores = _compute_quality_scores(audit, page_results)

    # --- Escribir Markdown principal ---
    _write_markdown(md_path, page_results, audit)

    # --- Escribir auditoría ---
    _write_audit(audit_path, audit, page_results)

    # --- IR debug ---
    if save_ir and ir_path:
        with open(ir_path, "w", encoding="utf-8") as f:
            json.dump(ir_data, f, ensure_ascii=False, indent=2)

    return str(md_path), str(audit_path)


# ---------------------------------------------------------------------------
# Quality score
# ---------------------------------------------------------------------------

def _compute_quality_scores(audit: ConversionAudit, results: list) -> dict:
    """Calcula quality score 0–100 por dimensión y total ponderado."""
    total = audit.total_pages
    content_pages = total - len(audit.pages_blank)
    if content_pages == 0:
        content_pages = 1

    # Estructura: ¿hay headings en páginas nativas?
    estructura = 100 if audit.headings_total > 0 else 30

    # Texto: cobertura (nativas + OCR) vs total de páginas con contenido
    covered = len(audit.pages_native) + len(audit.pages_ocr)
    texto = min(100, int(covered / content_pages * 100))

    # Imágenes: OK si no hay imágenes (N/A), penalizar solo si hay figuras sin captions
    if audit.images_extracted == 0:
        imagenes = 100  # N/A
    else:
        cap_ratio = audit.captions_total / audit.images_extracted
        imagenes = min(100, int(50 + cap_ratio * 50))

    # Tablas: N/A = 100 si no hay tablas en el documento
    tablas = 100

    # OCR: promedio de confianzas
    ocr_confs = [r.ocr_confidence for r in results
                 if r.ocr_confidence is not None and r.ocr_confidence >= 0]
    if not ocr_confs:
        ocr_score = 100  # N/A (no hubo páginas OCR)
    else:
        avg_conf = sum(ocr_confs) / len(ocr_confs)
        ocr_score = min(100, int(avg_conf))

    # Layout: penalizar por errores y advertencias detectadas
    layout = 100
    if audit.pages_failed:
        layout -= len(audit.pages_failed) * 10
    layout = max(0, layout)
    # Extra: si hay dos_col_pages, el layout fue detectado y manejado → bonus
    if audit.two_col_pages:
        layout = min(100, layout + 5)

    total_score = int(
        estructura * 0.20
        + texto     * 0.20
        + imagenes  * 0.15
        + tablas    * 0.10
        + ocr_score * 0.10
        + layout    * 0.25
    )

    return {
        "estructura": estructura,
        "texto":      texto,
        "imagenes":   imagenes,
        "tablas":     tablas,
        "ocr":        ocr_score,
        "layout":     layout,
        "total":      total_score,
    }


# ---------------------------------------------------------------------------
# Output writers
# ---------------------------------------------------------------------------

def detect_code_blocks(text: str) -> str:
    """Detecta líneas de terminal/código y las envuelve en bloques Markdown."""
    code_starters = (
        "curl ", "wget ", "pip ", "pip3 ", "npm ", "npx ", "yarn ",
        "python ", "python3 ", "node ", "ruby ", "java ",
        "sudo ", "apt ", "apt-get ", "brew ", "docker ",
        "git ", "cd ", "ls ", "mkdir ", "cp ", "mv ", "rm ",
        "export ", "echo ", "cat ", "grep ", "sed ", "awk ",
        "#!/", "$ ", "% ",
    )
    lines = text.split("\n")
    result_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if stripped and any(stripped.startswith(s) for s in code_starters):
            block = [stripped]
            j = i + 1
            while j < len(lines) and lines[j].strip() and any(
                lines[j].strip().startswith(s) for s in code_starters
            ):
                block.append(lines[j].strip())
                j += 1
            result_lines.append("```bash")
            result_lines.extend(block)
            result_lines.append("```")
            i = j
        else:
            result_lines.append(line)
            i += 1
    return "\n".join(result_lines)


def _write_markdown(path: Path, results: list, audit: ConversionAudit):
    lines = []
    lines.append(f"<!-- Convertido desde: {Path(audit.pdf_path).name} -->")
    lines.append(f"<!-- Tipo PDF: {audit.pdf_type} | Páginas: {audit.total_pages} -->")
    lines.append("")

    for res in results:
        lines.append(f"\n---\n<!-- Página {res.page_num} ({res.method}) -->\n")

        if res.method in ("ocr", "ocr_enhanced") and res.ocr_confidence is not None:
            if res.ocr_confidence < 60:
                lines.append(
                    f"> ⚠️ **OCR de baja confianza** ({res.ocr_confidence:.0f}%) — "
                    "el texto puede contener errores\n"
                )

        # Texto principal
        if res.text:
            lines.append(detect_code_blocks(res.text))
            lines.append("")

        # Tablas
        for tbl in res.tables:
            lines.append("\n" + tbl + "\n")

        # Imágenes (con caption si está disponible)
        for i, img_path in enumerate(res.images):
            caption = res.image_captions[i] if i < len(res.image_captions) else ""
            lines.append(f"\n![Imagen extraída de página {res.page_num}]({img_path})")
            if caption:
                lines.append(f"*{caption}*\n")
            else:
                lines.append(f"*Imagen de página {res.page_num} — ver auditoría para descripción*\n")

        if not res.text and not res.tables and not res.images:
            if res.method == "blank":
                lines.append(f"*[Página {res.page_num}: en blanco en el documento original]*\n")
            else:
                lines.append(f"*[Página {res.page_num}: sin contenido extraíble]*\n")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def _write_audit(path: Path, audit: ConversionAudit, results: list):
    lines = []
    lines.append(f"# Auditoría de conversión — {Path(audit.pdf_path).name}")
    lines.append("")
    lines.append("## Resumen del proceso")
    lines.append("")
    lines.append("| Campo | Valor |")
    lines.append("|-------|-------|")
    lines.append(f"| Archivo fuente | `{audit.pdf_path}` |")
    lines.append(f"| Tipo de PDF | **{audit.pdf_type}** |")
    lines.append(f"| Total de páginas | {audit.total_pages} |")
    lines.append(f"| Idioma OCR | `{audit.lang}` |")
    lines.append(f"| Páginas con texto nativo | {len(audit.pages_native)} |")
    lines.append(f"| Páginas con OCR | {len(audit.pages_ocr)} |")
    if audit.pages_blank:
        lines.append(f"| Páginas en blanco (original) | {len(audit.pages_blank)} |")
    lines.append(f"| Páginas fallidas | {len(audit.pages_failed)} |")
    lines.append(f"| Tablas convertidas | {audit.tables_converted} |")
    lines.append(f"| Imágenes extraídas | {audit.images_extracted} |")
    lines.append(f"| Captions extraídas | {audit.captions_total} |")
    lines.append(f"| Encabezados detectados | {audit.headings_total} |")
    if audit.two_col_pages:
        lines.append(f"| Páginas 2-col detectadas | {len(audit.two_col_pages)} ({audit.two_col_pages}) |")
    lines.append("")

    # Quality Score
    qs = audit.quality_scores
    if qs:
        total = qs.get("total", 0)
        emoji = "🟢" if total >= 80 else ("🟡" if total >= 60 else "🔴")
        lines.append(f"## {emoji} Quality Score: {total}/100")
        lines.append("")
        lines.append("| Dimensión | Peso | Score |")
        lines.append("|-----------|------|-------|")
        lines.append(f"| Estructura | 20% | {qs.get('estructura', 0)}/100 |")
        lines.append(f"| Texto | 20% | {qs.get('texto', 0)}/100 |")
        lines.append(f"| Imágenes | 15% | {qs.get('imagenes', 0)}/100 |")
        lines.append(f"| Tablas | 10% | {qs.get('tablas', 0)}/100 |")
        lines.append(f"| OCR | 10% | {qs.get('ocr', 0)}/100 |")
        lines.append(f"| Layout | 25% | {qs.get('layout', 0)}/100 |")
        lines.append("")
        if total >= 80:
            lines.append("> ✅ **Excelente** — listo para uso directo")
        elif total >= 60:
            lines.append("> 🟡 **Aceptable** — revisión de secciones WARNING recomendada")
        else:
            lines.append("> 🔴 **Conversión parcial** — revisar con el PDF original")
        lines.append("")

    # Notas del proceso
    if audit.notes:
        lines.append("## 📝 Notas del proceso")
        lines.append("")
        for note in audit.notes:
            lines.append(f"- {note}")
        lines.append("")

    # Páginas exitosas
    if audit.pages_native:
        pages_str = _format_page_ranges(audit.pages_native)
        lines.append("## ✅ Conversión directa (texto nativo)")
        lines.append("")
        lines.append(f"Páginas {pages_str} fueron extraídas directamente sin OCR.")
        lines.append("")

    # Páginas en blanco
    if audit.pages_blank:
        pages_str = _format_page_ranges(audit.pages_blank)
        lines.append("## ⬜ Páginas en blanco (sin contenido en el original)")
        lines.append("")
        lines.append(
            f"Páginas {pages_str} están en blanco en el PDF original "
            f"(versos de impresión o separadores de sección). "
            f"**No representan contenido perdido.**"
        )
        lines.append("")

    # Páginas OCR
    if audit.pages_ocr:
        lines.append("## 🔶 Conversión por OCR (imagen → texto)")
        lines.append("")
        lines.append("Estas páginas no tenían texto nativo y se procesaron con tesseract:\n")
        for res in results:
            if res.page_num in audit.pages_ocr:
                conf_str = (
                    f"{res.ocr_confidence:.0f}% confianza"
                    if res.ocr_confidence is not None else "confianza no disponible"
                )
                icon = "✅" if (res.ocr_confidence or 0) >= 70 else (
                    "🟡" if (res.ocr_confidence or 0) >= 50 else "❌"
                )
                lines.append(f"- {icon} Página {res.page_num}: {conf_str}")
        lines.append("")
        lines.append(
            "> **Nota:** OCR puede contener errores tipográficos en fuentes inusuales "
            "o texto muy pequeño."
        )
        lines.append("")

    # Páginas fallidas
    if audit.pages_failed:
        pages_str = _format_page_ranges(audit.pages_failed)
        lines.append("## ❌ Páginas sin conversión exitosa")
        lines.append("")
        lines.append(f"Páginas {pages_str} no pudieron convertirse:")
        lines.append("")
        for res in results:
            if res.page_num in audit.pages_failed:
                for err in res.errors or ["Sin información disponible"]:
                    lines.append(f"- Página {res.page_num}: {err}")
        lines.append("")

    # Advertencias
    if audit.warnings:
        lines.append("## ⚠️ Advertencias")
        lines.append("")
        for pg, w in audit.warnings:
            lines.append(f"- Página {pg}: {w}")
        lines.append("")

    # Errores
    if audit.errors:
        lines.append("## 🚨 Errores")
        lines.append("")
        for item in audit.errors:
            if isinstance(item, tuple):
                lines.append(f"- Página {item[0]}: {item[1]}")
            else:
                lines.append(f"- {item}")
        lines.append("")

    # Recomendaciones
    lines.append("## 🔍 Recomendaciones para revisión manual")
    lines.append("")
    recs = []
    if audit.pages_ocr:
        recs.append("Verificar texto OCR en páginas con baja confianza.")
    if audit.tables_converted:
        recs.append("Revisar tablas convertidas: pdfplumber puede alterar columnas en layouts complejos.")
    if audit.images_extracted:
        recs.append(
            f"Se extrajeron {audit.images_extracted} imágenes "
            f"({audit.captions_total} con caption ligada). "
            "Verificar referencias en el MD."
        )
    if audit.two_col_pages:
        recs.append(
            f"Verificar orden de lectura en páginas 2-col: {audit.two_col_pages}. "
            "La columna izquierda precede a la derecha."
        )
    if audit.headings_total > 0:
        recs.append(
            f"Se detectaron {audit.headings_total} encabezados por font size. "
            "Verificar jerarquía # / ## / ###."
        )
    if not recs:
        recs.append("No se detectaron elementos de alto riesgo. Revisión estándar recomendada.")
    for r in recs:
        lines.append(f"- {r}")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def _write_failed_outputs(md_path: Path, audit_path: Path, audit: ConversionAudit):
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# Error en la conversión\n\n")
        for e in audit.errors:
            f.write(f"- {e}\n")
    with open(audit_path, "w", encoding="utf-8") as f:
        f.write("# Auditoría — FALLIDA\n\n")
        for e in audit.errors:
            f.write(f"- {e}\n")


def _format_page_ranges(pages: list) -> str:
    """Formatea [1,2,3,5] → '1–3, 5'"""
    if not pages:
        return ""
    pages = sorted(set(pages))
    ranges = []
    start = end = pages[0]
    for p in pages[1:]:
        if p == end + 1:
            end = p
        else:
            ranges.append(f"{start}" if start == end else f"{start}–{end}")
            start = end = p
    ranges.append(f"{start}" if start == end else f"{start}–{end}")
    return ", ".join(ranges)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Convierte PDF a Markdown con análisis de layout y auditoría."
    )
    parser.add_argument("input", help="Ruta al archivo PDF")
    parser.add_argument("--output", "-o", help="Nombre base de salida (sin extensión)", default=None)
    parser.add_argument("--lang", default="spa+eng", help="Idioma tesseract (default: spa+eng)")
    parser.add_argument("--dpi", type=int, default=300, help="DPI para renderizar páginas (default: 300)")
    parser.add_argument("--ocr-only", action="store_true", help="Forzar OCR en todas las páginas")
    parser.add_argument("--no-images", action="store_true", help="No extraer imágenes embebidas")
    parser.add_argument("--save-ir", action="store_true", help="Guardar Layout IR en ir.json (debug)")

    args = parser.parse_args()

    if not Path(args.input).exists():
        sys.exit(f"ERROR: No se encontró el archivo: {args.input}")

    output_name = args.output or Path(args.input).stem.replace(" ", "_")

    print(f"🔄 Convirtiendo: {args.input}")
    print(f"   Idioma OCR: {args.lang} | DPI: {args.dpi}")

    md_path, audit_path = convert_pdf(
        pdf_path=args.input,
        output_name=output_name,
        lang=args.lang,
        dpi=args.dpi,
        ocr_only=args.ocr_only,
        extract_images=not args.no_images,
        save_ir=args.save_ir,
    )

    print(f"\n✅ Markdown:  {md_path}")
    print(f"📋 Auditoría: {audit_path}")


if __name__ == "__main__":
    main()
