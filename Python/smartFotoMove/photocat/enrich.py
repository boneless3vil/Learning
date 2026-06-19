"""AI enrichment phase.

For each photo (subject to config toggles) this computes:
  * a CLIP embedding   -> natural-language semantic search
  * a Florence-2 caption + tags (+ optional OCR) -> keyword search & "what's in it"
  * optional face embeddings -> search by person (see faces.py)

Models are loaded lazily and only if their toggle is on, so you can run a
caption-only, CLIP-only, or OCR-only pass. Heavy imports (torch, transformers)
happen here, not at module import, so the rest of photocat works without them.

Resumable: each photo is committed as it finishes; rows with ``enriched = 1``
are skipped unless ``force`` (redo all) or ``redo_ocr`` (fill OCR only) is set.
"""
from __future__ import annotations

from contextlib import contextmanager
from typing import Iterable, Optional

import numpy as np
from PIL import Image
from rich.console import Console
from rich.progress import (
    BarColumn, MofNCompleteColumn, Progress, SpinnerColumn, TextColumn, TimeRemainingColumn,
)

from . import db
from .config import Config

console = Console()


def _resolve_device(pref: str) -> str:
    import torch
    if pref == "cpu":
        return "cpu"
    return "cuda" if torch.cuda.is_available() else "cpu"  # "cuda" or "auto"


def _downscale(img: Image.Image, max_size: int) -> Image.Image:
    """Shrink the long edge to max_size (in place, aspect-preserving). 0 = off."""
    if max_size and max(img.size) > max_size:
        img.thumbnail((max_size, max_size))
    return img


def _chunks(seq: list, n: int) -> Iterable[list]:
    for i in range(0, len(seq), max(1, n)):
        yield seq[i:i + n]


# --------------------------------------------------------------------------- #
#  Model wrappers (lazy-loaded)                                               #
# --------------------------------------------------------------------------- #

class ClipEmbedder:
    def __init__(self, cfg: Config, device: str):
        import open_clip
        import torch
        self.torch = torch
        self.device = device
        self.model, _, self.preprocess = open_clip.create_model_and_transforms(
            cfg.enrich.clip_model, pretrained=cfg.enrich.clip_pretrained, device=device
        )
        self.model.eval()
        self.tokenizer = open_clip.get_tokenizer(cfg.enrich.clip_model)

    @property
    def dim(self) -> int:
        return self.model.visual.output_dim

    def embed_images(self, imgs: list[Image.Image]) -> np.ndarray:
        """Embed a batch of images at once -> (N, dim) float32, L2-normalised."""
        with self.torch.no_grad():
            batch = self.torch.stack([self.preprocess(im) for im in imgs]).to(self.device)
            feats = self.model.encode_image(batch)
            feats /= feats.norm(dim=-1, keepdim=True)
        return feats.cpu().numpy().astype("float32")

    def embed_image(self, img: Image.Image) -> np.ndarray:
        return self.embed_images([img])[0]

    def embed_text(self, text: str) -> np.ndarray:
        with self.torch.no_grad():
            tokens = self.tokenizer([text]).to(self.device)
            feat = self.model.encode_text(tokens)
            feat /= feat.norm(dim=-1, keepdim=True)
        return feat.cpu().numpy().astype("float32")[0]


@contextmanager
def _no_flash_attn():
    """Temporarily strip `flash_attn` from a remote model's import requirements.

    transformers' check_imports() refuses to load Florence-2 because its code
    file imports flash_attn. flash_attn is optional (the model falls back to
    standard attention) and barely installable on Windows, so we filter it out
    of the import check for the duration of the load.
    """
    import transformers.dynamic_module_utils as dmu
    original = dmu.get_imports

    def patched(filename):
        return [imp for imp in original(filename) if imp != "flash_attn"]

    dmu.get_imports = patched
    try:
        yield
    finally:
        dmu.get_imports = original


