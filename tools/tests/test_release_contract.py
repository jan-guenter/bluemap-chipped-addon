# SPDX-License-Identifier: MIT
"""Static release-evidence regression coverage."""

from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]


class ReleaseContractTest(unittest.TestCase):
    def test_alpha2_candidate_seals_all_publication_payloads(self) -> None:
        release = json.loads((ROOT / "provenance/release.json").read_text())

        self.assertEqual(1, release["schema_version"])
        self.assertEqual("owner-accepted-release-candidate", release["status"])
        self.assertEqual("0.1.0-alpha.2", release["version"])
        self.assertEqual("v0.1.0-alpha.2", release["tag"])
        self.assertEqual(
            {
                "production_jar": {
                    "file_name": "bluemap-chipped-addon-0.1.0-alpha.2.jar",
                    "size": 599_702,
                    "sha256": "2bf02cecde1f74cbb3be528710823367db5e487aef709a0aef0f64aeb2ee4713",
                },
                "sources_jar": {
                    "file_name": "bluemap-chipped-addon-0.1.0-alpha.2-sources.jar",
                    "size": 558_620,
                    "sha256": "f039709ee4741c6f92c208a1a5934b2f3aebfed15e5328e50f785cd0bb206d1c",
                },
                "pom": {
                    "file_name": "bluemap-chipped-addon-0.1.0-alpha.2.pom",
                    "size": 1_341,
                    "sha256": "db6addec7b3c0e32c3b71ada5b670b6ad8e5fe60413e9b2a93b6199ed6d7b9c7",
                },
                "gradle_module": {
                    "file_name": "bluemap-chipped-addon-0.1.0-alpha.2.module.json",
                    "size": 2_820,
                    "sha256": "5b3642845ffa163a57355a3813055c6333d2b467138b6c5d68cbcc7e842e1db4",
                },
            },
            release["final_release_artifacts"],
        )

    def test_alpha2_candidate_records_the_bounded_athena_migration(self) -> None:
        release = json.loads((ROOT / "provenance/release.json").read_text())

        self.assertEqual(
            {
                "module_repository": "https://github.com/jan-guenter/bluemap-athena-resource-models",
                "module_version": "0.1.0-alpha.1",
                "module_tag": "v0.1.0-alpha.1",
                "module_commit": "4a503a63f7f10b7c414c6c1228207a5ba00bfd54",
                "module_source_tree": "882689c2f9a0875547f4e30aefd68659103d5046",
                "removed_local_model_sources": 4,
                "renderer_or_gallery_behavior_change": False,
            },
            release["athena_model_migration"],
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
