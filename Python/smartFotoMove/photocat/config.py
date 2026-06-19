"""Configuration for photocat.

A single JSON file (``photocat.config.json``) holds every tunable, grouped into
sections (scan / dedup / enrich / faces / geocode / search). Defaults work
out-of-the-box on a CUDA GPU. The loader is tolerant: unknown keys are ignored
and missing sections fall back to defaults, so old config files keep working and
new settings appear automatically when you re-save (e.g. via the menu).
"""
from __future__ import annotations

import dataclasses
import json
import os
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Optional

CONFIG_FILENAME = "photocat.config.json"


def default_pictures_dir() -> str:
    """The user's Pictures folder (honours OneDrive/known-folder redirection)."""
    if os.name == "nt":
        try:
            import winreg
            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders",
            ) as k:
                val, _ = winreg.QueryValueEx(k, "My Pictures")
                return os.path.expandvars(val)
        except Exception:
            pass
    return str(Path.home() / "Pictures")


# Boolean capability flags toggled together by "enable/disable all".
FEATURE_FLAGS = [
    ("dedup", "enabled"),
    ("enrich", "enable_clip"), ("enrich", "enable_caption"),
    ("enrich", "enable_tags"), ("enrich", "enable_ocr"),
    ("faces", "enabled"),
    ("geocode", "enabled"),
]

# Image extensions photocat will catalog. Lower-case, with leading dot.
SUPPORTED_EXTS = (
    ".jpg", ".jpeg", ".png", ".bmp", ".webp", ".gif", ".tif", ".tiff",
    ".heic", ".heif", ".dng", ".cr2", ".cr3", ".nef", ".arw", ".raf", ".orf", ".rw2",
)

# Format quality ranking, BEST first. Decides which file in a duplicate group is
# the "keeper". Edit freely; anything not listed sorts last.
DEFAULT_FORMAT_PRIORITY = [
    "dng", "cr3", "cr2", "nef", "arw", "raf", "orf", "rw2",  # RAW (best)
    "tiff", "tif",
    "png",
    "heic", "heif",
    "jpeg", "jpg",
    "webp",
    "bmp", "gif",                                            # worst
]


@dataclass
class ScanConfig:
    # File types to index (override to add/remove formats).
    extensions: list[str] = field(default_factory=lambda: list(SUPPORTED_EXTS))
    recursive: bool = True               # descend into sub-folders
    follow_symlinks: bool = False
    skip_hidden: bool = True             # ignore dot-files / hidden dirs
    min_size_bytes: int = 1024           # skip tiny/corrupt files
    compute_phash: bool = True           # perceptual hash (needed for near-dup dedup)


@dataclass
class DedupConfig:
    enabled: bool = True
    # Hamming distance between perceptual hashes at/under which two images are
    # the "same picture" (different format/resolution/recompression).
    # 0 = identical look; 5 = tolerant of resizing/recompression.
    phash_threshold: int = 5
    format_priority: list[str] = field(default_factory=lambda: list(DEFAULT_FORMAT_PRIORITY))
    # Tie-breakers applied after format rank; higher value wins.
    keeper_tiebreakers: list[str] = field(default_factory=lambda: ["megapixels", "size_bytes"])
    # Where losing duplicates are moved. Blank = auto: a "duplicates" subfolder of
    # your first source folder. Set an absolute path (or one relative to the
    # config file) to override.
    duplicates_dir: str = ""


