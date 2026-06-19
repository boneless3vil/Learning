"""Interactive text menu for photocat.

Run `photocat menu` (or just `photocat` with no arguments) for a guided
experience: scan, geocode, enrich, dedup, search, and a full Settings editor
that can toggle any option and reset everything to defaults — no flags or SQL
to remember.

The Settings editor introspects the config dataclasses, so every option here
stays in sync automatically as settings are added.
"""
from __future__ import annotations

import dataclasses
from pathlib import Path

from rich.console import Console
from rich.table import Table

from . import db
from .config import Config, clean_path as _clean_path

console = Console()

# Config sections exposed in the Settings editor (attr name -> label).
SECTIONS = [
    ("scan", "Scanning"),
    ("dedup", "Duplicates"),
    ("enrich", "AI enrichment"),
    ("faces", "Faces"),
    ("organize", "Organize into folders"),
    ("geocode", "Geocoding"),
    ("search", "Search"),
]

# Plain-English description for each setting, shown in the editor so you don't
# need to know the developer field names. Keyed by section attr -> field.
HELP = {
    "scan": {
        "extensions": "Which file types to scan.",
        "recursive": "Also look inside sub-folders, not just the top folder.",
        "follow_symlinks": "Follow shortcut/linked folders into their real location (rarely needed).",
        "skip_hidden": "Ignore hidden files and folders (names starting with a dot).",
        "min_size_bytes": "Skip files smaller than this many bytes (filters out tiny/broken images).",
        "compute_phash": "Fingerprint each photo so near-duplicates (the same picture saved at a "
                         "different size or format) can be found. Needed for duplicate detection.",
    },
    "dedup": {
        "enabled": "Allow duplicate detection and removal.",
        "phash_threshold": "How visually close counts as a duplicate (0 = identical look; higher = looser).",
        "format_priority": "Best-to-worst file formats; the best-format copy in a group is kept.",
        "keeper_tiebreakers": "After format, keep the highest megapixels, then the largest file.",
        "duplicates_dir": "Where duplicate copies are moved. Blank = a 'duplicates' folder inside your photo folder.",
    },
    "enrich": {
        "enable_clip": "Enable concept/natural-language search (e.g. 'dog on a beach').",
        "enable_caption": "Write a sentence describing each photo.",
        "enable_tags": "List the objects/things detected in each photo.",
        "enable_ocr": "Read printed text in photos (documents, signs, ID cards).",
        "ocr_engine": "Which text reader to use: easyocr | paddle | tesseract | florence.",
        "device": "Where AI runs: 'cuda' (your GPU, fast), 'cpu' (slow), or 'auto'.",
        "batch_size": "How many photos the GPU handles at once (higher = faster, uses more memory).",
        "commit_every": "Save progress to the catalog every N photos.",
        "max_image_size": "Shrink very large photos to this many pixels before AI (0 = don't shrink).",
        "min_megapixels": "Skip AI on photos smaller than this (0 = process all).",
        "clip_model": "Concept-search model name (advanced — leave as-is unless you know it).",
        "clip_pretrained": "Trained weights for the concept model (advanced — leave as-is).",
        "caption_model": "Caption/tag model: Florence-2-large = sharper, Florence-2-base = faster.",
        "caption_max_tokens": "Maximum length of a generated caption (advanced).",
        "num_beams": "Caption wording quality vs speed — higher is better but slower (advanced).",
    },
    "faces": {
        "enabled": "Detect faces so you can search by person (needs an extra install).",
        "model_name": "Face-recognition model pack (advanced — leave as-is).",
        "det_size": "Face-detector resolution — higher finds smaller faces but is slower.",
        "min_det_score": "Confidence needed to keep a detected face (0 to 1).",
        "cluster_threshold": "How alike two faces must be to count as the same person (0 to 1).",
    },
    "organize": {
        "root": "Where year folders are created. Blank = inside your first photo folder.",
        "misc_folder": "Folder name for photos that have no camera date.",
        "require_camera_date": "Only a real camera (EXIF) date counts; otherwise the photo "
                              "goes to miscellaneous. Turn off to also use the file's timestamp.",
        "max_per_folder": "Split a year into month sub-folders once it exceeds this many photos. "
                          "0 = no limit (ignore the count, one folder per year).",
    },
    "geocode": {
        "enabled": "Turn GPS coordinates into place names, fully offline.",
    },
    "search": {
        "default_limit": "Most results to show per search.",
        "semantic_fallback": "If exact words find nothing, fall back to concept/visual matching.",
    },
}


