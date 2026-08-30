# Compatibility

Compatibility is exact and evidence-locked.

| Component | Accepted identity |
| --- | --- |
| All the Mons | `1.2.0`, repository commit `c7bb230f21d14d26859d0b92548f089b3a493ad9` |
| Minecraft / NeoForge / Java | `1.21.1` / `21.1.248` / `21` |
| BlueMap | feature backport `5.22-feature.backport-5.23-stateless-java-web-server-46`, commit `7e07f4e74ec1e92a6ead9aa1e66054af3e133aac` |
| Chipped | `chipped-neoforge-1.21.1-4.0.2.jar`, 15,020,578 bytes, SHA-256 `18ac6fd6b30db4922ccc6ee8bea5b113f69587505b7529834f37ace506427291` |
| Athena | `athena-neoforge-1.21.1-4.0.6.jar`, 99,944 bytes, SHA-256 `43699885bbce3343916d4c5c4940cf0e3f9f6f02fdeb46e8655e121b42282ec5` |
| Bundled model source | `bluemap-athena-resource-models` `0.1.0-alpha.1`, commit `4a503a63f7f10b7c414c6c1228207a5ba00bfd54`, source tree `882689c2f9a0875547f4e30aefd68659103d5046` |
| Bundled face-light source | `bluemap-addon-render-core` `0.1.0-alpha.1`, commit `faf53c9586a2c876b5a91db5ae3c2650a98f19ba`, source tree `73870b3976ad3a17bf4bf350d9531b66d3d4a3af` |
| Bundled adapter source | `bluemap-addon-adapter-api` `0.1.0-alpha.2` release, commit `e81f08bc4bfbf02d810ec8949a019130e2e61634`, source tree `2f974c9bb2ba13888d69682f86f30f58922d30eb` |

Both artifacts are mandatory even though Chipped declares Athena
`[4.0.0,)`: the installed behavior under review is the exact 4.0.2/4.0.6
tuple. The route additionally validates the active resource schema, allowing
pixel-only resource-pack replacements while rejecting schema changes.
All three source modules are build inputs, not installed runtime dependencies.

This is not a compatibility claim for another Chipped/Athena build, later
All the Mons release, Chisel's CTM format, Rechiseled's Fusion format, or a
cross-mod appearance proxy. Each new byte tuple needs a new profile and visual
review.