@dataclass
class EnrichConfig:
    # Which AI signals to compute.
    enable_clip: bool = True        # semantic natural-language search (recommended)
    enable_caption: bool = True     # Florence-2 detailed scene caption
    enable_tags: bool = True        # Florence-2 object/region tags
    enable_ocr: bool = False        # read printed text in the image (docs, signs, IDs)
    # Which engine reads text. "easyocr" (default) and "paddle"/"tesseract" read
    # at full resolution and catch small print; "florence" reuses the caption
    # model (no extra install, but downsamples to ~768px so it misses tiny text).
    ocr_engine: str = "easyocr"     # "easyocr" | "paddle" | "tesseract" | "florence"

    device: str = "auto"            # "auto" | "cuda" | "cpu"
    batch_size: int = 16            # images embedded together by CLIP (VRAM-bound)
    commit_every: int = 50          # DB commit cadence (photos)
    # Downscale the long edge to this before feeding the models (saves time/VRAM;
    # 0 disables). Models work at low res internally, so this is near-lossless.
    max_image_size: int = 1536
    min_megapixels: float = 0.0     # skip enriching images smaller than this (0 = all)

    # Models (all run locally).
    clip_model: str = "ViT-B-32"
    clip_pretrained: str = "laion2b_s34b_b79k"
    # Florence-2-large gives sharper captions/tags than -base (slower). MIT.
    caption_model: str = "microsoft/Florence-2-large"
    caption_max_tokens: int = 256
    num_beams: int = 3


@dataclass
class FacesConfig:
    enabled: bool = False           # detect faces so you can search by person
    model_name: str = "buffalo_l"   # InsightFace model pack
    det_size: int = 640             # detector input size (larger = small faces, slower)
    min_det_score: float = 0.5      # discard weak detections
    cluster_threshold: float = 0.5  # cosine similarity to group faces into one person


@dataclass
class OrganizeConfig:
    # Where year folders are created. Blank = inside your first source folder.
    root: str = ""
    misc_folder: str = "miscellaneous"   # for photos with no camera date
    # Only a real camera (EXIF) date counts as "dated"; otherwise -> miscellaneous.
    # Set False to also use the file's timestamp as a fallback date.
    require_camera_date: bool = True
    # Max photos before a year folder is split into month sub-folders
    # (e.g. 2019/2019-07). 0 = no limit: ignore the count, one folder per year.
    max_per_folder: int = 0


@dataclass
class GeocodeConfig:
    enabled: bool = True            # turn GPS into place names (offline)


@dataclass
class SearchConfig:
    default_limit: int = 50
    # When a keyword search finds nothing, fall back to CLIP visual ranking.
    # Off by default so literal searches return few precise hits (or none),
    # never a big pile of vaguely-similar photos. Use --semantic to force it.
    semantic_fallback: bool = False