class Florence:
    """Florence-2: caption, tags (dense region labels), and OCR in one model."""

    def __init__(self, cfg: Config, device: str):
        import torch
        from transformers import AutoModelForCausalLM, AutoProcessor
        self.torch = torch
        self.device = device
        self.max_tokens = cfg.enrich.caption_max_tokens
        self.num_beams = cfg.enrich.num_beams
        dtype = torch.float16 if device == "cuda" else torch.float32
        # Florence-2's remote code declares `import flash_attn`, which is hard to
        # build on Windows and isn't actually needed. Patch transformers' import
        # check to drop that requirement so it loads with standard attention.
        with _no_flash_attn():
            self.model = AutoModelForCausalLM.from_pretrained(
                cfg.enrich.caption_model, trust_remote_code=True, torch_dtype=dtype
            ).to(device).eval()
            self.processor = AutoProcessor.from_pretrained(
                cfg.enrich.caption_model, trust_remote_code=True
            )

    def _run(self, img: Image.Image, task: str) -> dict:
        inputs = self.processor(text=task, images=img, return_tensors="pt").to(
            self.device, self.model.dtype
        )
        with self.torch.no_grad():
            ids = self.model.generate(
                input_ids=inputs["input_ids"],
                pixel_values=inputs["pixel_values"],
                max_new_tokens=self.max_tokens, num_beams=self.num_beams, do_sample=False,
            )
        text_out = self.processor.batch_decode(ids, skip_special_tokens=False)[0]
        return self.processor.post_process_generation(
            text_out, task=task, image_size=(img.width, img.height)
        )

    def caption(self, img: Image.Image) -> str:
        return (self._run(img, "<DETAILED_CAPTION>").get("<DETAILED_CAPTION>") or "").strip()

    def tags(self, img: Image.Image) -> list[str]:
        out = self._run(img, "<DENSE_REGION_CAPTION>")
        labels = out.get("<DENSE_REGION_CAPTION>", {}).get("labels", [])
        seen, result = set(), []
        for lbl in labels:
            key = lbl.strip().lower()
            if key and key not in seen:
                seen.add(key)
                result.append(lbl.strip())
        return result

    def ocr(self, img: Image.Image) -> str:
        return (self._run(img, "<OCR>").get("<OCR>") or "").strip()


# --------------------------------------------------------------------------- #
#  Main entry                                                                 #
# --------------------------------------------------------------------------- #

