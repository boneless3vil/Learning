# photocat — searchable photo catalog

Organize and **search** a large photo library (20,000+) by what's *in* the
photo, when it was taken, where, and (optionally) who's in it.

Unlike the old folder-based PhotoMover, photocat does **not** shuffle your
photos into one-object-per-folder trees (a photo with a person *and* a dog *and*
a beach can only live in one folder). Instead it scans each photo **once** into
a single searchable catalog (`photocat.db`, plain SQLite) that you can query
along *any* axis at the same time:

```
photocat search "kids playing in snow" --from 2018 --to 2020 --place Colorado
```

Your original files stay where they are. Only **duplicates** are moved aside,
and only when you ask.

---

## What it captures per photo

| Axis | How | Needs |
|------|-----|-------|
| **Date taken, camera, GPS** | EXIF | core (fast) |
| **Place name** (City, Region, Country) | offline reverse-geocode from GPS | core |
| **Semantic concept** ("dog on a beach") | OpenCLIP image embedding | AI step |
| **Objects / tags / caption / text-in-image** | Florence-2 (replaces YOLO; thousands of concepts, not 80) | AI step |
| **People by name** | InsightFace face clustering + your labels | optional |
| **Duplicates** | SHA-256 (exact) + perceptual hash (same picture, any format/res) | core |

EXIF and AI signals are folded into one search blob, so `"beach 2019"` matches
even when only the GPS/date knew the year.

---

## Install

photocat's **core** (scan, dedup, metadata search) needs only light packages.
The **AI enrichment** step needs PyTorch — install the CUDA build to use your
RTX 4070.

> ⚠️ **Use the Python 3.11 conda env, not a 3.13 venv.** CUDA PyTorch has no
> wheels for Python 3.13, which is why `pip install torch ...cu121` failed
> earlier. Always confirm which Python you're in before installing (below).

```powershell
# 1) Create + ENTER the env. If your shell auto-activates another venv,
#    'deactivate' it first so conda wins.
conda create -n photocat python=3.11 -y
deactivate            # leave any auto-activated venv (ignore "not in venv" error)
conda activate photocat

# 2) VERIFY you are actually in the photocat env — this MUST print the
#    miniforge\envs\photocat path. If it doesn't, run `conda init powershell`
#    once, restart the terminal, and `conda activate photocat` again.
python -c "import sys; print(sys.executable)"

# 3) From the smartFotoMove folder, install photocat itself (core only).
#    This registers a `photocat` command you can run from ANY directory.
cd "C:\Users\JonathanBaldwin\OneDrive - sinoverpi\Documents\03_COMPUTER\Python\smartFotoMove"
pip install -e .

# 4) AI step: install CUDA PyTorch (cu124 = torch 2.6, verified for py3.11),
#    then the AI extras. ~2.5 GB, one time.
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu124
pip install -e ".[ai]"
python -c "import torch; print('CUDA available:', torch.cuda.is_available())"  # -> True
```

Optional extras:

```powershell
pip install -e ".[heic]"    # iPhone .HEIC support
pip install -e ".[faces]"   # faces -> names (InsightFace)
```

> Once installed, the `photocat` command works from any folder while the env is
> active — you do **not** need to `cd` into the project or use `python -m`.

---

## Usage

### Interactive menu (easiest)

After `init`, run `photocat` with no arguments (or `photocat menu`):

```
1. Search                 6. Geocode (GPS -> place names)
2. Recent searches        7. Enrich with AI
3. Settings               8. Find / remove duplicates
4. Scan photos            9. Show catalog stats
5. Organize into year folders
```

**Settings** is a full editor that can toggle any option (OCR, faces, device,
batch size…), **enable/disable ALL features** at once, and **reset to defaults**.
**Recent searches** lists your past queries and re-runs any of them. No flags or
SQL to remember.

```powershell
photocat            # opens the menu
```

### Command line (scriptable)