@dataclass
class Config:
    # Absolute (or config-relative) path to the SQLite catalog file.
    catalog_path: str = "photocat.db"
    # Folders to scan (absolute paths recommended).
    source_dirs: list[str] = field(default_factory=list)

    scan: ScanConfig = field(default_factory=ScanConfig)
    dedup: DedupConfig = field(default_factory=DedupConfig)
    enrich: EnrichConfig = field(default_factory=EnrichConfig)
    faces: FacesConfig = field(default_factory=FacesConfig)
    organize: OrganizeConfig = field(default_factory=OrganizeConfig)
    geocode: GeocodeConfig = field(default_factory=GeocodeConfig)
    search: SearchConfig = field(default_factory=SearchConfig)

    _config_path: str = field(default=CONFIG_FILENAME, repr=False)

    # --- persistence -------------------------------------------------------
    @property
    def config_dir(self) -> Path:
        return Path(self._config_path).resolve().parent

    @classmethod
    def load(cls, path: str | Path) -> "Config":
        path = Path(path)
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)

        enrich_raw = dict(raw.get("enrich", {}))
        faces_raw = dict(raw.get("faces", {}))
        # Migrate the old enrich.enable_faces flag into the faces section.
        if "enabled" not in faces_raw and "enable_faces" in enrich_raw:
            faces_raw["enabled"] = enrich_raw["enable_faces"]

        cfg = cls(
            catalog_path=raw.get("catalog_path", "photocat.db"),
            source_dirs=raw.get("source_dirs", []),
            scan=_sub(ScanConfig, raw.get("scan")),
            dedup=_sub(DedupConfig, raw.get("dedup")),
            enrich=_sub(EnrichConfig, enrich_raw),
            faces=_sub(FacesConfig, faces_raw),
            organize=_sub(OrganizeConfig, raw.get("organize")),
            geocode=_sub(GeocodeConfig, raw.get("geocode")),
            search=_sub(SearchConfig, raw.get("search")),
        )
        # Heal any paths that were stored with stray quotes.
        cfg.catalog_path = clean_path(cfg.catalog_path)
        cfg.source_dirs = [clean_path(s) for s in cfg.source_dirs]
        cfg.dedup.duplicates_dir = clean_path(cfg.dedup.duplicates_dir)
        cfg.organize.root = clean_path(cfg.organize.root)
        cfg._config_path = str(path)
        return cfg

    def save(self, path: str | Path | None = None) -> None:
        path = Path(path or self._config_path)
        data = asdict(self)
        data.pop("_config_path", None)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        self._config_path = str(path)

    def reset_to_defaults(self, keep_library: bool = True) -> None:
        """Restore every setting section to its default.

        Defaults are deliberately "necessary on, niche off": CLIP + caption +
        tags + dedup + geocode are enabled; OCR and faces are off. With
        keep_library=True the catalog path and source folders are preserved
        (resetting those would orphan your existing catalog).
        """
        catalog, sources = self.catalog_path, list(self.source_dirs)
        self.scan = ScanConfig()
        self.dedup = DedupConfig()
        self.enrich = EnrichConfig()
        self.faces = FacesConfig()
        self.geocode = GeocodeConfig()
        self.search = SearchConfig()
        if not keep_library:
            self.catalog_path, self.source_dirs = "photocat.db", []
        else:
            self.catalog_path, self.source_dirs = catalog, sources

    # Resolve paths relative to the config file's directory.
    def resolved_catalog_path(self) -> Path:
        p = Path(self.catalog_path)
        return p if p.is_absolute() else (self.config_dir / p)

    def resolved_duplicates_dir(self) -> Path:
        d = self.dedup.duplicates_dir.strip()
        if not d:  # auto: <first source folder>/duplicates
            base = Path(self.source_dirs[0]) if self.source_dirs else self.config_dir
            return base / "duplicates"
        p = Path(d)
        return p if p.is_absolute() else (self.config_dir / p)

    def resolved_organize_root(self) -> Path:
        d = self.organize.root.strip()
        if not d:  # default: organize inside the first source folder
            return Path(self.source_dirs[0]) if self.source_dirs else self.config_dir
        p = Path(d)
        return p if p.is_absolute() else (self.config_dir / p)

    def set_all_features(self, on: bool) -> None:
        """Turn every capability flag on or off at once."""
        for section, attr in FEATURE_FLAGS:
            setattr(getattr(self, section), attr, on)


def _sub(cls, data: Optional[dict]) -> Any:
    """Build a (sub)config dataclass from a dict, ignoring unknown keys."""
    known = {f.name for f in dataclasses.fields(cls)}
    return cls(**{k: v for k, v in (data or {}).items() if k in known})


def clean_path(s: str) -> str:
    """Normalise a user-entered path: drop surrounding quotes/whitespace.

    Lets you paste a plain Windows path (spaces and all) with or without quotes
    and store it cleanly — e.g.  "'C:\\Users\\Me\\My Pics'"  ->  C:\\Users\\Me\\My Pics
    """
    if not isinstance(s, str):
        return s
    s = s.strip()
    while len(s) >= 2 and s[0] in "\"'" and s[-1] == s[0]:
        s = s[1:-1].strip()
    return s


def find_config(start: Optional[str | Path] = None) -> Optional[Path]:
    """Search the current dir and its parents for a config file."""
    d = Path(start or Path.cwd()).resolve()
    for candidate in [d, *d.parents]:
        p = candidate / CONFIG_FILENAME
        if p.exists():
            return p
    return None
