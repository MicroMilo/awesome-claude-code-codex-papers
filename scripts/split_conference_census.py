#!/usr/bin/env python3
"""Migrate a legacy monolithic census to the per-conference layout."""

from __future__ import annotations

import argparse
from pathlib import Path

if __package__:
    from .census_store import CENSUS_DIR, LEGACY_CENSUS_PATH, load_census, write_census
else:  # pragma: no cover - documented direct-script entry point
    from census_store import CENSUS_DIR, LEGACY_CENSUS_PATH, load_census, write_census


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=LEGACY_CENSUS_PATH)
    parser.add_argument("--output-dir", type=Path, default=CENSUS_DIR)
    args = parser.parse_args()
    existing_index = args.output_dir / "index.yaml"
    if not args.input.exists() and existing_index.exists():
        print(f"Census is already split: {existing_index}")
        return 0
    census = load_census(args.input)
    index_path = write_census(census, args.output_dir)
    print(
        f"Wrote {len(census.get('conferences', []))} conference files and {index_path}. "
        "The input file is intentionally left untouched."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
