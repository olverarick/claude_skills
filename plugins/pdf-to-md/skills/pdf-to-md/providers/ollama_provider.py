"""
Ollama vision-model OCR provider for pdf-to-md.

Uses a local Ollama instance (default http://localhost:11434) with a multimodal
model such as llava, llava:13b, bakllava, or moondream.

Requires: requests, Pillow, a running Ollama server with a vision model pulled.

Usage:
    provider = OllamaProvider(model="llava", base_url="http://localhost:11434")
    result   = provider.run(pil_image)
    print(result.text, result.confidence)

Note: Ollama does not expose per-word confidence scores, so OcrResult.confidence
will always be -1.0 (not available).
"""
from __future__ import annotations
import base64
import io
import json
from typing import Optional
from PIL import Image

try:
    import requests as _requests
    _REQUESTS_AVAILABLE = True
except ImportError:
    _REQUESTS_AVAILABLE = False

from .base import OcrProvider, OcrResult

_DEFAULT_PROMPT = (
    "You are an OCR engine. Extract ALL text visible in this image exactly as it appears, "
    "preserving line breaks and paragraph structure. Do NOT summarize, interpret or add "
    "commentary. Output only the extracted text."
)


class OllamaProvider(OcrProvider):
    """
    OCR via a local Ollama vision model.

    Advantages over Tesseract:
    - Better handling of complex layouts, mixed fonts, and handwriting.
    - Understands context (can infer partially obscured characters).

    Limitations:
    - Much slower (LLM inference per page).
    - No confidence score.
    - Requires a GPU-capable machine or patience.
    """

    name = "ollama"

    def __init__(
        self,
        model: str = "llava",
        base_url: str = "http://localhost:11434",
        prompt: str = _DEFAULT_PROMPT,
        timeout: int = 120,
    ):
        if not _REQUESTS_AVAILABLE:
            raise RuntimeError(
                "requests is not installed. Run: pip install requests --break-system-packages"
            )
        self.model    = model
        self.base_url = base_url.rstrip("/")
        self.prompt   = prompt
        self.timeout  = timeout

    # ------------------------------------------------------------------
    # Health check
    # ------------------------------------------------------------------
    def is_available(self) -> bool:
        """Return True if the Ollama server is reachable."""
        try:
            r = _requests.get(f"{self.base_url}/api/tags", timeout=5)
            return r.status_code == 200
        except Exception:
            return False

    def model_is_pulled(self) -> bool:
        """Return True if the chosen model is already downloaded."""
        try:
            r = _requests.get(f"{self.base_url}/api/tags", timeout=5)
            if r.status_code != 200:
                return False
            models = [m["name"] for m in r.json().get("models", [])]
            return any(self.model in m for m in models)
        except Exception:
            return False

    # ------------------------------------------------------------------
    # Core OCR
    # ------------------------------------------------------------------
    def image_to_string(self, image: Image.Image,
                        lang: Optional[str] = None) -> OcrResult:
        """Send image to Ollama and return extracted text."""
        warnings: list = []

        # Encode image as base64 PNG
        buf = io.BytesIO()
        image.convert("RGB").save(buf, format="PNG")
        b64 = base64.b64encode(buf.getvalue()).decode("utf-8")

        payload = {
            "model": self.model,
            "prompt": self.prompt,
            "images": [b64],
            "stream": False,
        }

        try:
            r = _requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=self.timeout,
            )
            r.raise_for_status()
            body = r.json()
            text = body.get("response", "").strip()
        except _requests.exceptions.ConnectionError:
            warnings.append(
                f"No se pudo conectar a Ollama en {self.base_url}. "
                "Verifica que el servidor está corriendo."
            )
            text = ""
        except _requests.exceptions.Timeout:
            warnings.append(
                f"Ollama tardó más de {self.timeout}s. "
                "Considera reducir el DPI o usar un modelo más pequeño."
            )
            text = ""
        except Exception as exc:
            warnings.append(f"Error Ollama: {exc}")
            text = ""

        if not text:
            warnings.append("Ollama devolvió texto vacío para esta página.")

        return OcrResult(
            text=text,
            confidence=-1.0,   # Ollama does not provide word-level confidence
            lang=lang or "",
            provider=self.name,
            warnings=warnings,
        )
