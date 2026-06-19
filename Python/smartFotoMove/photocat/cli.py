"""photocat command-line interface.

Typical workflow:
    photocat init  --source "D:/Photos"      # create config + catalog
    photocat scan                            # index files + EXIF (fast)
    photocat geocode                         # GPS -> place names (offline)
    photocat enrich                          # AI captions/tags/CLIP (GPU)
    photocat dedup                           # preview duplicate groups
    photocat dedup --apply                   # move losers to _duplicates/
    photocat search "dog on the beach" --year 2019
    photocat export "birthday cake" ./out    # copy matches to a folder
"""
from __future__ import annotations

import shutil
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from . import db
from .config import CONFIG_FILENAME, Config, find_config

app = typer.Typer(add_completion=False, no_args_is_help=False,
                  help="Searchable photo catalog. Run with no command for an interactive menu.")
faces_app = typer.Typer(help="Optional face clustering / naming.")
app.add_typer(faces_app, name="faces")
config_app = typer.Typer(help="View or reset settings.")
app.add_typer(config_app, name="config")
console = Console()


@app.callback(invoke_without_command=True)
def _default(ctx: typer.Context):
    """Launch the interactive menu when no subcommand is given."""
    if ctx.invoked_subcommand is None:
        cfg_path = find_config()
        if not cfg_path:
            console.print("[yellow]No photocat.config.json found. Run [bold]photocat init[/] "
                          "first (e.g. photocat init --source \"D:\\Photos\").")
            raise typer.Exit(1)
        from . import menu
        menu.run(cfg_path)
        raise typer.Exit()


def _load_cfg(explicit: Optional[str] = None) -> Config:
    path = Path(explicit) if explicit else find_config()
    if not path or not Path(path).exists():
        console.print("[red]No photocat.config.json found. Run [bold]photocat init[/] first.")
        raise typer.Exit(1)
    return Config.load(path)


def _open(cfg: Config):
    return db.init_db(cfg.resolved_catalog_path())


# --------------------------------------------------------------------------- #

@app.command()
def init(
    source: list[str] = typer.Option(None, "--source", "-s", help="Folder(s) to scan. Repeatable."),
    catalog: str = typer.Option("photocat.db", help="Catalog DB filename."),
    here: str = typer.Option(".", help="Directory to write the config into."),
):
    """Create a config file and an empty catalog."""
    from .config import default_pictures_dir, clean_path
    if source:
        sources = [str(Path(clean_path(s)).expanduser().resolve()) for s in source]
    else:
        # Default to the user's Pictures folder when none is given.
        sources = [default_pictures_dir()]
        console.print(f"[dim]No --source given; defaulting to your Pictures folder:[/] {sources[0]}")
    cfg = Config(catalog_path=catalog, source_dirs=sources)
    cfg_path = Path(here).resolve() / CONFIG_FILENAME
    if cfg_path.exists():
        if not typer.confirm(f"{cfg_path} exists. Overwrite?"):
            raise typer.Exit()
    cfg.save(cfg_path)
    db.init_db(cfg.resolved_catalog_path())
    console.print(f"[green]Created[/] {cfg_path}")
    console.print(f"[green]Created[/] {cfg.resolved_catalog_path()}")
    console.print(f"[dim]Duplicates will go to:[/] {cfg.resolved_duplicates_dir()}")


@app.command()
def scan(config: Optional[str] = typer.Option(None, "--config", "-c")):
    """Index files: hashes, dimensions, EXIF (date/camera/GPS), perceptual hash."""
    cfg = _load_cfg(config)
    conn = _open(cfg)
    from . import scan as scan_mod
    stats = scan_mod.scan(cfg, conn)
    console.print(
        f"[green]Scan done.[/] new={stats['new']} updated={stats['updated']} "
        f"skipped={stats['skipped']} failed={stats['failed']}"
    )


@app.command()
def geocode(config: Optional[str] = typer.Option(None, "--config", "-c")):
    """Reverse-geocode GPS coordinates into place names (offline)."""
    cfg = _load_cfg(config)
    conn = _open(cfg)
    from . import geocode as geo
    geo.fill_places(conn)


@app.command()
def menu(config: Optional[str] = typer.Option(None, "--config", "-c")):
    """Open the interactive menu (settings, scan, enrich, search...)."""
    cfg_path = config or find_config()
    if not cfg_path or not Path(cfg_path).exists():
        console.print("[red]No photocat.config.json found. Run [bold]photocat init[/] first.")
        raise typer.Exit(1)
    from . import menu as menu_mod
    menu_mod.run(cfg_path)


@app.command()
def enrich(
    config: Optional[str] = typer.Option(None, "--config", "-c"),
    limit: Optional[int] = typer.Option(None, help="Only process the first N photos (testing)."),
    force: bool = typer.Option(False, "--force", help="Re-process every photo (recompute all signals)."),
    redo_ocr: bool = typer.Option(False, "--redo-ocr", help="Only (re)read OCR text on already-enriched photos."),
):
    """Run AI models (CLIP + Florence-2 captions/tags) over un-enriched photos."""
    cfg = _load_cfg(config)
    conn = _open(cfg)
    from . import enrich as enrich_mod
    enrich_mod.enrich(cfg, conn, limit=limit, force=force, redo_ocr=redo_ocr)


