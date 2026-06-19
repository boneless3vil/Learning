"""Search the catalog — no SQL required.

Three layers combine:
  * structured filters  (--year, --place, --camera, --person, date ranges)
  * full-text keyword   (FTS5 over the composed search_text blob: caption, tags,
                         OCR text, place, year, camera, filename)
  * semantic / CLIP     (free-text ranked by visual-concept similarity)

Default behaviour is **precision-first**: if the query text matches actual words
in the catalog (caption / OCR / tags / place), only those photos are returned —
so a literal query like "department of motor vehicles" returns the handful of
photos that really contain it, not 50 vaguely-similar ones.

CLIP semantic ranking (which sorts *all* photos by fuzzy similarity and is poor
at reading text) is used only when there are no keyword matches, or when the
caller explicitly asks for it via ``semantic=True``.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional

import numpy as np

from . import db


@dataclass
class Query:
    text: Optional[str] = None          # free-text query
    year: Optional[int] = None
    year_from: Optional[int] = None
    year_to: Optional[int] = None
    place: Optional[str] = None
    camera: Optional[str] = None
    person: Optional[str] = None
    include_duplicates: bool = False
    limit: int = 50
    semantic: bool = False              # force CLIP concept ranking
    semantic_fallback: bool = False     # if keyword finds nothing, try semantic
    min_score: Optional[float] = None   # drop semantic hits below this similarity


@dataclass
class Hit:
    id: int
    path: str
    score: float
    caption: str
    tags: str
    place: str
    date_taken: str
    match: str = ""                     # "keyword" or "semantic"


def _structured_where(q: Query) -> tuple[str, list]:
    clauses, params = [], []
    if not q.include_duplicates:
        clauses.append("p.is_duplicate = 0")
    if q.year is not None:
        clauses.append("p.year = ?"); params.append(q.year)
    if q.year_from is not None:
        clauses.append("p.year >= ?"); params.append(q.year_from)
    if q.year_to is not None:
        clauses.append("p.year <= ?"); params.append(q.year_to)
    if q.place:
        clauses.append("p.place LIKE ?"); params.append(f"%{q.place}%")
    if q.camera:
        clauses.append("(p.camera_model LIKE ? OR p.camera_make LIKE ?)")
        params += [f"%{q.camera}%", f"%{q.camera}%"]
    if q.person:
        clauses.append(
            "p.id IN (SELECT f.photo_id FROM faces f JOIN persons pe "
            "ON f.person_id = pe.id WHERE pe.name LIKE ?)"
        )
        params.append(f"%{q.person}%")
    where = " AND ".join(clauses) if clauses else "1=1"
    return where, params


def _fts_query(text: str) -> str:
    """Build a precise FTS5 query: ALL significant words must appear (implicit AND).

    Short words (<=2 chars, e.g. "of", "on", "a") are dropped so they don't force
    spurious requirements. Each term is a bareword prefix (``token*``) so plurals
    and suffixes still hit (e.g. ``vehicle*`` matches "vehicles"). Returns "" when
    the text has no usable terms.
    """
    tokens = re.findall(r"[0-9a-zA-Z]+", text.lower())
    terms = [t for t in tokens if len(t) >= 3] or tokens
    return " ".join(f"{t}*" for t in terms)


def _keyword_search(conn, text: str, where: str, params: list):
    fts = _fts_query(text)
    if not fts:
        return [], {}
    rows = conn.execute(
        f"SELECT p.id, bm25(photos_fts) AS rank FROM photos_fts "
        f"JOIN photos p ON p.id = photos_fts.rowid "
        f"WHERE photos_fts MATCH ? AND {where} ORDER BY rank",
        [fts, *params],
    ).fetchall()
    ids = [r["id"] for r in rows]
    scores = {r["id"]: -float(r["rank"]) for r in rows}  # higher = better
    return ids, scores


def _semantic_search(conn, text: str, where: str, params: list, min_score):
    rows = conn.execute(
        f"SELECT p.id, p.clip_vector FROM photos p "
        f"WHERE {where} AND p.clip_vector IS NOT NULL", params
    ).fetchall()
    if not rows:
        return None, {}
    try:
        from .enrich import ClipEmbedder
        from .config import Config, find_config
        cfg_path = find_config()
        cfg = Config.load(cfg_path) if cfg_path else Config()
        qv = ClipEmbedder(cfg, _device()).embed_text(text)
    except Exception:
        return None, {}
    ids = [r["id"] for r in rows]
    mat = np.stack([np.frombuffer(r["clip_vector"], dtype="float32") for r in rows])
    sims = mat @ qv  # L2-normalised vectors -> cosine similarity
    order = np.argsort(-sims)
    ranked = [(ids[i], float(sims[i])) for i in order]
    if min_score is not None:
        ranked = [(i, s) for i, s in ranked if s >= min_score]
    return [i for i, _ in ranked], {i: s for i, s in ranked}


def search(conn, q: Query) -> list[Hit]:
    where, params = _structured_where(q)
    ranked_ids: list[int] = []
    scores: dict[int, float] = {}
    match_kind = ""

    if q.text:
        if not q.semantic:
            # Precision-first: exact keyword/OCR/caption matches.
            ranked_ids, scores = _keyword_search(conn, q.text, where, params)
            match_kind = "keyword"
        # Semantic only when explicitly asked, or as an opt-in fallback when the
        # keyword search found nothing. Never silently dumps similar photos.
        if q.semantic or (not ranked_ids and q.semantic_fallback):
            sem_ids, sem_scores = _semantic_search(
                conn, q.text, where, params, q.min_score)
            if sem_ids:
                ranked_ids, scores, match_kind = sem_ids, sem_scores, "semantic"
    else:
        rows = conn.execute(
            f"SELECT p.id FROM photos p WHERE {where} ORDER BY p.date_taken DESC",
            params,
        ).fetchall()
        ranked_ids = [r["id"] for r in rows]

    ranked_ids = ranked_ids[: q.limit]
    return [_hit(conn, pid, scores.get(pid, 0.0), match_kind) for pid in ranked_ids]


def _hit(conn, pid: int, score: float, match: str) -> Hit:
    r = conn.execute(
        "SELECT id, path, caption, tags, place, date_taken FROM photos WHERE id = ?",
        (pid,),
    ).fetchone()
    return Hit(
        id=r["id"], path=r["path"], score=score,
        caption=r["caption"] or "", tags=r["tags"] or "",
        place=r["place"] or "", date_taken=r["date_taken"] or "", match=match,
    )


def _device() -> str:
    try:
        import torch
        return "cuda" if torch.cuda.is_available() else "cpu"
    except Exception:
        return "cpu"
