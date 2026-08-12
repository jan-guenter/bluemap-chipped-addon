# Provenance

The machine-readable lock lives in
`src/main/resources/bluemap-chipped/profiles/exact-artifacts.json`, the exact
profile directory beside it, and `provenance/upstreams.json`.

The exact All the Mons 1.2.0 server archive members establish the Chipped
4.0.2 and installed Athena 4.0.6 byte identities. The metadata generator
verifies filename, size, SHA-1, SHA-256, SHA-512, the complete 6,981-blockstate
roster, all seven routed rosters, 1,427 model IDs, 5,947 texture IDs, every
loader/model schema, and the 8,801-path resource closure. Generated output
contains only identifiers, counts, sizes, and hashes.

Chipped release commit `64144066d5a029e3b111d03f25ca132b4b99efaa`
is release-correlated by version, timing, changelog, and 36,816 byte-identical
common resources. Athena commit
`deb1209837a201f7ac9f0f3a616521dc1831b78e` is release-correlated to the
exact publication. These correlations are not reproducible-build or source
attestations.

Chipped non-code assets are All Rights Reserved under the Terrarium License
v1; Athena and this implementation are MIT. The implementation uses a
behavior-only clean-room oracle and operator-installed JSON/PNG resources at
runtime. It commits no upstream source, class, model, texture, translation,
capture, or derived mesh.

Repository/build/release mechanics and narrow BlueMap adapter/emitter patterns
were independently authored from the owner's MIT Pipez and Sophisticated
projects. No family profile, resource fact, state decoder, or renderer was
transferred.
