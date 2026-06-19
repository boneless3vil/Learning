"""EXIF / metadata extraction using Pillow (+ piexif as a fallback).

Returns a plain dict of the fields the catalog cares about: capture date,
camera make/model, GPS coordinates, and pixel dimensions. Everything is
best-effort — missing or malformed tags never raise.
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from PIL import Image, ExifTags

# Register HEIC/HEIF support if pillow-heif is installed (optional).
try:  # pragma: no cover - optional dependency
    import pillow_heif  # type: ignore

    pillow_heif.register_heif_opener()
except Exception:
    pass

_TAG_NAME = {v: k for k, v in ExifTags.TAGS.items()}  # name -> id
_GPS_NAME = {v: k for k, v in ExifTags.GPSTAGS.items()}


def _to_float(value: Any) -> Optional[float]:
    try:
        if isinstance(value, tuple) and len(value) == 2:  # IFDRational as (num, den)
            return value[0] / value[1] if value[1] else None
        return float(value)
    except (TypeError, ZeroDivisionError, ValueError):
        return None


def _dms_to_decimal(dms, ref) -> Optional[float]:
    try:
        d = _to_float(dms[0]) or 0.0
        m = _to_float(dms[1]) or 0.0
        s = _to_float(dms[2]) or 0.0
        dec = d + m / 60.0 + s / 3600.0
        if ref in ("S", "W"):
            dec = -dec
        return dec
    except (TypeError, IndexError):
        return None


def _parse_exif_datetime(value: str) -> Optional[str]:
    # EXIF stores "YYYY:MM:DD HH:MM:SS"
    for fmt in ("%Y:%m:%d %H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y:%m:%d"):
        try:
            return datetime.strptime(value.strip(), fmt).isoformat()
        except (ValueError, AttributeError):
            continue
    return None


def extract(path: str | Path) -> dict[str, Any]:
    """Extract metadata for one image. Always returns a dict (never raises)."""
    path = Path(path)
    out: dict[str, Any] = {
        "width": None, "height": None,
        "date_taken": None, "date_source": None,
        "camera_make": None, "camera_model": None,
        "gps_lat": None, "gps_lon": None,
    }

    try:
        with Image.open(path) as img:
            out["width"], out["height"] = img.size
            exif = img.getexif()
    except Exception:
        exif = None

    if exif:
        # Camera
        make = exif.get(_TAG_NAME.get("Make"))
        model = exif.get(_TAG_NAME.get("Model"))
        out["camera_make"] = str(make).strip() if make else None
        out["camera_model"] = str(model).strip() if model else None

        # Capture date — prefer the EXIF sub-IFD's DateTimeOriginal.
        dt_raw = None
        try:
            sub = exif.get_ifd(ExifTags.IFD.Exif)
            dt_raw = sub.get(_TAG_NAME.get("DateTimeOriginal")) or sub.get(
                _TAG_NAME.get("DateTimeDigitized")
            )
        except Exception:
            pass
        dt_raw = dt_raw or exif.get(_TAG_NAME.get("DateTime"))
        if dt_raw:
            parsed = _parse_exif_datetime(str(dt_raw))
            if parsed:
                out["date_taken"] = parsed
                out["date_source"] = "exif"

        # GPS
        try:
            gps = exif.get_ifd(ExifTags.IFD.GPSInfo)
            if gps:
                lat = _dms_to_decimal(
                    gps.get(_GPS_NAME["GPSLatitude"]), gps.get(_GPS_NAME["GPSLatitudeRef"])
                )
                lon = _dms_to_decimal(
                    gps.get(_GPS_NAME["GPSLongitude"]), gps.get(_GPS_NAME["GPSLongitudeRef"])
                )
                out["gps_lat"], out["gps_lon"] = lat, lon
        except Exception:
            pass

    # Fall back to the filesystem modification time if no EXIF date.
    if not out["date_taken"]:
        try:
            mtime = path.stat().st_mtime
            out["date_taken"] = datetime.fromtimestamp(mtime).isoformat()
            out["date_source"] = "file"
        except OSError:
            pass

    return out
