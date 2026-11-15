"""Render only the Quarto pages whose sources have changed.

The normal ``quarto render`` command intentionally rebuilds every render
target in a project.  This wrapper keeps the existing ``_site`` directory and
uses source/output timestamps to select incremental render targets instead.

Usage:

    python scripts/render_changed.py
    python scripts/render_changed.py concepts/kangaroo.qmd
    python scripts/render_changed.py --dry-run
    python scripts/render_changed.py --full

Changing an entry also refreshes the home page and its relevant theme and kind
listings. Site-wide configuration, shared metadata, includes and extensions
require a full build, as does a missing output directory or a large batch of
stale pages. CI uses the same selector with the previous ``_site`` restored
from a GitHub Actions cache.
"""

from __future__ import annotations

import argparse
from html import unescape
import os
from pathlib import Path
import re
import shutil
import subprocess


ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "_site"

# These inputs affect the generated HTML or navigation on every page.  If one
# is newer than any rendered page, a partial build could mix old and new site
# chrome, so fall back to a full project render.
GLOBAL_FILES = [
    ROOT / "_quarto.yml",
    ROOT / "_brand.yml",
    ROOT / "_sidebar.yml",
    ROOT / "styles.css",
    ROOT / "_a11y.html",
    ROOT / "_analytics.html",
    ROOT / "_sim-tools.html",
    ROOT / "concepts" / "_metadata.yml",
    ROOT / "scripts" / "post_render.py",
]
GLOBAL_DIRS = [ROOT / "_extensions"]

# These files are included only by the home page.
INDEX_FILES = [
    ROOT / "_group-cards.md",
    ROOT / "_kind-cards.md",
    ROOT / "_hero-chart.md",
]

# Project resources do not require every HTML page to be regenerated.  A
# single incremental render is enough for Quarto to synchronize them into
# _site, so use the home page as that lightweight render target.
RESOURCE_DIRS = [ROOT / "assets", ROOT / "js", ROOT / "sims"]

THEME_PAGES = {
    "Noise and evidence": "noise-and-evidence",
    "Building and checking models": "building-and-checking-models",
    "Causes, samples and populations": "causes-samples-populations",
    "Showing and telling": "showing-and-telling",
    "How science behaves": "how-science-behaves",
    "Thinking about statistics": "thinking-about-statistics",
}
KIND_PAGES = {
    "Method or technique": "methods",
    "Principle or heuristic": "principles",
    "Fallacy": "fallacies",
    "Law or aphorism": "laws-and-aphorisms",
    "Advice": "advice",
}

# Beyond this point a full project render is faster and less error-prone than
# starting Quarto once for each stale page.
MAX_INCREMENTAL_PAGES = 24

# Quarto preserves resource mtimes when copying, but Windows can round the
# destination by a fraction of a millisecond. Treat those tiny differences as
# equal or every run would think the resources changed again.
MTIME_TOLERANCE_NS = 2_000_000


def files_under(paths: list[Path]):
    """Yield files from a mixture of file and directory paths."""
    for path in paths:
        if path.is_file():
            yield path
        elif path.is_dir():
            yield from (p for p in path.rglob("*") if p.is_file())


def render_targets() -> list[Path]:
    """Return project .qmd targets, excluding Quarto partials."""
    targets = []
    for path in ROOT.rglob("*.qmd"):
        rel = path.relative_to(ROOT)
        if any(part.startswith(("_", ".")) for part in rel.parts):
            continue
        targets.append(path)
    return sorted(targets)


def output_for(source: Path) -> Path:
    return OUTPUT / source.relative_to(ROOT).with_suffix(".html")


def is_newer(source: Path, output: Path) -> bool:
    return (
        not output.exists()
        or source.stat().st_mtime_ns
        > output.stat().st_mtime_ns + MTIME_TOLERANCE_NS
    )


def any_newer(inputs, output: Path) -> bool:
    return any(is_newer(path, output) for path in inputs)


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def frontmatter_field(path: Path, name: str) -> str | None:
    text = path.read_text(encoding="utf-8")
    match = re.search(rf'^{re.escape(name)}:\s*"?(.*?)"?\s*$', text, re.M)
    return match.group(1) if match else None


def group_page(directory: str, slug: str) -> Path:
    return ROOT / directory / f"{slug}.qmd"


def add_entry_dependents(targets: set[Path]) -> None:
    """Refresh listings that read metadata from changed entries.

    The rendered entry's categories preserve its previous theme and kind, so
    both the old and current group pages are selected when an entry moves.
    """
    entries = [path for path in targets if path.parent == ROOT / "concepts"]
    if not entries:
        return
    targets.add(ROOT / "index.qmd")

    for entry in entries:
        theme = frontmatter_field(entry, "theme")
        kind = frontmatter_field(entry, "kind")
        if theme in THEME_PAGES:
            targets.add(group_page("themes", THEME_PAGES[theme]))
        else:
            targets.update((ROOT / "themes").glob("*.qmd"))
        if kind in KIND_PAGES:
            targets.add(group_page("kinds", KIND_PAGES[kind]))
        else:
            targets.update((ROOT / "kinds").glob("*.qmd"))

        previous = output_for(entry)
        if not previous.exists():
            continue
        html = previous.read_text(encoding="utf-8")
        categories = {
            unescape(value.strip())
            for value in re.findall(
                r'<div class="quarto-category">([^<]+)</div>', html
            )
        }
        for value in categories:
            if value in THEME_PAGES:
                targets.add(group_page("themes", THEME_PAGES[value]))
            if value in KIND_PAGES:
                targets.add(group_page("kinds", KIND_PAGES[value]))


