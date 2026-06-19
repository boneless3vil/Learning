"""Organize photos on disk into year folders (and optional month sub-folders).

Splits one giant folder into per-year folders so Windows Explorer stays fast.
The capture year comes from the camera's EXIF date; photos without a real camera
date go to a "miscellaneous" folder. If ``max_per_folder`` is set, a year that
exceeds it is split into month sub-folders (e.g. 2019/2019-07).

Files are MOVED (never copied), and the catalog's stored path is updated so
search keeps pointing at the right place. Preview first; nothing moves until you
apply.
"""
from __future__ import annotations

import shutil
from collections import Counter
from datetime import datetime
from pathlib import Path

from rich.console import Console
from rich.table import Table

from . import db
from .config import Config

console = Console()


def _month(date_taken: str) -> str:
    try:
        return f"{datetime.fromisoformat(date_taken).month:02d}"
    except (ValueError, TypeError):
        return "00"


def _is_dated(row, require_camera_date: bool) -> bool:
    if require_camera_date:
        return row["date_source"] == "exif" and bool(row["year"])
    return bool(row["year"])


def build_plan(conn, cfg: Config) -> tuple[list[dict], Path]:
    """Return (moves, root). Each move: {row, dest_dir, bucket}."""
    o = cfg.organize
    root = cfg.resolved_organize_root()
    rows = list(db.iter_photos(conn, "is_duplicate = 0"))

    # Count per year first so we know which years need month-splitting.
    year_counts = Counter(
        row["year"] for row in rows if _is_dated(row, o.require_camera_date)
    )

    moves: list[dict] = []
    for row in rows:
        if _is_dated(row, o.require_camera_date):
            year = row["year"]
            if o.max_per_folder and year_counts[year] > o.max_per_folder:
                dest = root / str(year) / f"{year}-{_month(row['date_taken'])}"
                bucket = f"{year}/{year}-{_month(row['date_taken'])}"
            else:
                dest = root / str(year)
                bucket = str(year)
        else:
            dest = root / o.misc_folder
            bucket = o.misc_folder
        # Skip files already sitting in their destination.
        try:
            if Path(row["path"]).resolve().parent == dest.resolve():
                continue
        except OSError:
            pass
        moves.append({"row": row, "dest_dir": dest, "bucket": bucket})
    return moves, root


def print_plan(moves: list[dict], root: Path) -> None:
    if not moves:
        console.print("[green]Nothing to organize — everything is already in place.")
        return
    counts = Counter(m["bucket"] for m in moves)
    console.print(f"[bold]{len(moves)} file(s)[/] would move under [bold]{root}[/]:\n")
    table = Table("folder", "photos to move", header_style="bold cyan")
    for bucket in sorted(counts):
        table.add_row(bucket, str(counts[bucket]))
    console.print(table)


def apply_plan(conn, cfg: Config, moves: list[dict]) -> int:
    moved = 0
    for m in moves:
        row, dest_dir = m["row"], m["dest_dir"]
        src = Path(row["path"])
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = _unique_dest(dest_dir, src.name)
        try:
            if src.exists():
                shutil.move(str(src), str(dest))
            db.update_photo(conn, row["id"], {"path": str(dest)})
            moved += 1
            if moved % 200 == 0:
                conn.commit()
        except Exception as e:
            console.print(f"[red]Could not move {src}: {e}")
    conn.commit()
    console.print(f"[green]Moved {moved} file(s) into year folders under {cfg.resolved_organize_root()}")
    return moved


def _unique_dest(folder: Path, name: str) -> Path:
    dest = folder / name
    stem, suffix = Path(name).stem, Path(name).suffix
    n = 1
    while dest.exists():
        dest = folder / f"{stem}__{n}{suffix}"
        n += 1
    return dest
