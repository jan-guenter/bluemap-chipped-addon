# SPDX-License-Identifier: MIT
"""Static release-evidence regression coverage."""

from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]


class ReleaseContractTest(unittest.TestCase):
    def test_alpha5_candidate_seals_all_publication_payloads(self) -> None:
        release = json.loads((ROOT / "provenance/release.json").read_text())

        self.assertEqual(1, release["schema_version"])
        self.assertEqual("owner-accepted-release-candidate", release["status"])
        self.assertEqual("0.1.0-alpha.5", release["version"])
        self.assertEqual("v0.1.0-alpha.5", release["tag"])
        self.assertEqual(
            {
                "production_jar": {
                    "file_name": "bluemap-chipped-addon-0.1.0-alpha.5.jar",
                    "size": 603_595,
                    "sha256": "6dc89c1f4a162177c703aef2d683e921cf62dbd9aac562ae0af9caed0d422624",
                },
                "sources_jar": {
                    "file_name": "bluemap-chipped-addon-0.1.0-alpha.5-sources.jar",
                    "size": 562_320,
                    "sha256": "3daa5c235dae2ba96e227641120e0a026b5d2017cb3af44541a897d875c36221",
                },
                "pom": {
                    "file_name": "bluemap-chipped-addon-0.1.0-alpha.5.pom",
                    "size": 1_341,
                    "sha256": "c67dcce4dbeaea23d761522167a2c7d3051013c7d4e32475679aad95a0ee0a49",
                },
                "gradle_module": {
                    "file_name": "bluemap-chipped-addon-0.1.0-alpha.5.module.json",
                    "size": 2_820,
                    "sha256": "dad8be96c27476ad0fd7d39bc087431375b80809e4134d22b534210c7bd51a5b",
                },
                "sha256sums": {
                    "file_name": "SHA256SUMS",
                    "size": 448,
                    "sha256": "c96619642be0e88bb5dd60897295391c7c14ca048cf32ac845b9bed5822171b0",
                },
            },
            release["final_release_artifacts"],
        )

    def test_alpha5_candidate_records_all_source_modules(self) -> None:
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
                "baseline_version": "0.1.0-alpha.3",
                "baseline_release_commit": "81d0b48dc1043136176caa78affeeab0fd3511b4",
                "baseline_production_jar_size": 601_011,
                "baseline_production_jar_sha256":
                    "b5a1e7184f98ebea44fc085fcc5dfcd54096fafae9ae158915476b33df1f9cac",
                "module_repository":
                    "https://github.com/jan-guenter/bluemap-addon-adapter-api",
                "module_version": "0.1.0-alpha.2",
                "module_tag": "v0.1.0-alpha.2",
                "module_release_commit": "e81f08bc4bfbf02d810ec8949a019130e2e61634",
                "module_source_tree": "2f974c9bb2ba13888d69682f86f30f58922d30eb",
                "bluemap_commit": "7e07f4e74ec1e92a6ead9aa1e66054af3e133aac",
                "compiled_source_count": 4,
                "standalone_module_jar_bundled": False,
                "standalone_module_jar_installed": False,
                "local_adapter_package":
                    "io.github.janguenter.bluemap.chipped.adapter.bluemap523",
                "displaced_local_helpers": [
                    "AdapterCompatibility",
                    "ChippedResourceExtensionType",
                    "BlueMap522Adapter registry helpers",
                    "ChippedResourceExtension synthetic-dispatch predicate",
                ],
                "production_archive": {
                    "old_entries": 50,
                    "new_entries": 52,
                    "unchanged_entries": 32,
                    "changed_common_entries": 6,
                    "removed_local_adapter_classes": 12,
                    "added_shared_and_renamed_adapter_classes": 14,
                },
                "preserved_contract": {
                    "renderer_registration_count": 1,
                    "resource_extension_registration_count": 1,
                    "registry_failure_reason": "registry-collision",
                    "routed_definition_count": 1_427,
                    "runtime_profile_and_renderer_behavior_changed": False,
                    "gallery_sources_changed": False,
                    "consumer_tests_passed": 25,
                },
            },
            release["adapter_api_migration"],
        )
        self.assertEqual(
            {
                "superseded_version": "0.1.0-alpha.4",
                "superseded_tag": "v0.1.0-alpha.4",
                "superseded_release_commit":
                    "b615af00c9255e9178f7358fc2c290364b7bca25",
                "substantive_release_payloads_valid": True,
                "recorded_checksum_file": {
                    "size": 440,
                    "sha256":
                        "26418b06f3695d9f86c1bb73bdd77f1f1affc28e92d3eb9759515803597a4859",
                    "path_prefix": "none",
                },
                "published_checksum_file": {
                    "size": 448,
                    "sha256":
                        "666710cb002cdabd8b9be142f5561ebc13ff975a24b9911a568f3178a70fef43",
                    "path_prefix": "./",
                },
                "alpha4_tag_or_release_mutated": False,
                "correction": (
                    "Alpha.5 stages CI and tag bundles with one tool and verifies every "
                    "workflow-formatted payload against release provenance before "
                    "publication."
                ),
            },
            release["post_release_checksum_correction"],
        )
        self.assertEqual(
            {
                "baseline_production_jar_sha256":
                    "05ebaea5e4053b92c76819153a417a47277a8464569a2bd261b96fec776597ea",
                "baseline_sources_jar_sha256":
                    "3daa5c235dae2ba96e227641120e0a026b5d2017cb3af44541a897d875c36221",
                "production_archive_entries": 52,
                "unchanged_production_entries": 50,
                "changed_production_entries": [
                    "META-INF/MANIFEST.MF",
                    "bluemap.addon.json",
                ],
                "sources_jar_byte_identical": True,
                "runtime_classes_or_resources_changed": False,
                "gallery_sources_changed": False,
                "visual_staging_inherited": True,
            },
            release["alpha4_to_alpha5_equivalence"],
        )
        self.assertEqual(
            {
                "production_jar_exact_byte_gate": True,
                "sources_jar_exact_byte_gate": True,
                "publication_metadata_exact_byte_gate": True,
                "adapter_api_source_boundary_gate": True,
                "exact_feature_backport_runtime_identity_gate": True,
                "workflow_checksum_format_gate": True,
                "exact_input_gate": True,
                "reproducibility_gate": True,
                "hostile_gitlink_trust_probes": True,
            },
            release["verification"],
        )


if __name__ == "__main__":
    unittest.main()
