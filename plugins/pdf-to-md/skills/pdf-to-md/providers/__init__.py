"""OCR provider abstractions for pdf-to-md skill."""
from .base import OcrProvider, OcrResult
from .tesseract_provider import TesseractProvider

__all__ = ["OcrProvider", "OcrResult", "TesseractProvider"]

try:
    from .ollama_provider import OllamaProvider
    __all__.append("OllamaProvider")
except ImportError:
    pass


def get_provider(name: str = "tesseract", **kwargs) -> OcrProvider:
    """Factory: returns an OcrProvider by name ('tesseract' | 'ollama')."""
    if name == "tesseract":
        return TesseractProvider(**kwargs)
    if name == "ollama":
        from .ollama_provider import OllamaProvider
        return OllamaProvider(**kwargs)
    raise ValueError(f"Unknown OCR provider: {name!r}. Choose 'tesseract' or 'ollama'.")
