"""Pluggable OCR backends that read printed text at full resolution.

Florence-2 downsamples images to ~768px internally, so it misses small print
(e.g. the tiny "Department of Motor Vehicles" header on an ID). These engines
run on the native-resolution image and catch that text.

  * "easyocr"   — EasyOCR (default; reuses the project's PyTorch, runs on GPU)
  * "paddle"    — PaddleOCR (strong on dense text; the 3.x CPU build is currently
                  unstable on Windows — use a GPU/known-good build)
  * "tesseract" — Tesseract via pytesseract (lightest; needs the Tesseract binary)

Each reader exposes ``read(pil_image) -> str``. ``load(engine, cfg)`` returns a
reader or raises a friendly ImportError naming the package to install.
"""
from __future__ import annotations

import numpy as np
from PIL import Image


def load(engine: str, cfg):
    engine = (engine or "easyocr").lower()
    if engine == "easyocr":
        return EasyReader(cfg)
    if engine == "paddle":
        return PaddleReader(cfg)
    if engine == "tesseract":
        return TesseractReader(cfg)
    raise ValueError(f"Unknown OCR engine '{engine}' (use easyocr | paddle | tesseract | florence).")


class EasyReader:
    """EasyOCR — reuses the project's PyTorch (GPU), good on small/clear text."""

    def __init__(self, cfg):
        try:
            import easyocr
        except ImportError as e:
            raise ImportError(
                "OCR engine 'easyocr' needs EasyOCR. Install it with:\n"
                "    pip install easyocr\n"
                "or set enrich.ocr_engine to 'tesseract' / 'florence'."
            ) from e
        gpu = cfg.enrich.device != "cpu"
        try:
            import torch
            gpu = gpu and torch.cuda.is_available()
        except Exception:
            gpu = False
        # verbose=False avoids EasyOCR's progress bar, whose block glyph crashes
        # non-UTF-8 Windows consoles.
        self.reader = easyocr.Reader(["en"], gpu=gpu, verbose=False)

    def read(self, img: Image.Image) -> str:
        arr = np.asarray(img.convert("RGB"))
        lines = self.reader.readtext(arr, detail=1, paragraph=False)
        return "\n".join(t for (_box, t, *_rest) in lines if t)


class PaddleReader:
    def __init__(self, cfg):
        try:
            from paddleocr import PaddleOCR
        except ImportError as e:
            raise ImportError(
                "OCR engine 'paddle' needs PaddleOCR. Install it with:\n"
                "    pip install paddleocr paddlepaddle    (CPU)\n"
                "or set enrich.ocr_engine to 'tesseract' / 'florence'."
            ) from e
        use_gpu = cfg.enrich.device != "cpu"
        # PaddleOCR's constructor args have shifted across versions; pass the
        # common ones and fall back to a bare constructor if rejected.
        for kwargs in (
            dict(use_angle_cls=True, lang="en", show_log=False, use_gpu=use_gpu),
            dict(use_angle_cls=True, lang="en"),
            dict(lang="en"),
            dict(),
        ):
            try:
                self.ocr = PaddleOCR(**kwargs)
                break
            except (TypeError, ValueError):
                continue
        else:
            raise ImportError("Could not initialise PaddleOCR with any known argument set.")

    def read(self, img: Image.Image) -> str:
        arr = np.asarray(img.convert("RGB"))
        try:
            res = self.ocr.ocr(arr)
        except TypeError:
            res = self.ocr.ocr(arr, cls=True)
        return "\n".join(_extract_paddle_text(res))


def _extract_paddle_text(res) -> list[str]:
    """Pull recognised strings out of PaddleOCR's (version-dependent) result."""
    texts: list[str] = []
    for page in (res or []):
        if page is None:
            continue
        # PaddleOCR 3.x: dict with 'rec_texts'.
        if isinstance(page, dict):
            texts.extend(t for t in page.get("rec_texts", []) if t)
            continue
        # PaddleOCR 2.x: list of [box, (text, score)].
        for item in page:
            try:
                t = item[1][0]
            except (TypeError, IndexError, KeyError):
                t = None
            if t:
                texts.append(t)
    return texts


class TesseractReader:
    def __init__(self, cfg):
        try:
            import pytesseract
        except ImportError as e:
            raise ImportError(
                "OCR engine 'tesseract' needs pytesseract and the Tesseract binary.\n"
                "    pip install pytesseract\n"
                "    winget install UB-Mannheim.TesseractOCR   (Windows binary)\n"
                "or set enrich.ocr_engine to 'paddle' / 'florence'."
            ) from e
        self._t = pytesseract

    def read(self, img: Image.Image) -> str:
        return self._t.image_to_string(img.convert("RGB")).strip()
