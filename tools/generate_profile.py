#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Generate the metadata-only exact Chipped/Athena rendering profile."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path, PurePosixPath
from typing import Any, Iterable
import zipfile


PROFILE_ROOT = Path("src/main/resources/bluemap-chipped/profiles")
PROFILE_DIRECTORY = PROFILE_ROOT / "chipped/4.0.2-athena-4.0.6"
CATALOG_PATH = PROFILE_ROOT / "exact-artifacts.json"
PROFILE_PATH = PROFILE_DIRECTORY / "profile.json"
DEFINITIONS_PATH = PROFILE_DIRECTORY / "definitions.tsv"
RESOURCES_PATH = PROFILE_DIRECTORY / "required-resources.tsv"

CHIPPED_FILENAME = "chipped-neoforge-1.21.1-4.0.2.jar"
CHIPPED_SIZE = 15_020_578
CHIPPED_SHA1 = "6f5395f58139802edfde7cb9170279f92f291971"
CHIPPED_SHA256 = "18ac6fd6b30db4922ccc6ee8bea5b113f69587505b7529834f37ace506427291"
CHIPPED_SHA512 = (
    "f3083b01267e7c674c4b42f45a317c93ee7723443cba2051fe5bc593638b533b0"
    "fe90699e2101661c934dff458eab693cce4e188533bfe977778c249563a2fa5"
)
ATHENA_FILENAME = "athena-neoforge-1.21.1-4.0.6.jar"
ATHENA_SIZE = 99_944
ATHENA_SHA1 = "4bcbdf388bd5e387beca7c627224aac33584b55b"
ATHENA_SHA256 = "43699885bbce3343916d4c5c4940cf0e3f9f6f02fdeb46e8655e121b42282ec5"
ATHENA_SHA512 = (
    "ab40a306a26ce834daae921a1e87768cd2538a4bfe27a4480f97af854084cc334"
    "e7416b1bd0b7583834a32a86951283f29fd4b1df7b98a967a6b26a3ec05e2cf"
)

ALL_BLOCKSTATES_COUNT = 6_981
ALL_BLOCKSTATES_DIGEST = (
    "255977e9e98c63fb335a771447a6ca31b5db7c9bc9d0894b5697c1e8716e08af"
)
ROSTER_COUNT = 1_427
ROSTER_DIGEST = "2d8f6d737e41759a759bddac09a9432c80ec47f6b37bcef92cb916ef336b7cf8"
MODEL_COUNT = 1_427
MODEL_DIGEST = "813f809f10f29f455f4660709446397d2ec73547acd791bc332f8effb23c5343"
TEXTURE_COUNT = 5_947
TEXTURE_DIGEST = "367515de4eaf4257ec95c8a377a74137935516cee27cb2604895eac4081dd86d"

LOADERS: dict[str, tuple[int, str, tuple[str, ...], str]] = {
    "athena:ctm": (
        896,
        "d1ed376d8970e8812e800898ed02e76adf121fa1b3f62ff450a21ea31901c125",
        ("particle", "empty", "center", "vertical", "horizontal"),
        "minecraft:block/cube_all",
    ),
    "athena:pillar": (
        248,
        "bebdc24614bb98ee3e2ae833edb909cd15e15311e791ab3d0befa0870162d9e7",
        ("particle", "self", "top", "center", "bottom"),
        "minecraft:block/cube_column",
    ),
    "athena:giant": (
        108,
        "5c50e6b6f590a47a1c7c5b1dd650481b7ac612708be706a106c0043fd41e7f4f",
        ("particle", "1", "2", "3", "4"),
        "minecraft:block/cube_all",
    ),
    "athena:pane_ctm": (
        93,
        "2969bcadf207a2acba4d22c89bf7f1cc869ac9564799f3ba2783446f1e055579",
        ("particle", "empty", "center", "vertical", "horizontal"),
        "minecraft:block/cube_all",
    ),
    "athena:carpet_ctm": (
        48,
        "73f730346b243f89359ab8225a6e36c2318de071e738353d40c49e2b19089360",
        ("particle", "empty", "center", "vertical", "horizontal"),
        "minecraft:block/carpet",
    ),
    "athena:limited_pillar": (
        17,
        "857c4f3abd6951d2d6294ad50004217c8eafc9038fe1320d25cfea3770608c4f",
        ("particle", "self", "top", "center", "bottom"),
        "minecraft:block/cube_all",
    ),
    "athena:pane_pillar": (
        17,
        "cface31b4f9225460f16ddb7238119897f6324183f3c5dd14c204f31f4b0a732",
        ("particle", "self", "top", "center", "bottom"),
        "minecraft:block/cube_all",
    ),
}
def digest_bytes(raw: bytes, algorithm: str = "sha256") -> str:
    return hashlib.new(algorithm, raw).hexdigest()


