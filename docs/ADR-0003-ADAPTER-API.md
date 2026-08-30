# ADR 0003: source-bundle the adapter API

Status: accepted for the `0.1.0-alpha.4` candidate.

## Decision

Compile the four classes in `bluemap-addon-adapter-api` from the exact pinned
source tree. Remove Chipped's local runtime compatibility and resource
extension wrapper classes. Replace its inline registry guard and synthetic
dispatch checks with the shared implementations. Do not install or nest the
module JAR.

Chipped accepts only the exact 5.23 feature-backport runtime identity audited
by the module. Its renderer instance, resource extension factory,
registry-collision failure, route state, profile checks, and stock fallback
remain local.

The settings preflight checks the committed and indexed gitlink, checkout
HEAD, source-tree hash, and clean worktree. Archive gates require one copy of
each selected shared class and source. They reject the removed local classes,
every unexpected class under the shared package, and nested JARs.
