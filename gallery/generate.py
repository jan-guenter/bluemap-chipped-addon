#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Generate the bounded exhaustive Chipped/Athena staging gallery."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import sys
from typing import Iterable


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parent
DEFINITIONS = (
    REPOSITORY
    / "src/main/resources/bluemap-chipped/profiles/chipped/"
    / "4.0.2-athena-4.0.6/definitions.tsv"
)
SWATCH_ORIGIN = (-86, 100, -86)
SWATCH_COLUMNS = 39
STRUCTURAL_ORIGIN = (8, 100, -80)
STRUCTURAL_COLUMNS = 10


@dataclass(frozen=True, order=True)
class Position:
    x: int
    y: int
    z: int

    def offset(self, dx: int = 0, dy: int = 0, dz: int = 0) -> "Position":
        return Position(self.x + dx, self.y + dy, self.z + dz)

    def command(self) -> str:
        return f"{self.x} {self.y} {self.z}"


@dataclass(frozen=True)
class Placement:
    position: Position
    block: str
    routed: bool = True


@dataclass(frozen=True)
class Fixture:
    case_id: str
    family: str
    anchor: Position
    placements: tuple[Placement, ...]
    notes: str


def definitions() -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    for line in DEFINITIONS.read_text(encoding="ascii").splitlines():
        fields = line.split("\t")
        if len(fields) < 2:
            raise ValueError("malformed definitions catalog")
        rows.append((fields[0], fields[1]))
    if len(rows) != 1427 or len({block for block, _family in rows}) != 1427:
        raise ValueError("exact routed definition census changed")
    return rows


