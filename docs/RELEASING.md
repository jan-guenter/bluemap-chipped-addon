# Release procedure

Pull-request CI is the authoritative clean gate. It reacquires both exact
third-party artifacts and runs profile generation checks, Python and Java
tests, compilation, packaging boundaries, exact-input verification, and Maven
metadata generation in one pass.

Before tagging:

1. Initialize all pinned submodules with
   `git submodule update --init --recursive -- tooling/bluemap-addon-toolkit modules/bluemap-athena-resource-models modules/bluemap-addon-render-core modules/bluemap-addon-adapter-api`.
   Require the settings trust preflight without changing either gitlink.
2. Confirm the reviewed commit, recursively clean repository, version,
   changelog, provenance, and exact profile.
3. Require passing PR CI and inspect its production JAR/publication metadata.
4. Complete the single staging lifecycle in [STAGING.md](STAGING.md), including
   the exhaustive placement census, one save/restart, bounded render, browser
   sanity check, and owner visual acceptance.
5. Merge version changes through a PR and create annotated tag
   `v<addon_version>` on the reviewed main commit.

The tag workflow rebuilds from the exact inputs, publishes immutable GitHub
prerelease assets and matching GitHub Packages coordinates, and deploys
nothing. Never move a published tag or replace a release asset.