```powershell
# 1. Create the catalog + config (point at one or more folders)
photocat init --source "D:\Photos" --source "E:\OldPhotos"

# 2. Index files: hashes, dimensions, EXIF date/camera/GPS, perceptual hash (fast)
photocat scan

# 3. Turn GPS into place names (offline, no network)
photocat geocode

# 4. AI pass: CLIP embeddings + Florence-2 caption/tags (uses the GPU; resumable)
photocat enrich

# 5. Organize into year folders (camera date); undated -> miscellaneous\
photocat organize               # preview the plan
photocat organize --apply       # move files into YYYY\ folders (paths stay searchable)

# 6. Duplicates — preview first, then apply
photocat dedup
photocat dedup --apply          # moves losers into duplicates\

# 6. Search — exact keyword/OCR/caption match by default (precise, few results)
photocat search "motor vehicles"          # only photos whose text has both words
photocat search "california identification"
photocat search --year 2021 --place Hawaii
photocat search --camera Canon
photocat search "dog on the beach" --semantic   # rank by visual concept (CLIP)
photocat recent                            # list past searches

# 7. Pull matches into a folder (e.g. to share)
photocat export "sunset over water" .\exports\sunsets

# Summary
photocat stats
```

> Prefer not to install? You can still run it as a module from inside the
> `smartFotoMove` folder: `python -m photocat <command>`.

Re-running `scan` / `enrich` only processes **new or changed** photos, so you
can add the next batch of pictures anytime and re-run — it resumes, never
redoes work.

```powershell
photocat enrich --redo-ocr   # add OCR text to ALREADY-enriched photos (cheap;
                             #   doesn't recompute captions/CLIP)
photocat enrich --force      # recompute everything from scratch
```

### Reading text in images (OCR)

