# Provenance

The machine-readable lock lives in
`src/main/resources/bluemap-chipped/profiles/exact-artifacts.json`, the exact
profile directory beside it, and `provenance/upstreams.json`. Candidate release
identity is recorded separately in `provenance/release.json`; it is not packed
into the add-on JAR.

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

Version `0.1.0-alpha.2` source-bundles four pure first-party model classes from
the released MIT `bluemap-athena-resource-models` `0.1.0-alpha.1` module at
commit `4a503a63f7f10b7c414c6c1228207a5ba00bfd54`, source tree
`882689c2f9a0875547f4e30aefd68659103d5046`. The module records their earliest
matching Chipped history commit and exhaustive algorithm parity. Its JAR is
neither installed nor nested. The emitter, exact profile, resource admission,
routing, and stock fallback remain local.

Version `0.1.0-alpha.3` also source-bundles the exact first-party
`FaceLighting` class from the MIT `bluemap-addon-render-core`
`0.1.0-alpha.1` release at commit
`faf53c9586a2c876b5a91db5ae3c2650a98f19ba`, source tree
`73870b3976ad3a17bf4bf350d9531b66d3d4a3af`. Only the package and public API
visibility differ from the removed local class; executable behavior is
unchanged. The module records the original Sophisticated add-on commit, the
frozen source hash, and all seven exact portfolio matches. Its JAR is neither
installed nor nested.

Version `0.1.0-alpha.4` source-bundles four first-party bootstrap helpers from
the MIT `bluemap-addon-adapter-api` `0.1.0-alpha.2` release at commit
`e81f08bc4bfbf02d810ec8949a019130e2e61634`, source tree
`2f974c9bb2ba13888d69682f86f30f58922d30eb`. It removes the local runtime
compatibility and resource-extension wrapper classes plus the inline registry
and synthetic-dispatch implementations. Chipped selects only the exact 5.23
feature-backport identity and keeps every renderer, factory, route, failure reason,
profile, and fallback decision local. The module JAR is neither installed nor
nested.
