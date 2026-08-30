# ADR 0002: source-bundle the shared face-light sampler

Status: accepted for the `0.1.0-alpha.3` candidate.

## Decision

Compile `FaceLighting` from the exact gitlink-pinned
`bluemap-addon-render-core` source tree and remove Chipped's token-identical
local class. Do not install or nest the module JAR.

The module contains only the BlueMap 5.22 sampler already used here. Chipped
keeps its emitter, Athena models, profile, route, and stock fallback. The
shared class changes only its package and API visibility. Its executable
statements and nested `Sample` record components remain unchanged.

The settings preflight checks the committed and indexed gitlink, checkout
HEAD, source-tree hash, and clean worktree. Archive gates require one shared
class and nested record class, reject the removed local package, reject every
other render-core class, and reject nested JARs.
