#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Stage and verify the exact Chipped release payload set."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys


VERSION_PATTERN = re.compile(r"[0-9A-Za-z][0-9A-Za-z.+-]*")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _payloads(root: Path, version: str) -> tuple[tuple[str, Path, str], ...]:
    return (
        (
            "production_jar",
            root / "build/libs" / f"bluemap-chipped-addon-{version}.jar",
            f"bluemap-chipped-addon-{version}.jar",
        ),
        (
            "sources_jar",
            root / "build/libs" / f"bluemap-chipped-addon-{version}-sources.jar",
            f"bluemap-chipped-addon-{version}-sources.jar",
        ),
        (
            "pom",
            root / "build/publications/addon/pom-default.xml",
            f"bluemap-chipped-addon-{version}.pom",
        ),
        (
            "gradle_module",
            root / "build/publications/addon/module.json",
            f"bluemap-chipped-addon-{version}.module.json",
        ),
    )


def stage(root: Path, output: Path, version: str) -> dict[str, Path]:
    if VERSION_PATTERN.fullmatch(version) is None:
        raise ValueError(f"invalid release version: {version}")
    if output.is_symlink():
        raise ValueError(f"release output must not be a symlink: {output}")
    if output.exists() and (not output.is_dir() or any(output.iterdir())):
        raise ValueError(f"release output is not an empty directory: {output}")
    output.mkdir(parents=True, exist_ok=True)

    staged: dict[str, Path] = {}
    for key, source, file_name in _payloads(root, version):
        if not source.is_file() or source.is_symlink():
            raise ValueError(f"release input is missing or unsafe: {source}")
        target = output / file_name
        shutil.copyfile(source, target)
        staged[key] = target

    checksum_path = output / "SHA256SUMS"
    checksum_lines = [
        f"{_sha256(path)}  ./{path.name}\n"
        for path in sorted(staged.values(), key=lambda item: item.name)
    ]
    checksum_path.write_text("".join(checksum_lines), encoding="ascii", newline="\n")
    staged["sha256sums"] = checksum_path
    return staged


def verify_provenance(provenance: Path, version: str, staged: dict[str, Path]) -> None:
    release = json.loads(provenance.read_text(encoding="utf-8"))
    if release.get("version") != version or release.get("tag") != f"v{version}":
        raise ValueError("release provenance version or tag differs from the staged version")
    expected = release.get("final_release_artifacts")
    if not isinstance(expected, dict) or set(expected) != set(staged):
        raise ValueError("release provenance payload roster differs from the staged bundle")

    for key, path in staged.items():
        record = expected[key]
        actual = {
            "file_name": path.name,
            "size": path.stat().st_size,
            "sha256": _sha256(path),
        }
        if record != actual:
            raise ValueError(
                f"release provenance differs for {key}: expected {record}, staged {actual}"
            )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", required=True)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--verify-provenance", type=Path)
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    output = args.output if args.output.is_absolute() else root / args.output
    provenance = args.verify_provenance
    if provenance is not None and not provenance.is_absolute():
        provenance = root / provenance

    try:
        staged = stage(root, output, args.version)
        if provenance is not None:
            verify_provenance(provenance, args.version, staged)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"release staging failed: {error}", file=sys.stderr)
        return 1

    action = "Staged and verified" if provenance is not None else "Staged"
    print(f"{action} {len(staged)} release payloads in {output}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
