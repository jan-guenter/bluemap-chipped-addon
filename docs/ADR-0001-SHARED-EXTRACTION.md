# ADR 0001: keep the Athena interpreter private for this release

Status: accepted for the initial Chipped candidate.

## Required extraction review

1. **Which code resembles an existing component?** Exact artifact/profile
   gates, reversible emission, face-neighbor sampling, diagnostics, CI, and
   release mechanics resemble the owner's existing BlueMap add-ons.
2. **Semantic or vocabulary?** Failure boundaries and deployment mechanics are
   semantically shared. Athena texture selection and geometry are a distinct
   renderer-format interpreter; terms such as CTM and pane are only vocabulary
   shared with Chisel CTM and Rechiseled Fusion.
3. **Same invariants and failures?** The neutral adapter/fallback patterns do.
   No second implementation yet has Athena 4.0.6's exact masks, pillar order,
   pane rules, coordinate phase, and schema gate.
4. **Third named consumer?** A future Athena-using mod could consume the
   interpreter, but none is yet scoped and proven. Chisel and Rechiseled would
   become more complex if forced through it.
5. **Extraction hazards?** A runtime provider would add an unversioned
   classloader dependency. Generalization would invite format conditionals;
   moving Chipped-derived assets or code would contaminate the MIT boundary.
6. **Decision?** Retain neutral specifications and test patterns, keep all
   production source private to this repository, and create no installed
   runtime. Revisit shared source only after a second independent Athena
   implementation and a concrete third consumer satisfy the portfolio gate.