def digest_path(path: Path, algorithm: str) -> str:
    value = hashlib.new(algorithm)
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(64 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def roster_digest(values: Iterable[str]) -> str:
    payload = "".join(f"{value}\n" for value in sorted(values)).encode("utf-8")
    return digest_bytes(payload)


def canonical_json(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=True, sort_keys=True, separators=(",", ":")
    ).encode("ascii")


def resource_path(key: str, kind: str, suffix: str) -> str:
    if ":" in key:
        namespace, value = key.split(":", 1)
    else:
        namespace, value = "minecraft", key
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        raise ValueError(f"unsafe resource key: {key}")
    return f"assets/{namespace}/{kind}/{value}{suffix}"


def verify_file_identity(
    path: Path, *, filename: str, size: int, sha1: str, sha256: str, sha512: str
) -> None:
    if not path.is_file() or path.name != filename:
        raise ValueError(f"unexpected artifact path: {path}")
    if path.stat().st_size != size:
        raise ValueError(f"unexpected artifact size for {path}")
    for algorithm, expected in (
        ("sha1", sha1),
        ("sha256", sha256),
        ("sha512", sha512),
    ):
        actual = digest_path(path, algorithm)
        if actual != expected:
            raise ValueError(
                f"{path.name} {algorithm} changed: got {actual}, expected {expected}"
            )


def _model_texture_digest(model: dict[str, Any]) -> str:
    textures = model.get("textures")
    if not isinstance(textures, dict) or not textures:
        raise ValueError("ordinary model has no texture map")
    rows: list[str] = []
    for key, value in sorted(textures.items()):
        if not isinstance(key, str) or not isinstance(value, str):
            raise ValueError("ordinary model texture map is malformed")
        rows.append(f"{key}={value}\n")
    return digest_bytes("".join(rows).encode("utf-8"))


def _parse_definition(
    archive: zipfile.ZipFile, path: str, raw: bytes
) -> tuple[tuple[str, ...], str, tuple[str, ...]] | None:
    value = json.loads(raw)
    if not isinstance(value, dict) or "athena:loader" not in value:
        return None
    loader = value.get("athena:loader")
    if loader not in LOADERS:
        raise ValueError(f"{path} has unsupported Athena loader {loader!r}")
    expected_count, _digest, roles, parent = LOADERS[loader]
    del expected_count

    expected_keys = {"athena:loader", "ctm_textures", "variants"}
    if loader == "athena:giant":
        expected_keys.update(("width", "height"))
        if value.get("width") != 2 or value.get("height") != 2:
            raise ValueError(f"{path} giant dimensions changed")
    if set(value) != expected_keys:
        raise ValueError(f"{path} blockstate schema changed")

    variants = value.get("variants")
    if not isinstance(variants, dict) or set(variants) != {""}:
        raise ValueError(f"{path} variants changed")
    variant = variants[""]
    if not isinstance(variant, dict) or set(variant) != {"model"}:
        raise ValueError(f"{path} default variant changed")
    model_key = variant.get("model")
    if not isinstance(model_key, str):
        raise ValueError(f"{path} model key is malformed")

    textures = value.get("ctm_textures")
    if not isinstance(textures, dict) or set(textures) != set(roles):
        raise ValueError(f"{path} Athena texture schema changed")
    texture_values = tuple(textures[role] for role in roles)
    if any(not isinstance(texture, str) for texture in texture_values):
        raise ValueError(f"{path} Athena texture key is malformed")

    model_path = resource_path(model_key, "models", ".json")
    try:
        model = json.loads(archive.read(model_path))
    except KeyError as error:
        raise ValueError(f"missing ordinary model {model_path}") from error
    if not isinstance(model, dict) or set(model) != {"parent", "textures"}:
        raise ValueError(f"{model_path} ordinary model schema changed")
    if model.get("parent") != parent:
        raise ValueError(f"{model_path} parent changed")

    block = path.removeprefix("assets/chipped/blockstates/").removesuffix(".json")
    row = (
        f"chipped:{block}",
        loader.removeprefix("athena:"),
        model_key,
        parent,
        *texture_values,
        _model_texture_digest(model),
    )
    return row, model_path, texture_values


def build_outputs(chipped: Path, athena: Path) -> dict[Path, bytes]:
    verify_file_identity(
        chipped,
        filename=CHIPPED_FILENAME,
        size=CHIPPED_SIZE,
        sha1=CHIPPED_SHA1,
        sha256=CHIPPED_SHA256,
        sha512=CHIPPED_SHA512,
    )
    verify_file_identity(
        athena,
        filename=ATHENA_FILENAME,
        size=ATHENA_SIZE,
        sha1=ATHENA_SHA1,
        sha256=ATHENA_SHA256,
        sha512=ATHENA_SHA512,
    )

    definitions: list[tuple[str, ...]] = []
    family_blocks: dict[str, list[str]] = {loader: [] for loader in LOADERS}
    all_blocks: list[str] = []
    model_keys: set[str] = set()
    texture_keys: set[str] = set()
    required_paths: set[str] = set()

    with zipfile.ZipFile(chipped) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)):
            raise ValueError("Chipped JAR contains duplicate ZIP entries")
        for path in sorted(names):
            prefix = "assets/chipped/blockstates/"
            if not path.startswith(prefix) or not path.endswith(".json"):
                continue
            bare_block = path[len(prefix) : -len(".json")]
            all_blocks.append(bare_block)
            parsed = _parse_definition(archive, path, archive.read(path))
            if parsed is None:
                continue
            row, model_path, textures = parsed
            definitions.append(row)
            loader = f"athena:{row[1]}"
            family_blocks[loader].append(bare_block)
            model_keys.add(row[2])
            texture_keys.update(textures)
            required_paths.add(path)
            required_paths.add(model_path)
            required_paths.update(
                resource_path(texture, "textures", ".png") for texture in textures
            )

        if len(all_blocks) != ALL_BLOCKSTATES_COUNT:
            raise ValueError("Chipped blockstate count changed")
        if roster_digest(all_blocks) != ALL_BLOCKSTATES_DIGEST:
            raise ValueError("Chipped complete blockstate roster changed")
        for loader, (count, expected_digest, _roles, _parent) in LOADERS.items():
            values = family_blocks[loader]
            if len(values) != count or roster_digest(values) != expected_digest:
                raise ValueError(f"{loader} roster changed")
        routed = [block for values in family_blocks.values() for block in values]
        if len(routed) != ROSTER_COUNT or roster_digest(routed) != ROSTER_DIGEST:
            raise ValueError("Chipped Athena-loader roster changed")
        if len(model_keys) != MODEL_COUNT or roster_digest(model_keys) != MODEL_DIGEST:
            raise ValueError("Chipped Athena model roster changed")
        if len(texture_keys) != TEXTURE_COUNT or roster_digest(texture_keys) != TEXTURE_DIGEST:
            raise ValueError("Chipped Athena texture roster changed")

        resource_rows: list[str] = []
        resource_bytes = 0
        for path in sorted(required_paths):
            try:
                raw = archive.read(path)
            except KeyError as error:
                raise ValueError(f"missing required Chipped resource {path}") from error
            resource_rows.append(f"{path}\t{len(raw)}\t{digest_bytes(raw)}\n")
            resource_bytes += len(raw)

    definitions.sort(key=lambda row: row[0])
    definitions_raw = "".join("\t".join(row) + "\n" for row in definitions).encode(
        "ascii"
    )
    resources_raw = "".join(resource_rows).encode("ascii")
    definitions_digest = digest_bytes(definitions_raw)
    resources_digest = digest_bytes(resources_raw)

    family_counts = {
        loader.removeprefix("athena:"): LOADERS[loader][0]
        for loader in sorted(LOADERS)
    }
    family_digests = {
        loader.removeprefix("athena:"): LOADERS[loader][1]
        for loader in sorted(LOADERS)
    }
    catalog = {
        "schemaVersion": 1,
        "baseline": {
            "packVersion": "1.2.0",
            "packRepositoryCommit": "c7bb230f21d14d26859d0b92548f089b3a493ad9",
            "minecraft": "1.21.1",
            "neoforge": "21.1.248",
            "java": 21,
        },
        "requiredForStaticRendering": ["chipped", "athena"],
        "artifacts": [
            {
                "modId": "chipped",
                "metadataVersion": "4.0.2",
                "filename": CHIPPED_FILENAME,
                "sizeBytes": CHIPPED_SIZE,
                "sha1": CHIPPED_SHA1,
                "sha256": CHIPPED_SHA256,
                "sha512": CHIPPED_SHA512,
                "license": "Terrarium License v1 / All Rights Reserved assets",
                "curseForgeProjectId": 456956,
                "curseForgeFileId": 5813117,
                "curseForgeFingerprint": 527531260,
                "modrinthProjectId": "BAscRYKm",
                "modrinthVersionId": "eqVowbGc",
                "verificationRole": "consumer-resource-owner",
            },
            {
                "modId": "athena",
                "metadataVersion": "4.0.6",
                "filename": ATHENA_FILENAME,
                "sizeBytes": ATHENA_SIZE,
                "sha1": ATHENA_SHA1,
                "sha256": ATHENA_SHA256,
                "sha512": ATHENA_SHA512,
                "license": "MIT",
                "curseForgeProjectId": 841890,
                "curseForgeFileId": 8061947,
                "curseForgeFingerprint": 669268138,
                "modrinthProjectId": "b1ZV3DIJ",
                "modrinthVersionId": "dJgL278E",
                "verificationRole": "renderer-format-identity",
            },
        ],
    }
    profile = {
        "schemaVersion": 1,
        "profileId": "chipped-athena-4.0.2-4.0.6",
        "minecraft": "1.21.1",
        "neoforge": "21.1.248",
        "chippedVersion": "4.0.2",
        "athenaVersion": "4.0.6",
        "coverage": {
            "allChippedBlockstates": ALL_BLOCKSTATES_COUNT,
            "allChippedBlockstatesDigest": ALL_BLOCKSTATES_DIGEST,
            "routedBlocks": ROSTER_COUNT,
            "routedBlocksDigest": ROSTER_DIGEST,
            "stockBlocks": ALL_BLOCKSTATES_COUNT - ROSTER_COUNT,
            "loaderCounts": family_counts,
            "loaderDigests": family_digests,
            "modelCount": MODEL_COUNT,
            "modelDigest": MODEL_DIGEST,
            "textureCount": TEXTURE_COUNT,
            "textureDigest": TEXTURE_DIGEST,
        },
        "definitionCatalog": {
            "path": "definitions.tsv",
            "rows": len(definitions),
            "sha256": definitions_digest,
        },
        "resourceClosure": {
            "path": "required-resources.tsv",
            "rows": len(resource_rows),
            "bytes": resource_bytes,
            "sha256": resources_digest,
        },
        "runtimePolicy": {
            "resourceSource": "operator-installed roots only",
            "pixelOverrides": "allowed when all schema and texture IDs remain exact",
            "schemaOverrides": "deactivate the route and preserve stock rendering",
            "nonNativeAppearanceProxies": "stock fallback",
        },
    }
    outputs = {
        CATALOG_PATH: json.dumps(catalog, indent=2, sort_keys=True).encode("utf-8")
        + b"\n",
        PROFILE_PATH: json.dumps(profile, indent=2, sort_keys=True).encode("utf-8")
        + b"\n",
        DEFINITIONS_PATH: definitions_raw,
        RESOURCES_PATH: resources_raw,
    }
    return outputs


def apply_outputs(outputs: dict[Path, bytes], *, check: bool) -> None:
    mismatches: list[str] = []
    for path, expected in outputs.items():
        if check:
            if not path.is_file() or path.read_bytes() != expected:
                mismatches.append(str(path))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(expected)
    if mismatches:
        raise ValueError("generated profile is stale: " + ", ".join(mismatches))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--chipped", required=True, type=Path)
    parser.add_argument("--athena", required=True, type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    outputs = build_outputs(args.chipped, args.athena)
    apply_outputs(outputs, check=args.check)
    action = "verified" if args.check else "generated"
    print(f"{action} exact Chipped/Athena profile ({ROSTER_COUNT} routed blocks)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
