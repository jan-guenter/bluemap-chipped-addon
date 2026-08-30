# BlueMap Chipped Add-on

An exact-profile BlueMap add-on for Chipped's Athena-backed connected models
on All the Mons 1.2.0.

## Status and compatibility

Version `0.1.0-alpha.5` corrects the checksum-file identity recorded for the
alpha.4 source-consolidation release. The add-on behavior remains the
owner-accepted Chipped/Athena renderer profile and accepts this exact tuple:

- Chipped `4.0.2`, 15,020,578 bytes, SHA-256
  `18ac6fd6b30db4922ccc6ee8bea5b113f69587505b7529834f37ace506427291`;
- Athena `4.0.6`, 99,944 bytes, SHA-256
  `43699885bbce3343916d4c5c4940cf0e3f9f6f02fdeb46e8655e121b42282ec5`;
- Minecraft `1.21.1`, NeoForge `21.1.248`, Java `21`;
- BlueMap feature backport
  `5.22-feature.backport-5.23-stateless-java-web-server-46` at
  `7e07f4e74ec1e92a6ead9aa1e66054af3e133aac`.

The route activates only when both installed JARs match exactly and every
active owned JSON resource retains its pinned schema and texture IDs. Pixel
overrides may change the appearance without changing the schema. A mismatched
tuple or schema stays on BlueMap's stock resource path.

The accepted production JAR is 598,326 bytes with SHA-256
`b43c238b764e068db4009ab16fc2af140b54d84feaf37bd6577602e1dc97fd21`.
It passed pull-request CI, the exhaustive 1,642-placement staging gate, a
clean restart and repeat verification, the canonical rendered-model audit,
the required agent-browser sanity check, and owner visual inspection on
2026-08-13.

The candidate changes adapter-source ownership and the supported BlueMap
identity. It retains the four pure Athena connection and face classes from the
released, commit-pinned `bluemap-athena-resource-models` `0.1.0-alpha.1` source
module. It also compiles
the exact face-light sampler from the released `bluemap-addon-render-core`
`0.1.0-alpha.1` module at commit
`faf53c9586a2c876b5a91db5ae3c2650a98f19ba`, source tree
`73870b3976ad3a17bf4bf350d9531b66d3d4a3af`. Emitters, profiles, resource
admission, routing, fallback, and visual behavior remain local and unchanged.
It compiles four bootstrap helpers from the
`bluemap-addon-adapter-api` `0.1.0-alpha.2` release at commit
`e81f08bc4bfbf02d810ec8949a019130e2e61634`, source tree
`2f974c9bb2ba13888d69682f86f30f58922d30eb`. Chipped selects only the exact
feature-backport runtime identity.

## Visual scope

The exact Chipped JAR contains 6,981 blockstates. This add-on owns the 1,427
whose default variant uses one of these Athena loaders:

| Loader | Blocks |
| --- | ---: |
| CTM cube | 896 |
| Pillar | 248 |
| Giant 2×2 mural | 108 |
| Connected pane | 93 |
| Connected carpet | 48 |
| Limited vertical pillar | 17 |
| Pillar pane | 17 |

It preserves exact-state connected seams, persisted pillar axes, stable
coordinate phases, carpet height, persisted pane arms and transparent
materials. The other 5,554 Chipped blockstates remain under stock BlueMap.
No block entities or transient state are read. Non-native appearance proxies
cannot be reconstructed from Anvil data and intentionally fall back.

See [coverage](docs/COVERAGE.md), [architecture](docs/ARCHITECTURE.md),
[compatibility](docs/COMPATIBILITY.md), [provenance](docs/PROVENANCE.md), and
the single [staging gate](docs/STAGING.md).

## Authoritative review gate

Use Java 21 and the exact sibling BlueMap checkout. Supply the two exact
operator-downloaded inputs once:

```bash
git clone --recurse-submodules \
  https://github.com/jan-guenter/bluemap-chipped-addon.git
```

For an existing clone, initialize all pinned development inputs before running
Gradle:

```bash
git submodule update --init --recursive -- \
  tooling/bluemap-addon-toolkit modules/bluemap-athena-resource-models \
  modules/bluemap-addon-render-core modules/bluemap-addon-adapter-api
```

The settings preflight accepts only the committed toolkit, Athena-model,
render-core, and adapter API gitlinks. It rejects an uninitialized, changed,
dirty, incorrectly pinned, or source-tree-mismatched checkout.

```bash
gradle --no-daemon \
  -PchippedJar=/absolute/path/chipped-neoforge-1.21.1-4.0.2.jar \
  -PathenaJar=/absolute/path/athena-neoforge-1.21.1-4.0.6.jar \
  clean check build generatePomFileForAddonPublication \
  generateMetadataFileForAddonPublication verifyPinnedArtifacts
```

CI reacquires both runtime inputs ephemerally, verifies their exact bytes and
the full resource/profile contract, and discards them. It also stages the five
release payloads in the tag workflow's exact checksum format and compares every
byte identity with the release provenance. The add-on
source-bundles only the four first-party MIT model classes, one first-party
MIT face-light class, and four first-party MIT adapter helpers. It bundles no
upstream Chipped or Athena code or assets and no nested module JAR.

Tagged releases publish production/source JARs, POM, module metadata, and
checksums on GitHub Releases and at Maven coordinates
`io.github.jan-guenter:bluemap-chipped-addon:<version>` on GitHub Packages. A
release tag must equal `v<addon_version>`.

## Installation

Place only the reviewed add-on JAR in BlueMap's `config/bluemap/packs`
directory and restart the JVM. It is not a NeoForge mod and does not belong in
the server's `mods` directory. Removal plus one restart restores stock
rendering; the add-on writes no world or player data.

## License

The add-on is independently written and released under the [MIT License](LICENSE).
Third-party software and resources are not bundled; see
[THIRD_PARTY.md](THIRD_PARTY.md) and [NOTICE.md](NOTICE.md).