def _ask(prompt: str, default: str = "") -> str:
    try:
        resp = input(prompt).strip()
        return resp if resp else default
    except (EOFError, KeyboardInterrupt):
        return "q"


def _open(cfg: Config):
    return db.init_db(cfg.resolved_catalog_path())


# --------------------------------------------------------------------------- #
#  Main menu                                                                  #
# --------------------------------------------------------------------------- #

def run(cfg_path: str | Path) -> None:
    cfg = Config.load(cfg_path)
    actions = {
        "1": ("Search", _do_search),
        "2": ("Recent searches", _do_recent),
        "3": ("Settings", _do_settings),
        "4": ("Scan photos (index files + EXIF)", _do_scan),
        "5": ("Organize into year folders", _do_organize),
        "6": ("Geocode (GPS -> place names)", _do_geocode),
        "7": ("Enrich with AI (captions / tags / search vectors)", _do_enrich),
        "8": ("Find / remove duplicates", _do_dedup),
        "9": ("Show catalog stats", _do_stats),
    }
    while True:
        console.print("\n[bold cyan]photocat[/] - main menu")
        for key, (label, _) in actions.items():
            console.print(f"  [bold]{key}[/]. {label}")
        console.print("  [bold]q[/]. Quit")
        choice = _ask("\nChoose: ").lower()
        if choice in ("q", "quit", "exit"):
            console.print("Bye.")
            return
        action = actions.get(choice)
        if not action:
            console.print("[yellow]Unknown choice.")
            continue
        try:
            action[1](cfg)
        except Exception as ex:
            console.print(f"[red]Error:[/] {ex}")


# --------------------------------------------------------------------------- #
#  Actions                                                                    #
# --------------------------------------------------------------------------- #

def _do_scan(cfg: Config) -> None:
    if not cfg.source_dirs:
        console.print("[yellow]No source folders set. Add them in Settings > Scanning.")
        return
    from . import scan as scan_mod
    stats = scan_mod.scan(cfg, _open(cfg))
    console.print(f"[green]Done.[/] {stats}")


def _do_geocode(cfg: Config) -> None:
    from . import geocode as geo
    geo.fill_places(_open(cfg))


def _do_enrich(cfg: Config) -> None:
    console.print("\nEnrich mode:")
    console.print("  [bold]1[/]. Normal (process new/unenriched photos)")
    console.print("  [bold]2[/]. Re-read OCR text on already-enriched photos")
    console.print("  [bold]3[/]. Force re-process everything")
    mode = _ask("Choose [1]: ", "1")
    limit_s = _ask("Limit to first N photos (blank = all): ")
    limit = int(limit_s) if limit_s.isdigit() else None
    from . import enrich as enrich_mod
    enrich_mod.enrich(cfg, _open(cfg), limit=limit,
                      force=(mode == "3"), redo_ocr=(mode == "2"))


def _do_organize(cfg: Config) -> None:
    from . import organize as organize_mod
    conn = _open(cfg)
    moves, root = organize_mod.build_plan(conn, cfg)
    organize_mod.print_plan(moves, root)
    if moves and _ask("\nMove these files into year folders now? (y/N): ").lower() in ("y", "yes"):
        organize_mod.apply_plan(conn, cfg, moves)


def _do_dedup(cfg: Config) -> None:
    from . import dedup as dedup_mod
    conn = _open(cfg)
    plan = dedup_mod.build_plan(conn, cfg)
    dedup_mod.print_plan(plan)
    if plan and _ask("\nMove duplicates aside now? (y/N): ").lower() in ("y", "yes"):
        dedup_mod.apply_plan(conn, cfg, plan)


