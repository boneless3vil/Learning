"""Scan phase: walk source folders, hash, read EXIF, compute perceptual hash.

This phase is fast and AI-free, so it can run on any machine. It is fully
idempotent: a file already in the catalog at the same path is skipped unless its
size or mtime changed. Rerunning after adding photos only processes the new ones.
"""
from __future__ import annotations

import hashlib
from datetime import datetime
from pathlib import Path
from typing import Iterator

import imagehash
from PIL import Image
from rich.console import Console
from rich.progress import (
    BarColumn, MofNCompleteColumn, Progress, SpinnerColumn, TextColumn, TimeRemainingColumn,
)

from . import db
from .config import Config
from . import exif as exif_mod

console = Console()
CHUNK = 1 << 20  # 1 MiB


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(CHUNK), b""):
            h.update(chunk)
    return h.hexdigest()


def perceptual_hash(path: Path) -> str | None:
    """Resolution/format-invariant hash. Same picture -> same/near hash."""
    try:
        with Image.open(path) as img:
            return str(imagehash.phash(img.convert("RGB")))
    except Exception:
        return None


def iter_image_files(cfg: Config) -> Iterator[Path]:
    sc = cfg.scan
    exts = {e.lower() for e in sc.extensions}
    pattern = "**/*" if sc.recursive else "*"
    # Never re-index the duplicates quarantine (it usually lives inside a source).
    try:
        dup_dir = cfg.resolved_duplicates_dir().resolve()
    except Exception:
        dup_dir = None
    for src in cfg.source_dirs:
        root = Path(src)
        if not root.exists():
            console.print(f"[yellow]Source not found, skipping:[/] {src}")
            continue
        for p in root.glob(pattern):
            if sc.skip_hidden and any(part.startswith(".") for part in p.parts):
                continue
            if not p.is_file() or p.suffix.lower() not in exts:
                continue
            if dup_dir is not None:
                try:
                    if dup_dir in p.resolve().parents:
                        continue
                except OSError:
                    pass
            if p.is_symlink() and not sc.follow_symlinks:
                continue
            try:
                if p.stat().st_size < sc.min_size_bytes:
                    continue
            except OSError:
                continue
            yield p


def scan(cfg: Config, conn) -> dict[str, int]:
    files = list(iter_image_files(cfg))
    stats = {"new": 0, "updated": 0, "skipped": 0, "failed": 0}

    if not files:
        console.print("[yellow]No images found in configured source_dirs.")
        return stats

    with Progress(
        SpinnerColumn(), TextColumn("[progress.description]{task.description}"),
        BarColumn(), MofNCompleteColumn(), TimeRemainingColumn(), console=console,
    ) as progress:
        task = progress.add_task("Scanning", total=len(files))
        for path in files:
            progress.advance(task)
            try:
                abspath = str(path.resolve())
                stat = path.stat()
                existing = db.get_photo_by_path(conn, abspath)
                if existing and existing["size_bytes"] == stat.st_size:
                    stats["skipped"] += 1
                    continue

                meta = exif_mod.extract(path)
                w, h = meta["width"], meta["height"]
                mp = round((w * h) / 1_000_000, 2) if (w and h) else None
                year = None
                if meta["date_taken"]:
                    try:
                        year = datetime.fromisoformat(meta["date_taken"]).year
                    except ValueError:
                        pass

                fields = {
                    "path": abspath,
                    "original_path": abspath,
                    "filename": path.name,
                    "ext": path.suffix.lower().lstrip("."),
                    "size_bytes": stat.st_size,
                    "width": w, "height": h, "megapixels": mp,
                    "sha256": sha256_file(path),
                    "phash": perceptual_hash(path) if cfg.scan.compute_phash else None,
                    "date_taken": meta["date_taken"],
                    "date_source": meta["date_source"],
                    "year": year,
                    "camera_make": meta["camera_make"],
                    "camera_model": meta["camera_model"],
                    "gps_lat": meta["gps_lat"], "gps_lon": meta["gps_lon"],
                }
                # Seed the FTS blob with what we know now (filename/year/camera);
                # enrich/geocode will rebuild it once AI + place data exist.
                fields["search_text"] = db.compose_search_text(fields)

                if existing:
                    db.update_photo(conn, existing["id"], {**fields, "enriched": 0})
                    stats["updated"] += 1
                else:
                    db.insert_photo(conn, fields)
                    stats["new"] += 1
            except Exception as e:  # never let one bad file stop the scan
                stats["failed"] += 1
                console.print(f"[red]Failed:[/] {path} ({e})")
            # Commit periodically so an interrupt loses little work.
            if (stats["new"] + stats["updated"]) % 200 == 0:
                conn.commit()
        conn.commit()

    return stats
