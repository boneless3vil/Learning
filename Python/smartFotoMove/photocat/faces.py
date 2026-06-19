"""Optional face detection & recognition (InsightFace).

Disabled by default (``enrich.enable_faces`` in config). When on, each photo's
faces are detected and their embeddings stored. You then:
  1. ``photocat faces cluster``  -> groups similar faces into unnamed people
  2. ``photocat faces name <cluster_id> "Aunt Mary"`` -> label a person
Thereafter ``photocat search --person "Aunt Mary"`` finds their photos.

Requires extra installs:
    pip install insightface onnxruntime-gpu   (or onnxruntime for CPU)
"""
from __future__ import annotations

import json

import numpy as np
from PIL import Image

from . import db


def load(device: str, cfg=None):
    """Load the InsightFace app, or raise a friendly error if missing."""
    try:
        from insightface.app import FaceAnalysis
    except ImportError as e:
        raise ImportError(
            "Faces are enabled but insightface is not installed. Run:\n"
            "    pip install insightface onnxruntime-gpu\n"
            "(use onnxruntime instead of -gpu for CPU-only)."
        ) from e

    fc = cfg.faces if cfg is not None else None
    model_name = fc.model_name if fc else "buffalo_l"
    det = fc.det_size if fc else 640
    providers = (
        ["CUDAExecutionProvider", "CPUExecutionProvider"]
        if device == "cuda" else ["CPUExecutionProvider"]
    )
    app = FaceAnalysis(name=model_name, providers=providers)
    app.prepare(ctx_id=0 if device == "cuda" else -1, det_size=(det, det))
    return app


def detect_and_store(conn, app, photo_id: int, img: Image.Image, cfg=None) -> int:
    min_score = cfg.faces.min_det_score if cfg is not None else 0.5
    # InsightFace expects BGR ndarray.
    arr = np.asarray(img)[:, :, ::-1].copy()
    faces = app.get(arr)
    # Replace any prior faces for this photo (idempotent re-runs).
    conn.execute("DELETE FROM faces WHERE photo_id = ?", (photo_id,))
    kept = 0
    for f in faces:
        if float(f.det_score) < min_score:
            continue
        emb = f.normed_embedding.astype("float32")
        bbox = json.dumps([round(float(x), 1) for x in f.bbox.tolist()])
        conn.execute(
            "INSERT INTO faces(photo_id, bbox, embedding, det_score) VALUES (?,?,?,?)",
            (photo_id, bbox, emb.tobytes(), float(f.det_score)),
        )
        kept += 1
    return kept


def cluster(conn, threshold: float = 0.5) -> int:
    """Greedy agglomerative clustering of un-named face embeddings.

    Faces with cosine similarity >= threshold join the same person. Returns the
    number of clusters (people) created. This is intentionally simple; refine by
    re-running after naming, or raise the threshold for stricter grouping.
    """
    rows = conn.execute(
        "SELECT id, embedding FROM faces WHERE person_id IS NULL"
    ).fetchall()
    if not rows:
        return 0

    embs = np.stack([np.frombuffer(r["embedding"], dtype="float32") for r in rows])
    ids = [r["id"] for r in rows]
    assigned = [-1] * len(ids)
    centroids: list[np.ndarray] = []

    for i in range(len(ids)):
        best, best_sim = -1, threshold
        for c, cen in enumerate(centroids):
            sim = float(np.dot(embs[i], cen))
            if sim >= best_sim:
                best, best_sim = c, sim
        if best == -1:
            centroids.append(embs[i].copy())
            assigned[i] = len(centroids) - 1
        else:
            assigned[i] = best

    # Materialise clusters as anonymous persons.
    cluster_to_person: dict[int, int] = {}
    for face_idx, cluster_id in zip(range(len(ids)), assigned):
        if cluster_id not in cluster_to_person:
            cur = conn.execute(
                "INSERT INTO persons(name) VALUES (?)", (f"person_{cluster_id+1}",)
            )
            cluster_to_person[cluster_id] = cur.lastrowid
        conn.execute(
            "UPDATE faces SET person_id = ? WHERE id = ?",
            (cluster_to_person[cluster_id], ids[face_idx]),
        )
    conn.commit()
    return len(cluster_to_person)


def rename_person(conn, old: str, new: str) -> bool:
    row = conn.execute("SELECT id FROM persons WHERE name = ?", (old,)).fetchone()
    if not row:
        return False
    conn.execute("UPDATE persons SET name = ? WHERE id = ?", (new, row["id"]))
    conn.commit()
    return True
