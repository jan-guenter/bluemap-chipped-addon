# SPDX-License-Identifier: MIT
"""Static release-evidence regression coverage."""

from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]


class ReleaseContractTest(unittest.TestCase):
    def test_alpha3_candidate_seals_all_publication_payloads(self) -> None:
        release = json.loads((ROOT / "provenance/release.json").read_text())

        self.assertEqual(1, release["schema_version"])
        self.assertEqual("owner-accepted-release-candidate", release["status"])
        self.assertEqual("0.1.0-alpha.3", release["version"])
        self.assertEqual("v0.1.0-alpha.3", release["tag"])
        self.assertEqual(
            {
                "production_jar": {
                    "file_name": "bluemap-chipped-addon-0.1.0-alpha.3.jar",
                    "size": 601_011,
                    "sha256": "b5a1e7184f98ebea44fc085fcc5dfcd54096fafae9ae158915476b33df1f9cac",
                },
                "sources_jar": {
                    "file_name": "bluemap-chipped-addon-0.1.0-alpha.3-sources.jar",
                    "size": 559_912,
                    "sha256": "02e43090ca15ef9f48b58a306b186e9976b55cd64ed7a8ee6109398b6a2e267b",
                },
                "pom": {
                    "file_name": "bluemap-chipped-addon-0.1.0-alpha.3.pom",
                    "size": 1_341,
                    "sha256": "cd27953c5fe1b3d184fc6d1d07226cbdc826e7bfb95d887f084517d57c2a2b9b",
                },
                "gradle_module": {
                    "file_name": "bluemap-chipped-addon-0.1.0-alpha.3.module.json",
                    "size": 2_820,
                    "sha256": "52b856089a9e4d6ac0287c8f3e31d3cfeb44a75aa05b91fd831504e9a9240d09",
                },
            },
            release["final_release_artifacts"],
        )

    def test_alpha3_candidate_records_both_source_modules(self) -> None:
        release = json.loads((ROOT / "provenance/release.json").read_text())

        self.assertEqual(
            {
                "module_repository": "https://github.com/jan-guenter/bluemap-addon-render-core",
                "module_version": "0.1.0-alpha.1",
                "module_tag": "v0.1.0-alpha.1",
                "module_commit": "faf53c9586a2c876b5a91db5ae3c2650a98f19ba",
                "module_source_tree": "73870b3976ad3a17bf4bf350d9531b66d3d4a3af",
                "removed_local_sources": 1,
                "renderer_or_gallery_behavior_change": False,
            },
            release["render_core_migration"],
        )
        self.assertEqual(
            {
                "production_jar_exact_byte_gate": True,
                "sources_jar_exact_byte_gate": True,
                "publication_metadata_exact_byte_gate": True,
                "exact_input_gate": True,
                "reproducibility_gate": True,
                "hostile_gitlink_trust_probes": True,
            },
            release["verification"],
        )


if __name__ == "__main__":
    unittest.main()