def enrich(
    cfg: Config, conn,
    limit: Optional[int] = None,
    force: bool = False,
    redo_ocr: bool = False,
) -> dict[str, int]:
    """Enrich photos.

    force     -> re-process every non-duplicate photo (recomputes all signals).
    redo_ocr  -> only (re)read printed text on already-enriched photos; cheap way
                 to add OCR after the fact without recomputing captions/CLIP.
    """
    e = cfg.enrich
    device = _resolve_device(e.device)

    # Decide which signals run this pass.
    do_caption = e.enable_caption and not redo_ocr
    do_tags = e.enable_tags and not redo_ocr
    do_ocr = redo_ocr or e.enable_ocr
    do_clip = e.enable_clip and not redo_ocr
    do_faces = cfg.faces.enabled and not redo_ocr
    # OCR runs either through Florence (downsampled) or a dedicated full-res engine.
    ocr_via_florence = do_ocr and e.ocr_engine == "florence"
    do_ocr_engine = do_ocr and e.ocr_engine != "florence"
    need_florence = do_caption or do_tags or ocr_via_florence

    if redo_ocr:
        where = "is_duplicate = 0 AND enriched = 1"
    elif force:
        where = "is_duplicate = 0"
    else:
        where = "is_duplicate = 0 AND enriched = 0"

    rows = list(db.iter_photos(conn, where))
    if e.min_megapixels:
        rows = [r for r in rows if (r["megapixels"] or 0) >= e.min_megapixels]
    if limit:
        rows = rows[:limit]
    if not rows:
        console.print("[green]Nothing to enrich for this pass.")
        return {"enriched": 0, "failed": 0}

    console.print(f"Enrichment device: [bold]{device}[/] | {len(rows)} photo(s) | "
                  f"signals: " + ", ".join(
                      n for n, on in [("clip", do_clip), ("caption", do_caption),
                                      ("tags", do_tags), ("ocr", do_ocr),
                                      ("faces", do_faces)] if on))

    clip = florence = faces_app = ocr_reader = None
    if do_clip:
        console.print("Loading CLIP model...")
        clip = ClipEmbedder(cfg, device)
    if need_florence:
        console.print(f"Loading Florence-2 ({e.caption_model})...")
        florence = Florence(cfg, device)
    if do_ocr_engine:
        from . import ocr as ocr_mod
        try:
            console.print(f"Loading OCR engine '{e.ocr_engine}'...")
            ocr_reader = ocr_mod.load(e.ocr_engine, cfg)
        except Exception as ex:
            console.print(f"[yellow]OCR engine '{e.ocr_engine}' unavailable; skipping OCR.\n  {ex}[/]")
            do_ocr = do_ocr_engine = False
    if do_faces:
        from . import faces as faces_mod
        faces_app = faces_mod.load(device, cfg)

    stats = {"enriched": 0, "failed": 0}
    florence_warned = False
    with Progress(
        SpinnerColumn(), TextColumn("[progress.description]{task.description}"),
        BarColumn(), MofNCompleteColumn(), TimeRemainingColumn(), console=console,
    ) as progress:
        task = progress.add_task("Enriching", total=len(rows))

        for batch in _chunks(rows, e.batch_size):
            # 1) Load + downscale every image in the batch.
            loaded: list[tuple] = []
            for row in batch:
                try:
                    with Image.open(row["path"]) as im:
                        img = _downscale(im.convert("RGB"), e.max_image_size)
                    loaded.append((row, img))
                except Exception as ex:
                    stats["failed"] += 1
                    console.print(f"[red]Could not open:[/] {row['path']} ({ex})")
                progress.advance(task)

            if not loaded:
                continue

            # 2) CLIP for the whole batch at once.
            vecs = None
            if clip is not None:
                try:
                    vecs = clip.embed_images([img for _, img in loaded])
                except Exception as ex:
                    console.print(f"[red]CLIP batch failed:[/] {ex}")

            # 3) Per-image Florence + faces, then save. Each signal is isolated so
            #    one failure never discards another's result for the same photo.
            for idx, (row, img) in enumerate(loaded):
                fields: dict = {}
                if florence is not None:
                    try:
                        if do_caption:
                            fields["caption"] = florence.caption(img)
                        if do_tags:
                            fields["tags"] = ", ".join(florence.tags(img))
                        if ocr_via_florence:
                            fields["ocr_text"] = florence.ocr(img)
                    except Exception as ex:
                        if not florence_warned:
                            console.print(f"[yellow]Florence-2 failed (skipping its "
                                          f"signals): {ex}")
                            florence_warned = True
                if ocr_reader is not None:
                    # Read text on the FULL-resolution original (catches small print).
                    try:
                        with Image.open(row["path"]) as im2:
                            fields["ocr_text"] = ocr_reader.read(im2.convert("RGB"))
                    except Exception as ex:
                        console.print(f"[red]OCR failed:[/] {row['path']} ({ex})")
                if vecs is not None:
                    fields["clip_vector"] = vecs[idx].tobytes()
                if faces_app is not None:
                    try:
                        from . import faces as faces_mod
                        faces_mod.detect_and_store(conn, faces_app, row["id"], img, cfg)
                    except Exception as ex:
                        console.print(f"[red]Faces failed:[/] {row['path']} ({ex})")

                produced = [k for k in ("caption", "tags", "ocr_text", "clip_vector")
                            if k in fields]
                if not produced and not (do_faces and faces_app is not None):
                    stats["failed"] += 1
                    continue
                if not redo_ocr:
                    fields["enriched"] = 1
                # Rebuild the FTS blob from merged (existing + new) values.
                fields["search_text"] = db.compose_search_text({**dict(row), **fields})
                db.update_photo(conn, row["id"], fields)
                stats["enriched"] += 1
                if stats["enriched"] % e.commit_every == 0:
                    conn.commit()
        conn.commit()

    verb = "Re-OCR'd" if redo_ocr else "Enriched"
    console.print(f"[green]{verb} {stats['enriched']} photos[/] ({stats['failed']} failed).")
    return stats
