"""
Base class for OCR providers used by pdf-to-md.

Every provider receives a PIL Image and returns an OcrResult with:
  - text:       the extracted string
  - confidence: float 0–100 (average word-level confidence, or -1 if unavailable)
  - lang:       the language code used
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional
from PIL import Image


@dataclass
class OcrResult:
    text: str
    confidence: float = -1.0          # -1 means "unavailable"
    lang: str = ""
    provider: str = ""
    warnings: list = field(default_factory=list)

    @property
    def is_low_confidence(self) -> bool:
        """True when confidence is known and below the 70% threshold."""
        return 0 <= self.confidence < 70.0

    def __repr__(self) -> str:
        conf_str = f"{self.confidence:.1f}%" if self.confidence >= 0 else "n/a"
        return f"OcrResult(provider={self.provider!r}, conf={conf_str}, chars={len(self.text)})"


class OcrProvider(ABC):
    """Abstract base class for OCR backends."""

    name: str = "base"

    @abstractmethod
    def image_to_string(self, image: Image.Image, lang: Optional[str] = None) -> OcrResult:
        """Run OCR on a PIL Image and return an OcrResult."""
        ...

    def preprocess(self, image: Image.Image) -> Image.Image:
        """
        Optional preprocessing hook.  Override to apply contrast enhancement,
        binarization, deskewing, etc. before OCR.  Default: returns image unchanged.
        """
        return image

    def run(self, image: Image.Image, lang: Optional[str] = None) -> OcrResult:
        """Preprocess then OCR.  Call this instead of image_to_string directly."""
        processed = self.preprocess(image)
        return self.image_to_string(processed, lang=lang)
