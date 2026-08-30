# Third-party components

| Component | Use | Exact identity | Declared license | Bundled |
| --- | --- | --- | --- | --- |
| BlueMap | Compile/runtime host ABI | Backport `5.22-agent.backport-5.22-mc1.21.1-2`, commit `9be321df995a1103808621d529eb72773e719d4d` | MIT | No |
| Chipped | Operator-installed consumer resources | `4.0.2`, 15,020,578 bytes, SHA-256 `18ac6fd6b30db4922ccc6ee8bea5b113f69587505b7529834f37ace506427291` | Terrarium License; assets reserved | No |
| Athena | Renderer-format identity only | `4.0.6`, 99,944 bytes, SHA-256 `43699885bbce3343916d4c5c4940cf0e3f9f6f02fdeb46e8655e121b42282ec5` | MIT | No |
| BlueMap Athena Resource Models | First-party pure connection and face model source | `0.1.0-alpha.1`, commit `4a503a63f7f10b7c414c6c1228207a5ba00bfd54`, source tree `882689c2f9a0875547f4e30aefd68659103d5046` | MIT | Four sources compile into this add-on; no module JAR |
| BlueMap Add-on Render Core | First-party BlueMap 5.22 face-light source | `0.1.0-alpha.1`, commit `faf53c9586a2c876b5a91db5ae3c2650a98f19ba`, source tree `73870b3976ad3a17bf4bf350d9531b66d3d4a3af` | MIT | One source compiles into this add-on; no module JAR |
| JetBrains annotations | Compile-only host dependency | `23.0.0` | Apache-2.0 | No |
| JUnit | Tests | `5.11.4` | EPL-2.0 | No |
| Checkstyle | Source style | `10.18.2` | LGPL-2.1-or-later | No |
| Gradle | CI build tool | `9.4.0` | Apache-2.0 | No |

The packaged profile contains only factual identifiers, loader families,
resource keys/paths, byte sizes, schemas, and hashes. It contains no
third-party resource bytes.