def swatches(rows: Iterable[tuple[str, str]]) -> list[Placement]:
    x0, y, z0 = SWATCH_ORIGIN
    result: list[Placement] = []
    for index, (block, _family) in enumerate(rows):
        x = x0 + 2 * (index % SWATCH_COLUMNS)
        z = z0 + 2 * (index // SWATCH_COLUMNS)
        result.append(Placement(Position(x, y, z), block))
    return result


def structural_fixtures() -> list[Fixture]:
    result: list[Fixture] = []
    slot = 0

    def cell() -> Position:
        nonlocal slot
        x0, y, z0 = STRUCTURAL_ORIGIN
        position = Position(
            x0 + 8 * (slot % STRUCTURAL_COLUMNS),
            y,
            z0 + 12 * (slot // STRUCTURAL_COLUMNS),
        )
        slot += 1
        return position

    def add(
        case_id: str,
        family: str,
        block: str,
        offsets: Iterable[tuple[int, int, int]],
        notes: str,
        *,
        center: Position | None = None,
        support: Iterable[tuple[int, int, int, str]] = (),
    ) -> None:
        reserved = cell()
        anchor = center if center is not None else reserved
        placements = [
            Placement(anchor.offset(dx, dy, dz), block)
            for dx, dy, dz in offsets
        ]
        placements.extend(
            Placement(anchor.offset(dx, dy, dz), support_block, False)
            for dx, dy, dz, support_block in support
        )
        result.append(Fixture(case_id, family, anchor, tuple(placements), notes))

    ctm_patterns = {
        "isolated": ((0, 0, 0),),
        "up": ((0, 0, 0), (0, 0, -1)),
        "right": ((0, 0, 0), (1, 0, 0)),
        "corner-open": ((0, 0, 0), (0, 0, -1), (1, 0, 0)),
        "corner-closed": (
            (0, 0, 0), (0, 0, -1), (1, 0, 0), (1, 0, -1)
        ),
        "all-eight": tuple(
            (dx, 0, dz) for dz in (-1, 0, 1) for dx in (-1, 0, 1)
        ),
        "direct-face": ((0, 0, 0), (0, 1, 0)),
    }
    materials = {
        "opaque": "chipped:acacia_planks_panel",
        "transparent": "chipped:clear_leaded_glass",
        "wool": "chipped:cornered_black_wool",
    }
    for material, block in materials.items():
        for pattern, offsets in ctm_patterns.items():
            add(
                f"ctm-{material}-{pattern}",
                "ctm",
                block,
                offsets,
                f"{material} CTM {pattern} truth-class witness",
            )

    face_patterns = {
        "north": ((0, 0, 0), (0, 1, 0), (1, 0, 0), (1, 1, 0)),
        "south": ((0, 0, 0), (0, 1, 0), (-1, 0, 0), (-1, 1, 0)),
        "west": ((0, 0, 0), (0, 1, 0), (0, 0, -1), (0, 1, -1)),
        "east": ((0, 0, 0), (0, 1, 0), (0, 0, 1), (0, 1, 1)),
    }
    for face, offsets in face_patterns.items():
        add(
            f"ctm-face-basis-{face}",
            "ctm",
            "chipped:black_concrete_panel",
            offsets,
            f"vertical {face} face-local up/left/diagonal basis",
        )

    axis_steps = {"x": (1, 0, 0), "y": (0, 1, 0), "z": (0, 0, 1)}
    for axis, step in axis_steps.items():
        block = f"chipped:black_concrete_pillar[axis={axis}]"
        dx, dy, dz = step
        add(f"pillar-{axis}-singleton", "pillar", block, ((0, 0, 0),),
            f"axis {axis} cap and self texture")
        add(f"pillar-{axis}-end", "pillar", block,
            ((0, 0, 0), (dx, dy, dz)), f"axis {axis} top/bottom endpoints")
        middle_offsets = (
            ((0, 0, 0), (0, 1, 0), (0, 2, 0))
            if axis == "y"
            else ((-dx, -dy, -dz), (0, 0, 0), (dx, dy, dz))
        )
        add(f"pillar-{axis}-middle", "pillar", block,
            middle_offsets,
            f"axis {axis} center chain texture")
        add(f"pillar-ice-{axis}", "pillar", f"chipped:curly_ice_pillar[axis={axis}]",
            ((0, 0, 0),), f"transparent axis {axis} alpha and UV witness")

    giant_cases = (
        ("giant-opaque-negative-y", "chipped:massive_blackstone_bricks",
         Position(-8, 100, -8), ((0, 0, 0), (1, 0, 0), (0, 0, 1), (1, 0, 1))),
        ("giant-ice-negative-x", "chipped:massive_ice_bricks",
         Position(-4, 100, -8), ((0, 0, 0), (0, 1, 0), (0, 0, 1), (0, 1, 1))),
        ("giant-opaque-positive-z", "chipped:massive_blackstone_bricks",
         Position(0, 100, 12), ((0, 0, 0), (1, 0, 0), (0, 1, 0), (1, 1, 0))),
        ("giant-ice-positive-y", "chipped:massive_ice_bricks",
         Position(4, 100, 12), ((0, 0, 0), (1, 0, 0), (0, 0, 1), (1, 0, 1))),
        ("giant-phase-shift-x", "chipped:massive_blackstone_bricks",
         Position(0, 100, 8), ((0, 0, 0), (0, 1, 0), (0, 0, 1), (0, 1, 1))),
    )
    for case_id, block, center, offsets in giant_cases:
        add(
            case_id,
            "giant",
            block,
            offsets,
            "2x2 X/Y/Z-face coordinate-phase and transparency witness",
            center=center,
        )

    carpet = "chipped:cornered_black_carpet"
    carpet_cases = {
        "isolated": ((0, 0, 0),),
        "line-end": ((0, 0, 0), (0, 0, 1)),
        "line-middle": ((0, 0, -1), (0, 0, 0), (0, 0, 1)),
        "corner": ((0, 0, 0), (0, 0, -1), (1, 0, 0)),
        "tee": ((0, 0, 0), (-1, 0, 0), (1, 0, 0), (0, 0, -1)),
        "solid": tuple((dx, 0, dz) for dz in (-1, 0, 1) for dx in (-1, 0, 1)),
    }
    for name, offsets in carpet_cases.items():
        add(f"carpet-{name}", "carpet_ctm", carpet, offsets,
            f"one-sixteenth carpet {name} seam witness")
    add(
        "carpet-opaque-neighbor",
        "carpet_ctm",
        carpet,
        ((0, 0, 0), (0, 0, 1)),
        "adjacent carpets beside an opaque full-cube culling witness",
        support=((1, 0, 0, "minecraft:stone"),),
    )

    pane_shapes = {
        "isolated": ((0, 0, 0),),
        "north-south": ((0, 0, -1), (0, 0, 0), (0, 0, 1)),
        "east-west": ((-1, 0, 0), (0, 0, 0), (1, 0, 0)),
        "corner": ((0, 0, 0), (0, 0, -1), (1, 0, 0)),
        "tee": ((0, 0, 0), (-1, 0, 0), (1, 0, 0), (0, 0, -1)),
        "cross": (
            (0, 0, 0), (-1, 0, 0), (1, 0, 0), (0, 0, -1), (0, 0, 1)
        ),
        "vertical-exact": ((0, 0, 0), (0, 1, 0)),
        "vertical-different": (
            (0, 0, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1),
            (-1, 1, 0), (1, 1, 0)
        ),
    }
    pane_engines = {
        "pane-ctm": ("pane_ctm", "chipped:clear_leaded_glass_pane"),
        "pane-pillar": (
            "pane_pillar", "chipped:arched_black_stained_glass_pane_pillar"
        ),
    }
    for engine, (family, block) in pane_engines.items():
        for shape, offsets in pane_shapes.items():
            add(f"{engine}-{shape}", family, block, offsets,
                f"centered one-eighth pane {shape} witness")

    limited = "chipped:arched_black_stained_glass_pillar"
    add("limited-singleton", "limited_pillar", limited, ((0, 0, 0),),
        "transparent fixed-Y singleton")
    add("limited-end", "limited_pillar", limited, ((0, 0, 0), (0, 1, 0)),
        "transparent fixed-Y endpoint pair")
    add("limited-middle", "limited_pillar", limited,
        ((0, 0, 0), (0, 1, 0), (0, 2, 0)), "transparent fixed-Y center chain")
    add("limited-direct-east", "limited_pillar", limited,
        ((0, 0, 0), (1, 0, 0)), "same-block direct east face suppression")
    add("limited-direct-north", "limited_pillar", limited,
        ((0, 0, 0), (0, 0, -1)), "same-block direct north face suppression")

    if len(result) != 70:
        raise AssertionError(f"gallery has {len(result)} structural cases, expected 70")
    occupied: dict[Position, str] = {}
    for fixture in result:
        for placement in fixture.placements:
            previous = occupied.setdefault(placement.position, placement.block)
            if previous != placement.block:
                raise AssertionError(f"conflicting fixture placement at {placement.position}")
    return result


def swatches_tsv(rows: list[tuple[str, str]], blocks: list[Placement]) -> str:
    lines = ["index\tblock_id\tloader_family\tx\ty\tz"]
    for index, ((block_id, family), placement) in enumerate(zip(rows, blocks, strict=True)):
        lines.append(
            f"{index}\t{block_id}\t{family}\t{placement.position.x}\t"
            f"{placement.position.y}\t{placement.position.z}"
        )
    return "\n".join(lines) + "\n"


def cases_tsv(fixtures: list[Fixture]) -> str:
    lines = ["case_id\tfamily\tx\ty\tz\tplacements\tnotes"]
    for fixture in fixtures:
        lines.append(
            f"{fixture.case_id}\t{fixture.family}\t{fixture.anchor.x}\t"
            f"{fixture.anchor.y}\t{fixture.anchor.z}\t"
            f"{len(fixture.placements)}\t{fixture.notes}"
        )
    return "\n".join(lines) + "\n"


def clear_function() -> str:
    lines = ["# Generated by gallery/generate.py; do not edit."]
    for x0 in range(-90, 90, 30):
        lines.append(f"fill {x0} 99 -90 {x0 + 29} 106 16 minecraft:air")
    return "\n".join(lines) + "\n"


def build_function(swatches_: list[Placement], fixtures: list[Fixture]) -> str:
    lines = [
        "# Generated by gallery/generate.py; do not edit.",
        "function chipped_gallery:clear",
        "fill -90 99 -90 89 99 16 minecraft:stone",
        "scoreboard players set #swatches chipped_gallery 0",
        "scoreboard players set #structures chipped_gallery 0",
    ]
    for placement in swatches_:
        lines.append(f"setblock {placement.position.command()} {placement.block}")
        lines.append("scoreboard players add #swatches chipped_gallery 1")
    for fixture in fixtures:
        for placement in fixture.placements:
            lines.append(f"setblock {placement.position.command()} {placement.block}")
        lines.append("scoreboard players add #structures chipped_gallery 1")
    lines.extend((
        "function chipped_gallery:verify",
        "tellraw @a [{\"text\":\"Chipped gallery: \"},{\"score\":{\"name\":\"#swatches\",\"objective\":\"chipped_gallery\"}},{\"text\":\" exact IDs, \"},{\"score\":{\"name\":\"#structures\",\"objective\":\"chipped_gallery\"}},{\"text\":\" structural cases, \"},{\"score\":{\"name\":\"#failures\",\"objective\":\"chipped_gallery\"}},{\"text\":\" failures\"}]",
    ))
    return "\n".join(lines) + "\n"


def verify_function(swatches_: list[Placement], fixtures: list[Fixture]) -> str:
    lines = [
        "# Generated by gallery/generate.py; do not edit.",
        "scoreboard players set #failures chipped_gallery 0",
        "scoreboard players set #checked chipped_gallery 0",
    ]
    for placement in swatches_:
        lines.append(
            f"execute unless block {placement.position.command()} {placement.block} run "
            "scoreboard players add #failures chipped_gallery 1"
        )
        lines.append("scoreboard players add #checked chipped_gallery 1")
    for fixture in fixtures:
        for placement in fixture.placements:
            lines.append(
                f"execute unless block {placement.position.command()} {placement.block} run "
                "scoreboard players add #failures chipped_gallery 1"
            )
            lines.append("scoreboard players add #checked chipped_gallery 1")
    expected = len(swatches_) + sum(len(fixture.placements) for fixture in fixtures)
    lines.extend((
        f"execute unless score #checked chipped_gallery matches {expected} run scoreboard players add #failures chipped_gallery 1",
        "execute unless score #swatches chipped_gallery matches 1427 run scoreboard players add #failures chipped_gallery 1",
        "execute unless score #structures chipped_gallery matches 70 run scoreboard players add #failures chipped_gallery 1",
    ))
    return "\n".join(lines) + "\n"


def rendered_files() -> dict[Path, bytes]:
    rows = definitions()
    swatch_blocks = swatches(rows)
    fixtures = structural_fixtures()
    placement_count = len(swatch_blocks) + sum(len(case.placements) for case in fixtures)
    files: dict[Path, bytes] = {
        Path("swatches.tsv"): swatches_tsv(rows, swatch_blocks).encode("utf-8"),
        Path("cases.tsv"): cases_tsv(fixtures).encode("utf-8"),
        Path("cases.json"): (json.dumps({
            "schema_version": 1,
            "baseline": {
                "pack": "All the Mons 1.2.0",
                "minecraft": "1.21.1",
                "chipped": "4.0.2",
                "athena": "4.0.6",
            },
            "routed_swatch_count": len(swatch_blocks),
            "structural_case_count": len(fixtures),
            "verified_placement_count": placement_count,
            "structural_cases": [
                {
                    "case_id": case.case_id,
                    "family": case.family,
                    "anchor": {"x": case.anchor.x, "y": case.anchor.y, "z": case.anchor.z},
                    "notes": case.notes,
                    "placements": [
                        {
                            "x": item.position.x, "y": item.position.y,
                            "z": item.position.z, "block": item.block,
                            "expected_route": "custom" if item.routed else "stock-control",
                        }
                        for item in case.placements
                    ],
                }
                for case in fixtures
            ],
        }, indent=2, sort_keys=True) + "\n").encode("utf-8"),
        Path("datapack/pack.mcmeta"): (json.dumps({
            "pack": {
                "description": "ATM 1.2.0 Chipped/Athena BlueMap review gallery",
                "pack_format": 48,
            }
        }, indent=2) + "\n").encode("utf-8"),
        Path("datapack/data/minecraft/tags/function/load.json"): (
            json.dumps({"values": ["chipped_gallery:load"]}, indent=2) + "\n"
        ).encode("utf-8"),
        Path("datapack/data/chipped_gallery/function/load.mcfunction"): (
            "# Generated by gallery/generate.py; do not edit.\n"
            "scoreboard objectives add chipped_gallery dummy\n"
            "forceload add -96 -96 96 31\n"
        ).encode("utf-8"),
        Path("datapack/data/chipped_gallery/function/build.mcfunction"):
            build_function(swatch_blocks, fixtures).encode("utf-8"),
        Path("datapack/data/chipped_gallery/function/verify.mcfunction"):
            verify_function(swatch_blocks, fixtures).encode("utf-8"),
        Path("datapack/data/chipped_gallery/function/clear.mcfunction"):
            clear_function().encode("utf-8"),
        Path("datapack/data/chipped_gallery/function/pose.mcfunction"): (
            "# Generated by gallery/generate.py; do not edit.\n"
            "tp @s 0.5 132 28.5 180 34\n"
        ).encode("utf-8"),
        Path("datapack/data/chipped_gallery/function/release.mcfunction"): (
            "# Generated by gallery/generate.py; do not edit.\n"
            "forceload remove -96 -96 96 31\n"
        ).encode("utf-8"),
    }
    checksums = [
        f"{hashlib.sha256(content).hexdigest()}  {path.as_posix()}"
        for path, content in sorted(files.items(), key=lambda item: item[0].as_posix())
    ]
    files[Path("SHA256SUMS")] = ("\n".join(checksums) + "\n").encode("ascii")
    return files


def write_or_check(files: dict[Path, bytes], check: bool) -> int:
    differences: list[str] = []
    for relative, expected in files.items():
        path = ROOT / relative
        if check:
            if not path.is_file() or path.read_bytes() != expected:
                differences.append(relative.as_posix())
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(expected)
    if differences:
        print("generated gallery files differ:", file=sys.stderr)
        for path in differences:
            print(f"  {path}", file=sys.stderr)
        return 1
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    return write_or_check(rendered_files(), args.check)


if __name__ == "__main__":
    raise SystemExit(main())
