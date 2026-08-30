# Agent guide for BlueMap Chipped Add-on

Read `/root/work/allthemons/AGENTS.md` and this file before changing this
repository. This is a standalone public MIT project, not a NeoForge mod and
not part of the root orchestration repository.

## Exact baseline

| Component | Identity |
| --- | --- |
| All the Mons | `1.2.0`, pack commit `c7bb230f21d14d26859d0b92548f089b3a493ad9` |
| Minecraft / NeoForge / Java | `1.21.1` / `21.1.248` / `21` |
| BlueMap | backport `5.22-agent.backport-5.22-mc1.21.1-2`, commit `9be321df995a1103808621d529eb72773e719d4d` |
| Chipped | `4.0.2`, 15,020,578 bytes, SHA-256 `18ac6fd6b30db4922ccc6ee8bea5b113f69587505b7529834f37ace506427291` |
| Athena | `4.0.6`, 99,944 bytes, SHA-256 `43699885bbce3343916d4c5c4940cf0e3f9f6f02fdeb46e8655e121b42282ec5` |
| Athena model source module | `0.1.0-alpha.1`, commit `4a503a63f7f10b7c414c6c1228207a5ba00bfd54`, source tree `882689c2f9a0875547f4e30aefd68659103d5046` |
| Render-core source module | `0.1.0-alpha.1`, commit `faf53c9586a2c876b5a91db5ae3c2650a98f19ba`, source tree `73870b3976ad3a17bf4bf350d9531b66d3d4a3af` |

A new pack or either changed artifact is a fresh evidence, implementation,
and review task.

## Project boundaries

- The production JAR is a plain BlueMap add-on. It contains no NeoForge
  metadata, Mixins, nested JARs, client bootstrap, or third-party classes or
  assets.
- Own exactly 1,427 `chipped:*` blockstates with one of seven exact
  `athena:loader` values. The other 5,554 Chipped blockstates remain stock.
- Preserve stable CTM seams, pillars/axes, 2×2 giant murals, carpets, panes,
  limited pillars, and pane pillars using installed resources.
- Use only block identity/properties, bounded neighbors, and stable world
  coordinates. NBT, BERs, animation, activity, and live contents are absent.
- Missing artifacts/resources, changed schemas, malformed state, or an
  unsupported appearance proxy use BlueMap's original path atomically.
- The implementation is clean-room MIT. Never copy/adapt Chipped or Athena
  source or package their classes, models, textures, captures, or meshes.
- Compile the four pure Athena connection and face classes and the exact
  BlueMap 5.22 face-light sampler from their pinned source modules. Keep
  emitters, profiles, admission, routing, and fallback local. Never install
  or nest either module JAR.

## Validation cadence

Develop in one coherent tranche. Pull-request CI is the authoritative full
gate; do not repeat it locally after small edits:

```bash
git submodule update --init --recursive -- \
  tooling/bluemap-addon-toolkit modules/bluemap-athena-resource-models \
  modules/bluemap-addon-render-core
gradle --no-daemon \
  -PchippedJar=/absolute/path/chipped-neoforge-1.21.1-4.0.2.jar \
  -PathenaJar=/absolute/path/athena-neoforge-1.21.1-4.0.6.jar \
  clean check build generatePomFileForAddonPublication \
  generateMetadataFileForAddonPublication verifyPinnedArtifacts
```

After CI, use the single enabled staging pass in [docs/STAGING.md](docs/STAGING.md).
Retain transparent CTM/pillar/giant/limited/pane witnesses and adjacent
carpets. Before presenting a BlueMap link, open that exact view in the agent
browser for the required lightweight visual sanity check.
