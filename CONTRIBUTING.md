# Contributing

Open an issue before expanding the supported byte tuple, loader families, or
visual scope. Compatibility is an exact profile, never a version range.

Contributions must be independently written under MIT. Do not copy or adapt
Chipped or Athena source, classes, models, textures, translations, captures,
or meshes. Third-party inputs stay local and ignored.

Malformed state and changed schemas must return the whole block to BlueMap's
original path. Submit one coherent change and rely on pull-request CI for the
authoritative clean gate described in [AGENTS.md](AGENTS.md). Clone with
`--recurse-submodules`, or initialize an existing checkout with:

```bash
git submodule update --init --recursive -- \
  tooling/bluemap-addon-toolkit modules/bluemap-athena-resource-models \
  modules/bluemap-addon-render-core modules/bluemap-addon-adapter-api
```
