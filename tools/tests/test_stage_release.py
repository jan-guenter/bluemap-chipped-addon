# SPDX-License-Identifier: MIT
"""Regression coverage for exact release-bundle staging."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "stage_release", ROOT / "tools/stage_release.py"
)
assert SPEC is not None and SPEC.loader is not None
stage_release = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(stage_release)


class StageReleaseTest(unittest.TestCase):
    VERSION = "0.1.0-test.1"

    def _write_inputs(self, root: Path) -> None:
        libraries = root / "build/libs"
        publication = root / "build/publications/addon"
        libraries.mkdir(parents=True)
        publication.mkdir(parents=True)
        (libraries / f"bluemap-chipped-addon-{self.VERSION}.jar").write_bytes(b"jar")
        (libraries / f"bluemap-chipped-addon-{self.VERSION}-sources.jar").write_bytes(
            b"sources"
        )
        (publication / "pom-default.xml").write_bytes(b"pom")
        (publication / "module.json").write_bytes(b"module")

    def test_stage_uses_the_workflow_dot_slash_checksum_format(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._write_inputs(root)
            staged = stage_release.stage(root, root / "release", self.VERSION)

            checksum = staged["sha256sums"].read_text(encoding="ascii")
            lines = checksum.splitlines()
            self.assertEqual(4, len(lines))
            self.assertEqual(lines, sorted(lines, key=lambda line: line.split("./", 1)[1]))
            self.assertTrue(all("  ./bluemap-chipped-addon-" in line for line in lines))

    def test_provenance_must_match_every_staged_byte(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._write_inputs(root)
            staged = stage_release.stage(root, root / "release", self.VERSION)
            artifacts = {
                key: {
                    "file_name": path.name,
                    "size": path.stat().st_size,
                    "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                }
                for key, path in staged.items()
            }
            provenance = root / "release.json"
            provenance.write_text(
                json.dumps(
                    {
                        "version": self.VERSION,
                        "tag": f"v{self.VERSION}",
                        "final_release_artifacts": artifacts,
                    }
                ),
                encoding="utf-8",
            )

            stage_release.verify_provenance(provenance, self.VERSION, staged)
            artifacts["sha256sums"]["size"] += 1
            provenance.write_text(
                json.dumps(
                    {
                        "version": self.VERSION,
                        "tag": f"v{self.VERSION}",
                        "final_release_artifacts": artifacts,
                    }
                ),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "sha256sums"):
                stage_release.verify_provenance(provenance, self.VERSION, staged)


if __name__ == "__main__":
    unittest.main()