@app.command()
def dedup(
    config: Optional[str] = typer.Option(None, "--config", "-c"),
    apply: bool = typer.Option(False, "--apply", help="Actually move duplicates (default: preview)."),
):
    """Find duplicate/near-duplicate photos; keep the best, quarantine the rest."""
    cfg = _load_cfg(config)
    conn = _open(cfg)
    from . import dedup as dedup_mod
    plan = dedup_mod.build_plan(conn, cfg)
    dedup_mod.print_plan(plan)
    if apply and plan:
        if typer.confirm(f"Move {sum(len(p['losers']) for p in plan)} files to "
                         f"{cfg.resolved_duplicates_dir()}?"):
            dedup_mod.apply_plan(conn, cfg, plan)
    elif plan:
        console.print("\n[dim]Preview only. Re-run with --apply to move duplicates.[/]")


@app.command()
def organize(
    config: Optional[str] = typer.Option(None, "--config", "-c"),
    apply: bool = typer.Option(False, "--apply", help="Actually move files (default: preview)."),
):
    """Move photos into year folders (camera date); undated ones go to 'miscellaneous'."""
    cfg = _load_cfg(config)
    conn = _open(cfg)
    from . import organize as organize_mod
    moves, root = organize_mod.build_plan(conn, cfg)
    organize_mod.print_plan(moves, root)
    if apply and moves:
        if typer.confirm(f"Move {len(moves)} file(s) into year folders under {root}?"):
            organize_mod.apply_plan(conn, cfg, moves)
    elif moves:
        console.print("\n[dim]Preview only. Re-run with --apply to move the files.[/]")


@app.command()
def search(
    text: Optional[str] = typer.Argument(None, help="Free-text / semantic query."),
    year: Optional[int] = typer.Option(None),
    year_from: Optional[int] = typer.Option(None, "--from"),
    year_to: Optional[int] = typer.Option(None, "--to"),
    place: Optional[str] = typer.Option(None),
    camera: Optional[str] = typer.Option(None),
    person: Optional[str] = typer.Option(None),
    limit: Optional[int] = typer.Option(None, "--limit", "-n", help="Max results (default from config)."),
    semantic: bool = typer.Option(False, "--semantic", help="Rank by visual concept (CLIP) instead of exact keywords."),
    include_duplicates: bool = typer.Option(False, "--include-duplicates"),
    config: Optional[str] = typer.Option(None, "--config", "-c"),
):
    """Search the catalog. Exact keyword/OCR matches by default; --semantic for concept search."""
    cfg = _load_cfg(config)
    conn = _open(cfg)
    from .search import Query, search as run_search
    q = Query(text=text, year=year, year_from=year_from, year_to=year_to,
              place=place, camera=camera, person=person,
              limit=limit or cfg.search.default_limit, semantic=semantic,
              semantic_fallback=cfg.search.semantic_fallback,
              include_duplicates=include_duplicates)
    hits = run_search(conn, q)
    if text:
        db.record_search(conn, text, semantic, len(hits))
    if not hits:
        console.print("[yellow]No matches.[/] Try fewer/different words, or --semantic.")
        raise typer.Exit()

    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("#", justify="right"); table.add_column("score", justify="right")
    table.add_column("date"); table.add_column("place")
    table.add_column("caption / tags", overflow="fold")
    table.add_column("path", overflow="fold")
    for i, h in enumerate(hits, 1):
        desc = h.caption or h.tags
        table.add_row(str(i), f"{h.score:.3f}", (h.date_taken or "")[:10],
                      h.place, desc, h.path)
    console.print(table)
    kind = hits[0].match or "filter"
    console.print(f"[dim]{len(hits)} result(s) ({kind} match).[/]")
    if kind == "semantic" and not semantic:
        console.print("[dim]No exact keyword match found, so these are ranked by visual "
                      "similarity. Add --semantic to force this, or refine your words.[/]")


@app.command()
def export(
    text: str = typer.Argument(..., help="Query (same as search)."),
    dest: str = typer.Argument(..., help="Destination folder for matched copies."),
    year: Optional[int] = typer.Option(None),
    place: Optional[str] = typer.Option(None),
    limit: int = typer.Option(1000, "--limit", "-n"),
    move: bool = typer.Option(False, "--move", help="Move instead of copy."),
    config: Optional[str] = typer.Option(None, "--config", "-c"),
):
    """Copy (or move) every photo matching a query into a folder."""
    cfg = _load_cfg(config)
    conn = _open(cfg)
    from .search import Query, search as run_search
    hits = run_search(conn, Query(text=text, year=year, place=place, limit=limit))
    out = Path(dest); out.mkdir(parents=True, exist_ok=True)
    n = 0
    for h in hits:
        src = Path(h.path)
        if not src.exists():
            continue
        target = out / src.name
        (shutil.move if move else shutil.copy2)(str(src), str(target))
        n += 1
    console.print(f"[green]{'Moved' if move else 'Copied'} {n} photo(s) to {out}")


