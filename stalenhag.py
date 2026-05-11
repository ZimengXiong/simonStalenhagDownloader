#!/usr/bin/env python3
"""Pure downloader for Simon Stålenhag wallpapers."""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path
from urllib import request

BASE = "http://www.simonstalenhag.se/"

# Where wallpapers are saved
IMAGES_DIR = Path.home() / "Pictures" / "Stålenhag"

# The pages to scrape — each maps to a collection on the site
PAGES: dict[str, str] = {
    "steel_meadow": BASE,
    "paleoart": f"{BASE}paleo.html",
    "commissions": f"{BASE}other.html",
    "tales_from_the_loop": f"{BASE}tftl.html",
    "things_from_the_flood": f"{BASE}tftf.html",
    "the_electric_state": f"{BASE}es.html",
    "labyrinth": f"{BASE}labyrinth.html",
}


def ensure_dir() -> None:
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)


def get_all_image_names() -> list[str]:
    """Scrape all pages and return a de-duplicated list of image paths
    (relative to BASE, e.g. 'bilderbig/foo.jpg')."""
    images: set[str] = set()
    pattern = re.compile(r"(?:bilder|paleo|other|tftl|tftf)big/[a-zA-Z0-9_]*\.jpg")
    for url in PAGES.values():
        try:
            contents = request.urlopen(url, timeout=30).read()
            images.update(pattern.findall(str(contents)))
        except Exception as exc:
            print(f"Warning: failed to fetch {url}: {exc}", file=sys.stderr)
    return sorted(images)


def download_all() -> None:
    """Download every wallpaper that isn't already saved locally."""
    ensure_dir()
    names = get_all_image_names()
    print(f"Found {len(names)} images total")

    already = {f.name for f in IMAGES_DIR.iterdir() if f.suffix == ".jpg"}
    # The local filename replaces '/' with '-'
    local_names = {n.replace("/", "-") for n in names}
    existing = already & local_names
    missing = sorted(local_names - already)

    print(f"Already downloaded: {len(existing)}")
    print(f"To download:        {len(missing)}")

    for idx, local_name in enumerate(missing, 1):
        # Reconstruct the original relative path
        orig_name = local_name.replace("-", "/", 1)  # only first slash
        url = BASE + orig_name
        dest = IMAGES_DIR / local_name
        print(f"  [{idx}/{len(missing)}] {orig_name} ... ", end="", flush=True)
        try:
            request.urlretrieve(url, dest)
            print("OK")
        except Exception as exc:
            print(f"FAILED: {exc}")

    print(f"\nDone — {len(IMAGES_DIR)} wallpapers saved to {IMAGES_DIR}")


def list_images() -> None:
    """Print all available image names."""
    names = get_all_image_names()
    print(f"Available images ({len(names)}):")
    for n in names:
        print(f"  {n}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download Simon Stålenhag wallpapers.",
        prog="stalenhag",
    )
    parser.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="Download all wallpapers to ~/Pictures/Stålenhag/",
    )
    parser.add_argument(
        "-l",
        "--list",
        action="store_true",
        help="List all available wallpapers",
    )

    args = parser.parse_args()

    if args.list:
        list_images()
    elif args.all:
        download_all()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
