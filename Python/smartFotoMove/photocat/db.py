"""SQLite catalog: schema, full-text index, and access helpers.

The catalog is a single ``.db`` file. ``photos`` holds one row per image with
all extracted metadata and AI signals. ``photos_fts`` is an FTS5 index over the
text fields so keyword search is fast. CLIP vectors are stored as BLOBs and
loaded into numpy at search time (20K x 512 floats is ~40MB — trivial).
"""
from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any, Iterable, Optional

SCHEMA_VERSION = 1

SCHEMA = """
CREATE TABLE IF NOT EXISTS meta (
    key TEXT PRIMARY KEY,
    value TEXT
);

CREATE TABLE IF NOT EXISTS photos (
    id            INTEGER PRIMARY KEY,
    path          TEXT NOT NULL,          -- current location on disk
    original_path TEXT NOT NULL,          -- where first discovered
    filename      TEXT,
    ext           TEXT,                   -- lower-case, no dot
    size_bytes    INTEGER,
    width         INTEGER,
    height        INTEGER,
    megapixels    REAL,
    sha256        TEXT,                   -- exact-duplicate key
    phash         TEXT,                   -- perceptual hash (16 hex chars)

    date_taken    TEXT,                   -- ISO 8601, best available
    date_source   TEXT,                   -- 'exif' | 'file'
    year          INTEGER,
    camera_make   TEXT,
    camera_model  TEXT,
    gps_lat       REAL,
    gps_lon       REAL,
    place         TEXT,                   -- "City, Region, Country" (geocoded)

    caption       TEXT,                   -- AI scene description
    tags          TEXT,                   -- comma-separated detected objects/tags
    ocr_text      TEXT,                   -- text found inside the image
    search_text   TEXT,                   -- combined blob fed to FTS

    clip_vector   BLOB,                   -- float32 embedding for semantic search

    is_duplicate  INTEGER DEFAULT 0,      -- 1 if moved aside as a dup
    duplicate_of  INTEGER,                -- photos.id of the keeper
    dup_group     INTEGER,                -- group id shared by visual dupes

    scanned       INTEGER DEFAULT 1,
    enriched      INTEGER DEFAULT 0,      -- AI signals computed?
    created_at    TEXT DEFAULT (datetime('now')),
    updated_at    TEXT DEFAULT (datetime('now'))
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_photos_path ON photos(path);
CREATE INDEX IF NOT EXISTS idx_photos_sha256 ON photos(sha256);
CREATE INDEX IF NOT EXISTS idx_photos_phash  ON photos(phash);
CREATE INDEX IF NOT EXISTS idx_photos_year   ON photos(year);
CREATE INDEX IF NOT EXISTS idx_photos_enriched ON photos(enriched);
CREATE INDEX IF NOT EXISTS idx_photos_dup    ON photos(is_duplicate);

-- Full-text index over one composed blob (caption + tags + ocr + place + year
-- + camera + filename). One column keeps free-text search dead simple and is
-- kept in sync from photos.search_text by the triggers below.
CREATE VIRTUAL TABLE IF NOT EXISTS photos_fts USING fts5(
    search_text, content='photos', content_rowid='id'
);

CREATE TRIGGER IF NOT EXISTS photos_ai AFTER INSERT ON photos BEGIN
    INSERT INTO photos_fts(rowid, search_text) VALUES (new.id, new.search_text);
END;
CREATE TRIGGER IF NOT EXISTS photos_ad AFTER DELETE ON photos BEGIN
    INSERT INTO photos_fts(photos_fts, rowid, search_text) VALUES ('delete', old.id, old.search_text);
END;
CREATE TRIGGER IF NOT EXISTS photos_au AFTER UPDATE ON photos BEGIN
    INSERT INTO photos_fts(photos_fts, rowid, search_text) VALUES ('delete', old.id, old.search_text);
    INSERT INTO photos_fts(rowid, search_text) VALUES (new.id, new.search_text);
END;

-- Optional faces support.
CREATE TABLE IF NOT EXISTS persons (
    id   INTEGER PRIMARY KEY,
    name TEXT UNIQUE
);
CREATE TABLE IF NOT EXISTS faces (
    id         INTEGER PRIMARY KEY,
    photo_id   INTEGER NOT NULL REFERENCES photos(id) ON DELETE CASCADE,
    person_id  INTEGER REFERENCES persons(id),
    bbox       TEXT,
    embedding  BLOB,
    det_score  REAL
);
CREATE INDEX IF NOT EXISTS idx_faces_photo  ON faces(photo_id);
CREATE INDEX IF NOT EXISTS idx_faces_person ON faces(person_id);

-- Recent searches, for the menu's "Recent searches" list.
CREATE TABLE IF NOT EXISTS search_history (
    id        INTEGER PRIMARY KEY,
    query     TEXT NOT NULL,
    semantic  INTEGER DEFAULT 0,
    n_results INTEGER,
    ts        TEXT DEFAULT (datetime('now'))
);
"""