def resolve_requested(values: list[str]) -> set[Path]:
    targets = set()
    for value in values:
        path = (ROOT / value).resolve() if not Path(value).is_absolute() else Path(value).resolve()
        try:
            path.relative_to(ROOT)
        except ValueError:
            raise SystemExit(f"Render target must be inside {ROOT}: {value}")
        if not path.is_file() or path.suffix.lower() != ".qmd":
            raise SystemExit(f"Render target is not a .qmd file: {value}")
        if any(part.startswith(("_", ".")) for part in path.relative_to(ROOT).parts):
            raise SystemExit(f"Quarto partials are not render targets: {value}")
        targets.add(path)
    return targets


def choose_targets(requested: list[str]) -> tuple[bool, str, set[Path]]:
    all_targets = render_targets()
    outputs = [output_for(path) for path in all_targets]
    existing_outputs = [path for path in outputs if path.exists()]

    if not existing_outputs:
        return True, "_site has no rendered pages", set()

    # A removed source should remove its old HTML too. A full render performs
    # Quarto's normal output cleanup; an incremental render deliberately does
    # not. Restrict the check to directories that contain real render targets
    # so HTML files inside third-party libraries cannot be mistaken for pages.
    expected_outputs = set(outputs)
    page_directories = {path.parent for path in outputs}
    orphaned = [
        path
        for path in OUTPUT.rglob("*.html")
        if path.parent in page_directories and path not in expected_outputs
    ]
    if orphaned:
        return True, f"{len(orphaned)} rendered page(s) no longer have a source", set()

    # The oldest page is the safe baseline: a global input newer than it has
    # not yet been applied consistently across the whole site.
    oldest_output = min(existing_outputs, key=lambda path: path.stat().st_mtime_ns)
    if any_newer(files_under(GLOBAL_FILES + GLOBAL_DIRS), oldest_output):
        return True, "a shared site-wide input changed", set()

    if requested:
        targets = resolve_requested(requested)
    else:
        targets = {source for source in all_targets if is_newer(source, output_for(source))}
        missing = len(outputs) - len(existing_outputs)
        if missing > MAX_INCREMENTAL_PAGES:
            return True, f"{missing} rendered pages are missing", set()
        if len(targets) > MAX_INCREMENTAL_PAGES:
            return True, f"{len(targets)} pages are stale", set()

    index = ROOT / "index.qmd"
    if any_newer(files_under(INDEX_FILES), output_for(index)):
        targets.add(index)

    # Compare each resource with its destination instead of using one global
    # timestamp, so an old untouched asset does not force needless renders.
    resources_changed = False
    for source in files_under(RESOURCE_DIRS):
        destination = OUTPUT / source.relative_to(ROOT)
        if is_newer(source, destination):
            resources_changed = True
            break
    if resources_changed:
        targets.add(index)

    add_entry_dependents(targets)
    if len(targets) > MAX_INCREMENTAL_PAGES:
        return True, f"incremental dependencies expand to {len(targets)} pages", set()
    return False, "", targets


def quarto_command(explicit: str | None) -> str:
    command = explicit or os.environ.get("QUARTO") or shutil.which("quarto")
    if not command:
        raise SystemExit(
            "Quarto was not found. Add it to PATH or pass --quarto with the "
            "path to quarto/quarto.exe."
        )
    return command


def run(command: list[str], dry_run: bool) -> None:
    print("+", subprocess.list2cmdline(command), flush=True)
    if not dry_run:
        subprocess.run(command, cwd=ROOT, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pages", nargs="*", help="specific .qmd pages to render")
    parser.add_argument("--full", action="store_true", help="force a full project render")
    parser.add_argument("--dry-run", action="store_true", help="show what would render")
    parser.add_argument("--quarto", help="path to the Quarto executable")
    args = parser.parse_args()

    if args.full and args.pages:
        parser.error("--full cannot be combined with page paths")

    if args.full:
        full, reason, targets = True, "requested with --full", set()
    else:
        full, reason, targets = choose_targets(args.pages)

    if not full and not targets:
        print("Nothing to render; _site is up to date.", flush=True)
        return

    # A dry run should work on machines where Quarto is not installed.
    quarto = args.quarto or os.environ.get("QUARTO") or shutil.which("quarto")
    if not quarto and args.dry_run:
        quarto = "quarto"
    elif not quarto:
        quarto = quarto_command(args.quarto)

    if full:
        print(f"Full render: {reason}.", flush=True)
        run([quarto, "render"], args.dry_run)
        return

    ordered = sorted(targets, key=relative)
    print(
        f"Incremental render: {len(ordered)} page(s); existing _site is preserved.",
        flush=True,
    )
    for target in ordered:
        run([quarto, "render", relative(target), "--no-clean"], args.dry_run)


if __name__ == "__main__":
    main()