Captions/tags describe what a photo *looks like* ("an identification card");
they do **not** transcribe printed text. To make the words on documents, signs,
ID cards, and screenshots searchable, turn on **OCR** (off by default because
it's slow and useless for ordinary snapshots):

- Menu: **Settings > AI enrichment > enable_ocr**, or set `"enable_ocr": true`
  in the config.
- Then `photocat enrich --redo-ocr` to backfill text on photos you already
  enriched, and search by the words on them (e.g. a name or city on an ID card).

**OCR engine** (`enrich.ocr_engine`):
- **`easyocr`** (default) — reads at full resolution, reuses the project's
  PyTorch so it runs on your **GPU**. Good on clear small text. (`pip install -e ".[easyocr]"`)
- **`tesseract`** — lightest; needs the Tesseract binary (`pip install -e ".[tesseract]"`).
- **`paddle`** — strong on dense text, but the current paddlepaddle 3.x **CPU**
  build is unstable on Windows; use only with a working GPU/known-good build.
- **`florence`** — no extra install, but downsamples images to ~768px, so it
  misses small text.

> **Limit:** very small, low-contrast micro-print (e.g. the tiny "Department of
> Motor Vehicles" header on a California ID) is below what *any* general OCR
> engine reads reliably. The card is still findable by its legible text — name,
> city, "identification", DOB, etc.

### How search picks results

- **Default = keyword:** returns only photos whose text (caption + tags + OCR +
  place + filename) contains **all** your significant words. Precise — a few hits
  or none, never a big pile.
- **`--semantic` (or "concept search" in the menu):** ranks photos by visual
  similarity using CLIP. Use it for vibes ("sunset over water") rather than exact
  words. CLIP is poor at reading text, so it's the wrong tool for words on a page.

### Faces (optional)

```powershell
# Menu: Settings > Faces > enabled, or set "faces": {"enabled": true} in config.
photocat enrich
photocat faces cluster              # group similar faces into person_1, person_2...
photocat faces list
photocat faces name person_3 "Aunt Mary"
photocat search --person "Aunt Mary"
```

---

## Configuration (`photocat.config.json`)

Every setting lives in one JSON file, grouped into sections. Edit it directly,
or use the menu's **Settings** editor (which can also **reset to defaults**:
`photocat config reset`). Defaults are "necessary on, niche off" — CLIP, caption,
tags, dedup, and geocode are on; OCR and faces are off.

**Top level**
- `catalog_path` — the SQLite catalog file.
- `source_dirs` — folders to scan. `photocat init` with no `--source` defaults to
  your **Pictures** folder; change it anytime in Settings > Library.

**`scan`** — `extensions`, `recursive`, `follow_symlinks`, `skip_hidden`,
`min_size_bytes`, `compute_phash` (needed for near-duplicate detection).

**`dedup`**
- `format_priority` — **your quality hierarchy**, best first. The keeper in each
  duplicate group is chosen by this order, then tie-breakers. Default ranks
  RAW > TIFF > PNG > HEIC > JPEG > WEBP > BMP/GIF.
- `phash_threshold` — how visually-close counts as a duplicate (0 = identical
  look; 5 = tolerant of recompression/resizing).
- `keeper_tiebreakers` — `["megapixels", "size_bytes"]`.
- `duplicates_dir` — where losers are moved. Blank = **auto**: a `duplicates`
  subfolder of your first source folder (e.g. `D:\Photos\duplicates`). It's
  excluded from scans, so quarantined dupes never get re-indexed. Set a path to
  override.

**`enrich`**
- `enable_clip` / `enable_caption` / `enable_tags` / `enable_ocr` — toggle each AI signal.
- `ocr_engine` — `easyocr` (default) / `paddle` / `tesseract` / `florence` (see OCR section).
- `device` — `auto` / `cuda` / `cpu`.
- `batch_size` — images CLIP embeds at once (raise for more speed if VRAM allows).
- `max_image_size` — downscale long edge before the models (saves time/VRAM; 0 = off).
- `min_megapixels` — skip enriching images smaller than this (0 = all).
- `caption_model` — `microsoft/Florence-2-large` (default) or `-base` (faster, less sharp).
- `caption_max_tokens`, `num_beams`, `commit_every`.

**`faces`** — `enabled`, `model_name`, `det_size`, `min_det_score`, `cluster_threshold`.

**`organize`** — move photos into folders so Explorer stays fast on huge libraries.
- `root` — where year folders are created. Blank = inside your first source folder.
- `require_camera_date` — only a real camera (EXIF) date counts; otherwise the photo
  goes to `miscellaneous`. Set `false` to also use the file timestamp as a fallback.
- `misc_folder` — name of the no-camera-date folder (default `miscellaneous`).
- `max_per_folder` — split a year into month sub-folders (`2019/2019-07`) once it
  exceeds this many photos. **`0` = no limit: ignore the count, one folder per year.**

**`geocode`** — `enabled`. **`search`** — `default_limit`, `prefer_semantic`.

> **Don't change `transformers` from 4.44.2.** Florence-2's bundled code breaks on
> newer versions (verified). The pin is set in `requirements.txt`/`pyproject.toml`.

---

## How duplicates are handled

1. **Exact** copies are found by SHA-256.
2. **Same picture, different file** (re-saved as a different format, resolution,
   or quality) is found by perceptual hash within `phash_threshold`.
3. In each group the **keeper** is the best file per your `format_priority` +
   tie-breakers. Everything else is **moved** (never deleted) into `_duplicates\`
   and flagged in the catalog, so the action is fully reversible and the
   duplicates are excluded from normal searches.

---

## Notes

- The catalog is a normal SQLite file — once you're comfortable you can open it
  in any DB browser and write your own SQL, or build a web UI on top without
  changing anything here.
- 20K photos: scan is minutes; the AI `enrich` pass is the long one (roughly a
  few hours on the RTX 4070 with Florence-2-base + CLIP) and is fully resumable.
- `make_test_images.py` generates synthetic images (with EXIF + deliberate
  duplicates) to try the pipeline quickly.
