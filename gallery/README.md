# Chipped staging gallery

This deterministic datapack provides two deliberately different layers:

- 1,427 isolated, two-block-spaced swatches—one for every exact routed ID;
- 70 structural cases covering every loader family, CTM truth classes and
  face bases, opaque/transparent/wool materials, all pillar axes, positive and
  negative giant phases, carpets beside carpets/full cubes, and both pane
  engines including exact and differing vertical stacks.

Run `python3 gallery/generate.py --check`, package with
`gallery/package.sh <output.zip>`, then use:

```text
/function chipped_gallery:build
/function chipped_gallery:verify
/function chipped_gallery:pose
/function chipped_gallery:release
```

The verifier is also the exact server registry/placement census: every routed
block must place and persist, all generated structural placements must match,
and `#failures chipped_gallery` must be zero. The datapack contains only IDs,
coordinates, commands, and metadata; it bundles no Chipped/Athena asset.
