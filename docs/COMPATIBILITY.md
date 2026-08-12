# Compatibility

Compatibility is exact and evidence-locked.

| Component | Accepted identity |
| --- | --- |
| All the Mons | `1.2.0`, repository commit `c7bb230f21d14d26859d0b92548f089b3a493ad9` |
| Minecraft / NeoForge / Java | `1.21.1` / `21.1.248` / `21` |
| BlueMap | `5.22-agent.backport-5.22-mc1.21.1-2`, commit `9be321df995a1103808621d529eb72773e719d4d` |
| Chipped | `chipped-neoforge-1.21.1-4.0.2.jar`, 15,020,578 bytes, SHA-256 `18ac6fd6b30db4922ccc6ee8bea5b113f69587505b7529834f37ace506427291` |
| Athena | `athena-neoforge-1.21.1-4.0.6.jar`, 99,944 bytes, SHA-256 `43699885bbce3343916d4c5c4940cf0e3f9f6f02fdeb46e8655e121b42282ec5` |

Both artifacts are mandatory even though Chipped declares Athena
`[4.0.0,)`: the installed behavior under review is the exact 4.0.2/4.0.6
tuple. The route additionally validates the active resource schema, allowing
pixel-only resource-pack replacements while rejecting schema changes.

This is not a compatibility claim for another Chipped/Athena build, later
All the Mons release, Chisel's CTM format, Rechiseled's Fusion format, or a
cross-mod appearance proxy. Each new byte tuple needs a new profile and visual
review.
