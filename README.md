# BlueMap Chipped Add-on

An exact-profile BlueMap 5.22 add-on for Chipped's Athena-backed connected
models on All the Mons 1.2.0.

## Status and compatibility

Version `0.1.0-alpha.2` is the source-consolidation candidate for the same
owner-accepted exact tuple:

- Chipped `4.0.2`, 15,020,578 bytes, SHA-256
  `18ac6fd6b30db4922ccc6ee8bea5b113f69587505b7529834f37ace506427291`;
- Athena `4.0.6`, 99,944 bytes, SHA-256
  `43699885bbce3343916d4c5c4940cf0e3f9f6f02fdeb46e8655e121b42282ec5`;
- Minecraft `1.21.1`, NeoForge `21.1.248`, Java `21`;
- BlueMap backport `5.22-agent.backport-5.22-mc1.21.1-2` at
  `9be321df995a1103808621d529eb72773e719d4d`.

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

The candidate changes source ownership only. It compiles the four pure Athena
connection and face classes from the released, commit-pinned
`bluemap-athena-resource-models` `0.1.0-alpha.1` source module. Emitters,
profiles, resource admission, routing, fallback, and visual behavior remain
local and unchanged.

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

For an existing clone, initialize both pinned source submodules before running
Gradle:

```bash
git submodule update --init --recursive -- \
  tooling/bluemap-addon-toolkit modules/bluemap-athena-resource-models
```

The settings preflight accepts only the committed toolkit and Athena-model
gitlinks. It rejects an uninitialized, changed, dirty, incorrectly pinned, or
source-tree-mismatched checkout.

```bash
gradle --no-daemon \
  -PchippedJar=/absolute/path/chipped-neoforge-1.21.1-4.0.2.jar \
  -PathenaJar=/absolute/path/athena-neoforge-1.21.1-4.0.6.jar \
  clean check build generatePomFileForAddonPublication \
  generateMetadataFileForAddonPublication verifyPinnedArtifacts
```

CI reacquires both inputs ephemerally, verifies their exact bytes and the full
resource/profile contract, and discards them. The add-on source-bundles only
the four first-party MIT model classes. It bundles no upstream Chipped or
Athena code or assets and no nested module JAR.

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