@app.command()
def recent(
    config: Optional[str] = typer.Option(None, "--config", "-c"),
    limit: int = typer.Option(15, "--limit", "-n"),
):
    """List recent searches."""
    cfg = _load_cfg(config)
    conn = _open(cfg)
    rows = db.recent_searches(conn, limit=limit)
    if not rows:
        console.print("[yellow]No recent searches yet.")
        raise typer.Exit()
    table = Table("when", "mode", "hits", "query", header_style="bold cyan")
    for r in rows:
        table.add_row((r["ts"] or "")[:16], "concept" if r["semantic"] else "keyword",
                      str(r["n_results"]), r["query"])
    console.print(table)


@app.command()
def stats(config: Optional[str] = typer.Option(None, "--config", "-c")):
    """Show catalog summary."""
    cfg = _load_cfg(config)
    conn = _open(cfg)
    total = db.count(conn)
    dups = db.count(conn, "is_duplicate = 1")
    enriched = db.count(conn, "enriched = 1")
    geo = db.count(conn, "place IS NOT NULL AND place != ''")
    faces_n = conn.execute("SELECT COUNT(*) FROM faces").fetchone()[0]
    people = conn.execute("SELECT COUNT(*) FROM persons").fetchone()[0]
    table = Table(show_header=False)
    table.add_row("Catalog", str(cfg.resolved_catalog_path()))
    table.add_row("Photos (active)", str(total - dups))
    table.add_row("Duplicates quarantined", str(dups))
    table.add_row("AI-enriched", str(enriched))
    table.add_row("Geocoded", str(geo))
    table.add_row("Faces / people", f"{faces_n} / {people}")
    console.print(table)


# ---- faces subcommands -------------------------------------------------------

@faces_app.command("cluster")
def faces_cluster(
    threshold: float = typer.Option(0.5, help="Similarity threshold (higher = stricter)."),
    config: Optional[str] = typer.Option(None, "--config", "-c"),
):
    """Group detected faces into (initially unnamed) people."""
    cfg = _load_cfg(config)
    conn = _open(cfg)
    from . import faces as faces_mod
    n = faces_mod.cluster(conn, threshold)
    console.print(f"[green]Created/updated {n} person cluster(s).[/] "
                  f"Name them with: photocat faces name person_1 \"Real Name\"")


@faces_app.command("name")
def faces_name(
    cluster_name: str = typer.Argument(..., help="Existing person label, e.g. person_1."),
    new_name: str = typer.Argument(..., help="Real name to assign."),
    config: Optional[str] = typer.Option(None, "--config", "-c"),
):
    """Rename a person cluster so you can search --person \"Name\"."""
    cfg = _load_cfg(config)
    conn = _open(cfg)
    from . import faces as faces_mod
    ok = faces_mod.rename_person(conn, cluster_name, new_name)
    console.print(f"[green]Renamed to {new_name}." if ok else f"[red]No person '{cluster_name}'.")


@faces_app.command("list")
def faces_list(config: Optional[str] = typer.Option(None, "--config", "-c")):
    """List people and how many faces each has."""
    cfg = _load_cfg(config)
    conn = _open(cfg)
    rows = conn.execute(
        "SELECT pe.name, COUNT(f.id) AS n FROM persons pe "
        "LEFT JOIN faces f ON f.person_id = pe.id GROUP BY pe.id ORDER BY n DESC"
    ).fetchall()
    table = Table("person", "faces")
    for r in rows:
        table.add_row(r["name"], str(r["n"]))
    console.print(table)


@config_app.command("show")
def config_show(config: Optional[str] = typer.Option(None, "--config", "-c")):
    """Print the current settings as JSON."""
    import json, dataclasses
    cfg = _load_cfg(config)
    data = dataclasses.asdict(cfg)
    data.pop("_config_path", None)
    console.print_json(json.dumps(data))


@config_app.command("enable-all")
def config_enable_all(config: Optional[str] = typer.Option(None, "--config", "-c")):
    """Turn ON every capability (clip, caption, tags, ocr, faces, dedup, geocode)."""
    cfg = _load_cfg(config)
    cfg.set_all_features(True)
    cfg.save()
    console.print("[green]All features enabled and saved.")


@config_app.command("disable-all")
def config_disable_all(config: Optional[str] = typer.Option(None, "--config", "-c")):
    """Turn OFF every capability."""
    cfg = _load_cfg(config)
    cfg.set_all_features(False)
    cfg.save()
    console.print("[green]All features disabled and saved.")


@config_app.command("reset")
def config_reset(
    config: Optional[str] = typer.Option(None, "--config", "-c"),
    keep_library: bool = typer.Option(True, help="Keep catalog path and source folders."),
):
    """Reset all settings to defaults (CLIP+caption+tags+dedup+geocode on; OCR+faces off)."""
    cfg = _load_cfg(config)
    if not typer.confirm("Reset every setting to defaults?"):
        raise typer.Exit()
    cfg.reset_to_defaults(keep_library=keep_library)
    cfg.save()
    console.print(f"[green]Settings reset and saved to {cfg._config_path}")


def main():
    app()


if __name__ == "__main__":
    main()