def connect(path: str | Path) -> sqlite3.Connection:
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    conn.execute("PRAGMA foreign_keys=ON;")
    return conn


def init_db(path: str | Path) -> sqlite3.Connection:
    conn = connect(path)
    conn.executescript(SCHEMA)
    conn.execute(
        "INSERT OR IGNORE INTO meta(key, value) VALUES ('schema_version', ?)",
        (str(SCHEMA_VERSION),),
    )
    conn.commit()
    return conn


def get_photo_by_path(conn: sqlite3.Connection, path: str) -> Optional[sqlite3.Row]:
    return conn.execute("SELECT * FROM photos WHERE path = ?", (path,)).fetchone()


def insert_photo(conn: sqlite3.Connection, fields: dict[str, Any]) -> int:
    cols = ", ".join(fields)
    placeholders = ", ".join("?" for _ in fields)
    cur = conn.execute(
        f"INSERT INTO photos ({cols}) VALUES ({placeholders})",
        tuple(fields.values()),
    )
    return cur.lastrowid


def update_photo(conn: sqlite3.Connection, photo_id: int, fields: dict[str, Any]) -> None:
    assignments = ", ".join(f"{k} = ?" for k in fields)
    conn.execute(
        f"UPDATE photos SET {assignments}, updated_at = datetime('now') WHERE id = ?",
        (*fields.values(), photo_id),
    )


def iter_photos(
    conn: sqlite3.Connection,
    where: str = "",
    params: Iterable[Any] = (),
) -> Iterable[sqlite3.Row]:
    sql = "SELECT * FROM photos"
    if where:
        sql += f" WHERE {where}"
    yield from conn.execute(sql, tuple(params))


def count(conn: sqlite3.Connection, where: str = "", params: Iterable[Any] = ()) -> int:
    sql = "SELECT COUNT(*) FROM photos"
    if where:
        sql += f" WHERE {where}"
    return conn.execute(sql, tuple(params)).fetchone()[0]


def set_updated_now(conn: sqlite3.Connection, photo_id: int) -> None:
    conn.execute("UPDATE photos SET updated_at = datetime('now') WHERE id = ?", (photo_id,))


def record_search(conn: sqlite3.Connection, query: str, semantic: bool, n_results: int) -> None:
    """Log a search so it appears in 'Recent searches'. De-dupes the immediate repeat."""
    query = (query or "").strip()
    if not query:
        return
    last = conn.execute(
        "SELECT query, semantic FROM search_history ORDER BY id DESC LIMIT 1"
    ).fetchone()
    if last and last["query"] == query and bool(last["semantic"]) == bool(semantic):
        return
    conn.execute(
        "INSERT INTO search_history(query, semantic, n_results) VALUES (?,?,?)",
        (query, int(semantic), n_results),
    )
    conn.commit()


def recent_searches(conn: sqlite3.Connection, limit: int = 15) -> list[sqlite3.Row]:
    return conn.execute(
        "SELECT query, semantic, n_results, ts FROM search_history "
        "ORDER BY id DESC LIMIT ?", (limit,)
    ).fetchall()


def compose_search_text(values: dict[str, Any]) -> str:
    """Build the single free-text blob FTS indexes.

    Folds AI signals (caption/tags/ocr) together with metadata (place/year/
    camera/filename) so one keyword search hits any of them — e.g. "beach 2019"
    matches even when only EXIF knew the year. Pass a dict or sqlite3.Row-like
    mapping of the photo's effective (post-update) field values.
    """
    import os

    filename = values.get("filename") or ""
    name_words = os.path.splitext(filename)[0].replace("_", " ").replace("-", " ")
    parts = [
        values.get("caption") or "",
        values.get("tags") or "",
        values.get("ocr_text") or "",
        values.get("place") or "",
        str(values.get("year") or ""),
        values.get("camera_make") or "",
        values.get("camera_model") or "",
        name_words,
    ]
    return " ".join(p for p in parts if p).strip()
