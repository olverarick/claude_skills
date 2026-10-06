"""
Tesseract OCR provider for pdf-to-md.

Requires: pytesseract, Pillow, tesseract-ocr (system package).

Usage:
    provider = TesseractProvider(lang="spa+eng", dpi=300)
    result   = provider.run(pil_image)
    print(result.text, result.confidence)
"""
from __future__ import annotations
import re
from typing import Optional
from PIL import Image, ImageFilter, ImageEnhance

try:
    import pytesseract
    _TESS_AVAILABLE = True
except ImportError:
    _TESS_AVAILABLE = False

from .base import OcrProvider, OcrResult


class TesseractProvider(OcrProvider):
    """Wraps pytesseract with per-word confidence reporting."""

    name = "tesseract"

    def __init__(self, lang: str = "spa+eng", dpi: int = 300,
                 psm: int = 3, oem: int = 3):
        if not _TESS_AVAILABLE:
            raise RuntimeError(
                "pytesseract is not installed. Run: pip install pytesseract --break-system-packages"
            )
        self.lang = lang
        self.dpi  = dpi
        self.psm  = psm    # Page Segmentation Mode  (3 = auto)
        self.oem  = oem    # OCR Engine Mode          (3 = LSTM + legacy)

    # ------------------------------------------------------------------
    # Preprocessing
    # ------------------------------------------------------------------
    def preprocess(self, image: Image.Image) -> Image.Image:
        """Convert to grayscale and slightly sharpen."""
        gray = image.convert("L")
        enhanced = ImageEnhance.Contrast(gray).enhance(1.4)
        return enhanced.filter(ImageFilter.SHARPEN)

    # ------------------------------------------------------------------
    # Core OCR
    # ------------------------------------------------------------------
    def image_to_string(self, image: Image.Image,
                        lang: Optional[str] = None) -> OcrResult:
        lang = lang or self.lang
        config = f"--psm {self.psm} --oem {self.oem}"

        warnings: list = []

        # --- plain text ---
        text = pytesseract.image_to_string(image, lang=lang, config=config)

        # --- confidence via data output ---
        confidence = -1.0
        try:
            data = pytesseract.image_to_data(
                image, lang=lang, config=config,
                output_type=pytesseract.Output.DICT
            )
            confs = [int(c) for c in data["conf"] if str(c).lstrip("-").isdigit() and int(c) >= 0]
            if confs:
                confidence = sum(confs) / len(confs)
        except Exception as exc:
            warnings.append(f"No se pudo calcular confianza: {exc}")

        if confidence >= 0 and confidence < 70:
            warnings.append(f"Confianza baja ({confidence:.1f}%) — revisar caracteres especiales")

        return OcrResult(
            text=text,
            confidence=confidence,
            lang=lang,
            provider=self.name,
            warnings=warnings,
        )

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------
    @staticmethod
    def available_langs() -> list:
        """Return list of installed Tesseract language packs."""
        try:
            return pytesseract.get_languages()
        except Exception:
            return []