def _do_search(cfg: Config) -> None:
    from .search import Query
    text = _ask("\nSearch text (keywords, blank to filter only): ")
    year = _ask("Year (blank = any): ")
    place = _ask("Place contains (blank = any): ")
    semantic = _ask("Concept/visual search instead of exact words? (y/N): ").lower() in ("y", "yes")
    q = Query(
        text=text or None,
        year=int(year) if year.isdigit() else None,
        place=place or None,
        limit=cfg.search.default_limit,
        semantic=semantic,
        semantic_fallback=cfg.search.semantic_fallback,
    )
    _run_query(cfg, q)


def _do_recent(cfg: Config) -> None:
    from .search import Query
    conn = _open(cfg)
    rows = db.recent_searches(conn, limit=15)
    if not rows:
        console.print("[yellow]No recent searches yet.")
        return
    console.print("\n[bold]Recent searches[/]")
    for i, r in enumerate(rows, 1):
        mode = "concept" if r["semantic"] else "keyword"
        console.print(f"  [bold]{i}[/]. {r['query']}  "
                      f"[dim]({mode}, {r['n_results']} hits, {(r['ts'] or '')[:16]})[/]")
    choice = _ask("\nRe-run which (number, blank = back): ")
    if not choice.isdigit() or not (1 <= int(choice) <= len(rows)):
        return
    r = rows[int(choice) - 1]
    q = Query(text=r["query"], semantic=bool(r["semantic"]),
              limit=cfg.search.default_limit,
              semantic_fallback=cfg.search.semantic_fallback)
    _run_query(cfg, q)


def _run_query(cfg: Config, q) -> None:
    from .search import search as run_search
    conn = _open(cfg)
    hits = run_search(conn, q)
    if q.text:
        db.record_search(conn, q.text, q.semantic, len(hits))
    if not hits:
        console.print("[yellow]No matches.[/] "
                      "[dim]Try fewer/different words, or answer 'y' to concept search.[/]")
        return
    table = Table(show_header=True, header_style="bold cyan")
    for col in ("#", "score", "date", "place", "caption / tags", "path"):
        table.add_column(col, overflow="fold")
    for i, h in enumerate(hits, 1):
        table.add_row(str(i), f"{h.score:.3f}", (h.date_taken or "")[:10],
                      h.place, (h.caption or h.tags), h.path)
    console.print(table)
    kind = hits[0].match or "filter"
    console.print(f"[dim]{len(hits)} result(s) ({kind} match).[/]")
    if kind == "semantic" and not q.semantic:
        console.print("[dim]No exact keyword match — showing closest visual matches.[/]")


def _do_stats(cfg: Config) -> None:
    conn = _open(cfg)
    total = db.count(conn)
    dups = db.count(conn, "is_duplicate = 1")
    table = Table(show_header=False)
    table.add_row("Photos (active)", str(total - dups))
    table.add_row("Duplicates quarantined", str(dups))
    table.add_row("AI-enriched", str(db.count(conn, "enriched = 1")))
    table.add_row("Geocoded", str(db.count(conn, "place IS NOT NULL AND place != ''")))
    table.add_row("Faces", str(conn.execute("SELECT COUNT(*) FROM faces").fetchone()[0]))
    console.print(table)


# --------------------------------------------------------------------------- #
#  Settings editor                                                            #
# --------------------------------------------------------------------------- #

def _do_settings(cfg: Config) -> None:
    while True:
        console.print("\n[bold cyan]Settings[/]")
        console.print("  [bold]0[/]. Library (catalog path + source folders)")
        for i, (_, label) in enumerate(SECTIONS, 1):
            console.print(f"  [bold]{i}[/]. {label}")
        console.print("  [bold]a[/]. Enable ALL features")
        console.print("  [bold]x[/]. Disable ALL features")
        console.print("  [bold]r[/]. Reset ALL settings to defaults")
        console.print("  [bold]s[/]. Save and go back")
        console.print("  [bold]b[/]. Back without saving")
        choice = _ask("\nChoose: ").lower()

        if choice in ("b", "q"):
            return
        if choice == "s":
            cfg.save()
            console.print(f"[green]Saved[/] {cfg._config_path}")
            return
        if choice == "a":
            cfg.set_all_features(True)
            console.print("[green]All features ON[/] (choose 's' to save).")
            continue
        if choice == "x":
            cfg.set_all_features(False)
            console.print("[green]All features OFF[/] (choose 's' to save).")
            continue
        if choice == "r":
            if _ask("Reset every setting to defaults? (y/N): ").lower() in ("y", "yes"):
                cfg.reset_to_defaults(keep_library=True)
                console.print("[green]Reset to defaults[/] (catalog + sources kept). "
                              "Choose 's' to save.")
            continue
        if choice == "0":
            _edit_library(cfg)
            continue
        if choice.isdigit() and 1 <= int(choice) <= len(SECTIONS):
            attr, label = SECTIONS[int(choice) - 1]
            _edit_section(getattr(cfg, attr), label, attr)
            continue
        console.print("[yellow]Unknown choice.")


