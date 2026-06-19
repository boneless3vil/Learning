"""Offline reverse geocoding: GPS coordinates -> "City, Region, Country".

Uses the ``reverse_geocoder`` package, which ships a local cities database, so
no network calls are made. Results are filled into ``photos.place`` so you can
search by location. Coordinates are batched for speed.
"""
from __future__ import annotations

from rich.console import Console

from . import db

console = Console()


def fill_places(conn) -> int:
    rows = conn.execute(
        "SELECT * FROM photos "
        "WHERE gps_lat IS NOT NULL AND gps_lon IS NOT NULL "
        "AND (place IS NULL OR place = '')"
    ).fetchall()
    if not rows:
        console.print("No un-geocoded photos with GPS data.")
        return 0

    try:
        import reverse_geocoder as rg
    except ImportError:
        console.print(
            "[yellow]reverse_geocoder not installed; skipping geocoding. "
            "Install it with: pip install reverse_geocoder"
        )
        return 0

    coords = [(r["gps_lat"], r["gps_lon"]) for r in rows]
    console.print(f"Reverse-geocoding {len(coords)} locations (offline)...")
    results = rg.search(coords)  # list of dicts: name, admin1, cc

    updated = 0
    for row, res in zip(rows, results):
        place = ", ".join(
            part for part in (res.get("name"), res.get("admin1"), res.get("cc")) if part
        )
        merged = {**dict(row), "place": place}
        db.update_photo(conn, row["id"], {
            "place": place,
            "search_text": db.compose_search_text(merged),
        })
        updated += 1
    conn.commit()
    console.print(f"[green]Geocoded {updated} photos.")
    return updated
