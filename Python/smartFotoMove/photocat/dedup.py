"""Duplicate detection and quarantine.

Two photos are duplicates when either:
  * their SHA-256 is identical (byte-for-byte the same file), or
  * their perceptual hashes are within ``phash_threshold`` Hamming distance
    (the *same picture* re-saved at a different resolution/format/quality).

Within each duplicate group one file is chosen as the KEEPER using the
configurable quality hierarchy: format rank first (RAW/TIFF/PNG > JPEG > WEBP...),
then the tie-breakers (highest megapixels, then largest file). The losers are
moved into the duplicates folder and flagged in the catalog, never deleted.
"""
from __future__ import annotations

import shutil
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.table import Table

from . import db
from .config import Config

console = Console()


# ---- perceptual-hash grouping (BK-tree for efficient near-neighbour search) --

def _hamming(a: int, b: int) -> int:
    return bin(a ^ b).count("1")


class _BKTree:
    """Tiny BK-tree over 64-bit hashes for fast 'within distance d' queries."""

    def __init__(self):
        self.root: Optional["_BKNode"] = None

    def add(self, h: int, idx: int):
        node = _BKNode(h, idx)
        if self.root is None:
            self.root = node
            return
        cur = self.root
        while True:
            d = _hamming(h, cur.h)
            nxt = cur.kids.get(d)
            if nxt is None:
                cur.kids[d] = node
                return
            cur = nxt

    def query(self, h: int, max_d: int) -> list[int]:
        if self.root is None:
            return []
        out: list[int] = []
        stack = [self.root]
        while stack:
            node = stack.pop()
            d = _hamming(h, node.h)
            if d <= max_d:
                out.append(node.idx)
            for dist, child in node.kids.items():
                if d - max_d <= dist <= d + max_d:
                    stack.append(child)
        return out


class _BKNode:
    __slots__ = ("h", "idx", "kids")

    def __init__(self, h: int, idx: int):
        self.h = h
        self.idx = idx
        self.kids: dict[int, _BKNode] = {}


class _UnionFind:
    def __init__(self):
        self.parent: dict[int, int] = {}

    def find(self, x: int) -> int:
        self.parent.setdefault(x, x)
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: int, b: int):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[ra] = rb


def _phash_to_int(phash_hex: str) -> Optional[int]:
    try:
        return int(phash_hex, 16)
    except (TypeError, ValueError):
        return None


def find_groups(conn, threshold: int) -> list[list[int]]:
    """Return groups (lists of photo ids) of duplicate/near-duplicate photos."""
    rows = conn.execute(
        "SELECT id, sha256, phash FROM photos WHERE is_duplicate = 0"
    ).fetchall()

    uf = _UnionFind()

    # 1) exact-byte duplicates via sha256
    by_sha: dict[str, list[int]] = {}
    for r in rows:
        if r["sha256"]:
            by_sha.setdefault(r["sha256"], []).append(r["id"])
    for ids in by_sha.values():
        for other in ids[1:]:
            uf.union(ids[0], other)

    # 2) visual near-duplicates via perceptual hash + BK-tree
    tree = _BKTree()
    int_hashes: list[tuple[int, int]] = []  # (phash_int, id)
    for r in rows:
        hi = _phash_to_int(r["phash"])
        if hi is not None:
            int_hashes.append((hi, r["id"]))
    for hi, idx in int_hashes:
        for match_idx in tree.query(hi, threshold):
            uf.union(idx, match_idx)
        tree.add(hi, idx)

    # collect components with >1 member
    groups: dict[int, list[int]] = {}
    all_ids = {r["id"] for r in rows}
    for pid in all_ids:
        groups.setdefault(uf.find(pid), []).append(pid)
    return [g for g in groups.values() if len(g) > 1]


# ---- keeper selection --------------------------------------------------------

def _keeper_sort_key(row, format_priority: list[str], tiebreakers: list[str]):
    ext = (row["ext"] or "").lower()
    fmt_rank = format_priority.index(ext) if ext in format_priority else len(format_priority)
    key = [fmt_rank]  # lower = better
    for tb in tiebreakers:
        val = row[tb] if row[tb] is not None else 0
        key.append(-val)  # negate: higher value sorts earlier (better)
    return tuple(key)


def choose_keeper(rows, format_priority: list[str], tiebreakers: list[str]):
    return min(rows, key=lambda r: _keeper_sort_key(r, format_priority, tiebreakers))


# ---- plan + apply ------------------------------------------------------------

def build_plan(conn, cfg: Config) -> list[dict]:
    groups = find_groups(conn, cfg.dedup.phash_threshold)
    plan: list[dict] = []
    for gid, ids in enumerate(groups, start=1):
        rows = [conn.execute("SELECT * FROM photos WHERE id = ?", (i,)).fetchone() for i in ids]
        keeper = choose_keeper(rows, cfg.dedup.format_priority, cfg.dedup.keeper_tiebreakers)
        losers = [r for r in rows if r["id"] != keeper["id"]]
        plan.append({"group": gid, "keeper": keeper, "losers": losers})
    return plan


def print_plan(plan: list[dict]) -> None:
    if not plan:
        console.print("[green]No duplicates found.")
        return
    total_losers = sum(len(p["losers"]) for p in plan)
    console.print(
        f"[bold]{len(plan)} duplicate group(s)[/], "
        f"{total_losers} file(s) would be moved aside.\n"
    )
    for p in plan[:50]:  # preview first 50 groups
        table = Table(title=f"Group {p['group']}", show_header=True, header_style="bold cyan")
        table.add_column("role"); table.add_column("ext")
        table.add_column("MP", justify="right"); table.add_column("size", justify="right")
        table.add_column("path", overflow="fold")
        k = p["keeper"]
        table.add_row("[green]KEEP", k["ext"], str(k["megapixels"]), _h(k["size_bytes"]), k["path"])
        for l in p["losers"]:
            table.add_row("[yellow]dup", l["ext"], str(l["megapixels"]), _h(l["size_bytes"]), l["path"])
        console.print(table)
    if len(plan) > 50:
        console.print(f"... and {len(plan) - 50} more groups (not shown).")


def apply_plan(conn, cfg: Config, plan: list[dict]) -> int:
    dups_dir = cfg.resolved_duplicates_dir()
    dups_dir.mkdir(parents=True, exist_ok=True)
    moved = 0
    for p in plan:
        keeper_id = p["keeper"]["id"]
        for loser in p["losers"]:
            src = Path(loser["path"])
            dest = _unique_dest(dups_dir, src.name)
            try:
                if src.exists():
                    shutil.move(str(src), str(dest))
                db.update_photo(conn, loser["id"], {
                    "is_duplicate": 1,
                    "duplicate_of": keeper_id,
                    "dup_group": p["group"],
                    "path": str(dest),
                })
                moved += 1
            except Exception as e:
                console.print(f"[red]Could not move {src}: {e}")
    conn.commit()
    console.print(f"[green]Moved {moved} duplicate(s) into {dups_dir}")
    return moved


def _unique_dest(folder: Path, name: str) -> Path:
    dest = folder / name
    stem, suffix = Path(name).stem, Path(name).suffix
    n = 1
    while dest.exists():
        dest = folder / f"{stem}__{n}{suffix}"
        n += 1
    return dest


def _h(n: Optional[int]) -> str:
    if not n:
        return "0"
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.0f}{unit}"
        n /= 1024
    return f"{n:.0f}TB"
