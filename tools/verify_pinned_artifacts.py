#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Fail-closed review gate for the exact Chipped 4.0.2/Athena 4.0.6 tuple."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys
import zipfile

import generate_profile


def _verify_mod_metadata(chipped: Path, athena: Path) -> None:
    with zipfile.ZipFile(chipped) as archive:
        try:
            metadata = archive.read("META-INF/neoforge.mods.toml")
        except KeyError as error:
            raise ValueError("missing Chipped NeoForge metadata") from error
        if b'"chipped"' not in metadata or b'"4.0.2"' not in metadata:
            raise ValueError("Chipped NeoForge metadata identity changed")
        names = archive.namelist()
        if not any(name.startswith("assets/chipped/") for name in names):
            raise ValueError("Chipped archive has no installed resource root")
        if any(name.startswith("earth/terrarium/athena/") for name in names):
            raise ValueError("Chipped archive unexpectedly embeds Athena classes")

    with zipfile.ZipFile(athena) as archive:
        names = archive.namelist()
        if "META-INF/neoforge.mods.toml" not in names:
            raise ValueError("Athena archive has no NeoForge metadata")
        metadata = archive.read("META-INF/neoforge.mods.toml")
        if b'"athena"' not in metadata or b'"4.0.6"' not in metadata:
            raise ValueError("Athena NeoForge metadata identity changed")
        if not any(name.startswith("earth/terrarium/athena/") for name in names):
            raise ValueError("Athena archive has no expected implementation package")


def verify(chipped: Path, athena: Path) -> None:
    outputs = generate_profile.build_outputs(chipped, athena)
    generate_profile.apply_outputs(outputs, check=True)
    _verify_mod_metadata(chipped, athena)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--chipped", required=True, type=Path)
    parser.add_argument("--athena", required=True, type=Path)
    args = parser.parse_args()
    try:
        verify(args.chipped, args.athena)
    except (OSError, ValueError, zipfile.BadZipFile) as error:
        print(f"artifact verification failed: {error}", file=sys.stderr)
        return 1
    print(
        "Verified exact Chipped 4.0.2 + Athena 4.0.6 artifacts, "
        "1,427 routed definitions, and the metadata-only resource closure."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
