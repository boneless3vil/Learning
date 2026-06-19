"""Generate synthetic test images for smoke-testing photocat.

Creates a handful of distinct pictures plus deliberate duplicates at different
resolutions/formats so dedup has something to chew on. Adds EXIF date + GPS to
the JPEGs so scan/geocode have data.
"""
import os
from pathlib import Path

import piexif
from PIL import Image, ImageDraw

OUT = Path("test_images")
OUT.mkdir(exist_ok=True)


def base_image(seed: int, size=(1200, 900)) -> Image.Image:
    img = Image.new("RGB", size, (seed * 30 % 255, seed * 70 % 255, seed * 110 % 255))
    d = ImageDraw.Draw(img)
    # Some shapes so perceptual hashes differ between distinct images.
    d.rectangle([100, 100, 100 + seed * 40, 400], fill=(255, 255, 0))
    d.ellipse([400, 200, 700, 500 + seed * 10], fill=(0, 128, 255))
    d.text((50, 50), f"scene {seed}", fill=(255, 255, 255))
    return img


def exif_bytes(year: int, lat=37.7749, lon=-122.4194) -> bytes:
    def dms(v):
        v = abs(v)
        deg = int(v); m = int((v - deg) * 60); s = round((v - deg - m / 60) * 3600 * 100)
        return [(deg, 1), (m, 1), (s, 100)]
    zeroth = {piexif.ImageIFD.Make: b"TestCam", piexif.ImageIFD.Model: b"Model X"}
    exif = {piexif.ExifIFD.DateTimeOriginal: f"{year}:07:04 12:30:00".encode()}
    gps = {
        piexif.GPSIFD.GPSLatitudeRef: b"N" if lat >= 0 else b"S",
        piexif.GPSIFD.GPSLatitude: dms(lat),
        piexif.GPSIFD.GPSLongitudeRef: b"E" if lon >= 0 else b"W",
        piexif.GPSIFD.GPSLongitude: dms(lon),
    }
    return piexif.dump({"0th": zeroth, "Exif": exif, "GPS": gps})


# 4 distinct scenes as JPEG with EXIF (different years).
for i in range(1, 5):
    img = base_image(i)
    img.save(OUT / f"scene{i}.jpg", exif=exif_bytes(2018 + i))

# Duplicates of scene1: a high-res PNG (best), a small JPEG, and a webp.
s1 = base_image(1)
s1.save(OUT / "scene1_copy_hires.png")                       # bigger res, PNG
s1.resize((600, 450)).save(OUT / "scene1_copy_small.jpg")    # smaller JPEG
s1.resize((900, 675)).save(OUT / "scene1_copy.webp")         # webp

# Exact byte duplicate of scene2.
import shutil
shutil.copy2(OUT / "scene2.jpg", OUT / "scene2_exact_dup.jpg")

print("Test images written to", OUT.resolve())
for p in sorted(OUT.iterdir()):
    print(" ", p.name, f"{os.path.getsize(p)//1024}KB")
