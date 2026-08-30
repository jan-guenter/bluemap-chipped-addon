# SPDX-License-Identifier: MIT
"""Static release-evidence regression coverage."""

from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]


class ReleaseContractTest(unittest.TestCase):
    def setUp(self) -> None:
        self.release = json.loads(
            (ROOT / "provenance/release.json").read_text(encoding="utf-8")
        )

    def test_alpha6_candidate_seals_all_publication_payloads(self) -> None:
        self.assertEqual(1, self.release["schema_version"])
        self.assertEqual("owner-accepted-release-candidate", self.release["status"])
        self.assertEqual("0.1.0-alpha.6", self.release["version"])
        self.assertEqual("v0.1.0-alpha.6", self.release["tag"])
        self.assertEqual(
            {
                "production_jar": {
                    "file_name": "bluemap-chipped-addon-0.1.0-alpha.6.jar",
                    "size": 603_586,
                    "sha256":
                        "4d3e0b0a0f6663c23595dd7a5565e4f05e5552d04a13f887aa0ab7364cc701a8",
                },
                "sources_jar": {
                    "file_name": "bluemap-chipped-addon-0.1.0-alpha.6-sources.jar",
                    "size": 562_312,
                    "sha256":
                        "feacf746981e09883b53c19a2634c7cf63d5659c2cf99da9a0fb248069d4d663",
                },
                "pom": {
                    "file_name": "bluemap-chipped-addon-0.1.0-alpha.6.pom",
                    "size": 1_341,
                    "sha256":
                        "88866556c5b05dabc5a33d1465c264f3f1e3f3005de163160ba00f6824547a27",
                },
                "gradle_module": {
                    "file_name": "bluemap-chipped-addon-0.1.0-alpha.6.module.json",
                    "size": 2_820,
                    "sha256":
                        "f129eb560b6ecae1d33cdbf55bc7913d69cc009cf92f671bc2915235326a1756",
                },
                "sha256sums": {
                    "file_name": "SHA256SUMS",
                    "size": 448,
                    "sha256":
                        "753b7960fc74704aa2df4c69cbacef708cefd64224c5c38480e812e9212542dd",
                },
            },
            self.release["final_release_artifacts"],
        )

    def test_alpha6_candidate_records_exact_523_source_modules(self) -> None:
        migration = self.release["render_core_523_migration"]
        self.assertEqual("0.1.0-alpha.2", migration["module_version"])
        self.assertEqual("v0.1.0-alpha.2", migration["module_tag"])
        self.assertEqual(
            "24b84efdc8235f3f1323e1a8e9fd033080e3a79e",
            migration["module_release_commit"],
        )
        self.assertEqual(
            "424040931680fb82d37693f893ca887c0ed48eae",
            migration["module_source_tree"],
        )
        self.assertEqual(
            "7e07f4e74ec1e92a6ead9aa1e66054af3e133aac",
            migration["bluemap_commit"],
        )
        self.assertEqual(
            "285c9a60eff3ac2b0cab308ce1058d1565be0971",
            migration["bluemap_api_commit"],
        )
        self.assertEqual(
            "io.github.janguenter.bluemap.addon.render.core.adapter.bluemap523",
            migration["source_package"],
        )
        self.assertFalse(migration["standalone_module_jar_bundled"])
        self.assertFalse(migration["standalone_module_jar_installed"])
        preserved = migration["preserved_contract"]
        self.assertFalse(preserved["runtime_profile_and_renderer_behavior_changed"])
        self.assertFalse(preserved["gallery_sources_changed"])

        adapter = self.release["adapter_api_source"]
        self.assertEqual("0.1.0-alpha.2", adapter["module_version"])
        self.assertEqual(
            "e81f08bc4bfbf02d810ec8949a019130e2e61634",
            adapter["module_release_commit"],
        )
        self.assertEqual(
            "2f974c9bb2ba13888d69682f86f30f58922d30eb",
            adapter["module_source_tree"],
        )

    def test_release_uses_one_provenance_checked_staging_tool(self) -> None:
        self.assertEqual(
            {
                "tool": "tools/stage_release.py",
                "workflow_uses_same_tool": True,
                "checksum_path_prefix": "./",
                "payload_count": 5,
                "provenance_exact_byte_verification": True,
            },
            self.release["release_staging"],
        )
        self.assertTrue(
            self.release["verification"]["gradle_9_4_reproducibility_gate"]
        )
        self.assertTrue(
            self.release["verification"]["gradle_9_6_compatibility_gate"]
        )


if __name__ == "__main__":
    unittest.main()