def _edit_library(cfg: Config) -> None:
    console.print("\n[bold]Library[/]")
    console.print(f"  catalog: {cfg.catalog_path}")
    console.print("  source folders:")
    if cfg.source_dirs:
        for i, d in enumerate(cfg.source_dirs, 1):
            console.print(f"    {i}. {d}")
    else:
        console.print("    (none)")

    val = _clean_path(_ask("\nNew catalog path (blank = keep): "))
    if val and val.lower() != "q":
        cfg.catalog_path = val

    console.print("\nEnter source folder(s), one per line — spaces are fine, no quotes needed.")
    console.print("[dim]Press Enter on the first line to keep the current folders.[/]")
    first = _clean_path(_ask("Folder: "))
    if first and first.lower() != "q":
        new_dirs = [first]
        while True:
            nxt = _clean_path(_ask("Another folder (blank = done): "))
            if not nxt or nxt.lower() == "q":
                break
            new_dirs.append(nxt)
        cfg.source_dirs = [str(Path(p).expanduser()) for p in new_dirs]


def _fmt_value(v) -> str:
    """Compact, quote-free display of a setting's current value."""
    if isinstance(v, list):
        s = ", ".join(str(x) for x in v)
    else:
        s = str(v)
    return s if len(s) <= 70 else s[:67] + "..."


def _edit_section(section, label: str, section_key: str = "") -> None:
    """Generic editor: lists fields with plain-English descriptions and current values."""
    help_for = HELP.get(section_key, {})
    while True:
        fields = dataclasses.fields(section)
        console.print(f"\n[bold]{label}[/] settings:")
        for i, f in enumerate(fields, 1):
            console.print(f"  [bold]{i}[/]. {f.name}  [cyan][{_fmt_value(getattr(section, f.name))}][/]")
            desc = help_for.get(f.name)
            if desc:
                console.print(f"      [dim]{desc}[/]")
        console.print("  [bold]b[/]. Back")
        choice = _ask("\nEdit which (number): ").lower()
        if choice in ("b", "q", ""):
            return
        if not (choice.isdigit() and 1 <= int(choice) <= len(fields)):
            console.print("[yellow]Unknown choice.")
            continue
        f = fields[int(choice) - 1]
        desc = help_for.get(f.name)
        if desc:
            console.print(f"[dim]{desc}[/]")
        _edit_field(section, f.name, getattr(section, f.name))


def _edit_field(section, name: str, cur) -> None:
    if isinstance(cur, bool):
        setattr(section, name, not cur)
        console.print(f"[green]{name} -> {not cur}[/]")
        return
    if isinstance(cur, list):
        val = _ask(f"{name} = {cur}\nNew comma-separated values (blank = keep): ")
        if val and val != "q":
            setattr(section, name, [v.strip() for v in val.split(",") if v.strip()])
        return
    val = _ask(f"{name} = {cur!r}\nNew value (blank = keep): ")
    if not val or val == "q":
        return
    try:
        if isinstance(cur, int):
            setattr(section, name, int(val))
        elif isinstance(cur, float):
            setattr(section, name, float(val))
        else:
            setattr(section, name, val)
        console.print(f"[green]{name} -> {getattr(section, name)!r}[/]")
    except ValueError:
        console.print(f"[red]'{val}' is not valid for {name}.")
