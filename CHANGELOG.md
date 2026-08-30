# Changelog

## 0.1.0-alpha.5 - 2026-08-30

- Preserve alpha.4's exact feature-backport runtime and shared adapter source.
- Stage review and tag bundles through one tool that writes the workflow's
  `./`-prefixed checksum lines and verifies all five payload identities against
  release provenance before upload.
- Supersede immutable alpha.4 because its tagged provenance recorded a locally
  generated checksum-file identity without the workflow's `./` prefixes. Its
  four substantive release payloads remain unchanged and valid.

## 0.1.0-alpha.4 - 2026-08-30

- Source-bundle four bootstrap helpers from the commit-pinned
  `bluemap-addon-adapter-api` `0.1.0-alpha.2` release.
- Remove the local runtime compatibility and resource-extension wrappers plus
  the inline registry and synthetic-dispatch implementations.
- Select only the audited BlueMap 5.23 feature-backport runtime identity. Keep
  Chipped renderers, factories, profiles, routes, failure reasons, fallback,
  and gallery behavior local.
- Reject a missing, changed, dirty, incorrectly pinned, or source-tree-mismatched
  adapter API checkout and reject displaced or unexpected shared classes in
  both publication JARs.

## 0.1.0-alpha.3 - 2026-08-30

- Source-bundle `FaceLighting` from the commit-pinned
  `bluemap-addon-render-core` `0.1.0-alpha.1` release and remove the exact
  local duplicate.
- Keep Chipped emission, profile admission, routing, fallback, gallery, and
  visual behavior unchanged.
- Reject a missing, changed, dirty, incorrectly pinned, or source-tree-mismatched
  render-core checkout and reject legacy or unexpected shared classes in both
  publication JARs.

## 0.1.0-alpha.2 - 2026-08-30

- Source-bundle the released `bluemap-athena-resource-models`
  `0.1.0-alpha.1` module at commit
  `4a503a63f7f10b7c414c6c1228207a5ba00bfd54`.
- Remove the four local duplicate model sources while retaining the exhaustive
  256-mask, face-basis, giant, pillar, pane, emitter, gallery, and exact-input
  tests.
- Fail closed when the module gitlink, index, checkout HEAD, source tree, or
  worktree differs from the reviewed pin. Keep every Chipped-specific profile,
  emitter, route, and fallback boundary local.

## 0.1.0-alpha.1 - 2026-08-13

- Add one exact Chipped 4.0.2 plus Athena 4.0.6 profile for ATMons 1.2.0.
- Route exactly 1,427 Athena-loader Chipped blockstates across seven families.
- Preserve stable CTM seams, axes, giant coordinate phases, carpet and pane
  geometry using only operator-installed resources.
- Add dual-artifact/schema gates, exhaustive metadata/resource verification,
  atomic stock fallback, deterministic gallery generation, and release CI.
- Record owner acceptance after the exact 598,326-byte production JAR passed
  the 1,642-placement staging gate, clean restart, canonical render audit, and
  browser sanity check; its SHA-256 is
  `b43c238b764e068db4009ab16fc2af140b54d84feaf37bd6577602e1dc97fd21`.
