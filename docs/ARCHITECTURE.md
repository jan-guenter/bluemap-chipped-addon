# Architecture

This repository produces one plain BlueMap add-on JAR. It is not a NeoForge
mod and has no client renderer, world state, packet, or required configuration.

```text
BlueMap add-on entrypoint
        |
exact BlueMap 5.22 internal adapter
        |
dual exact-JAR + active-resource-schema gate
        |
1,427 immutable Chipped definitions
        |
seven bounded Athena-family renderers
        |
four commit-pinned pure model classes
        |
operator-installed models and textures
```

## Activation boundary

The route starts inactive. Activation requires exactly the All the Mons 1.2.0
Chipped 4.0.2 and Athena 4.0.6 byte identities, the exact 1,427-block roster,
and the expected active blockstate/model/texture-key schemas. Higher-priority
resource packs may replace pixels without changing those schemas. A roster,
model, texture-key, or schema change deactivates the complete route and leaves
BlueMap's stock resource path in place.

Only the exact `chipped:*` catalog is redirected to the synthetic dispatch
model. The remaining 5,554 Chipped blockstates stay stock. The extension adds
all 5,947 installed texture keys before atlas filtering and caches only the
metadata-only parsed definitions. It bundles no Chipped or Athena resource.

## Renderer families

The pure `CtmTextureRole`, `CtmSelector`, `CtmConnections`, and `CubeFace`
classes compile from the exact released `bluemap-athena-resource-models`
source tree. The module has no entrypoint or installed runtime. Every emitter,
profile, resource gate, route, and fallback remains in this add-on.

- `ctm` samples the eight exact-state neighbors in each face plane, selects a
  texture per quadrant, and suppresses a face against the same block ID.
- `pillar` uses persisted `axis`, exact-state chain neighbors, cap textures,
  and face/axis UV rotation.
- `giant` selects a stable 2-by-2 tile from absolute world coordinates and
  the rendered face.
- `carpet_ctm` emits the installed one-sixteenth-high shape and connected
  top/bottom surfaces.
- `pane_ctm` and `pane_pillar` emit centered one-eighth-thick geometry from
  persisted cardinal booleans, including vertical seam rules.
- `limited_pillar` is the fixed-Y, same-block chain form.

Every renderer reads only the block ID, persisted properties, a bounded
neighborhood, and coordinates. Output is planned into a reversible tile-model
segment; an invalid observation or emission resets partial geometry and calls
the original Chipped blockstate renderer. Unknown cross-mod appearance/camo
proxies deliberately use stock fallback because Anvil data cannot reproduce
NeoForge's live `getAppearance` dispatch.

Pane and carpet routes are always non-occluding. Every other owned ordinary
model is a full cube, so the active model's alpha-sensitive culling result is
used for both culling and occlusion; glass and ice therefore do not become
opaque through the synthetic dispatch.
