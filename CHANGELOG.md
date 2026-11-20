# Changelog

Every release says what changed, why, and what it affects. Versions follow
the rules in the README: patch for wording, minor for changes valid data
still passes, major for anything that makes valid data invalid.

## v1.0.0 — 2026-11-20

The first public version.

### What it is
- The schema as a Frictionless Data Package (`datapackage.json`) with seven
  tables: `windows`, `instruments`, `threads`, `sources`, `events`, `edges`
  and `register`.
- A rules checker (`scripts/validate_rules.py`) for what a table schema can't
  express: the promotion test, contested status, entity scoping, dates and
  windows. Each rule has a test that breaks it.
- The method docs, invented example data, and a GitHub check that runs all
  of it on every change.

### Where it came from
A private working ledger (v0.5). v1 states its
rules as its docs mean them, with these choices:
- An edge's `role` describes the controller side only: `candidate`,
  `controller` or `contested`. The private ledger's `mixed` and `resident`
  roles had no written definition and are not part of v1.
- Spheres are always written as labels (`S1_Security` … `S6_Legitimacy`).
- `region` and `source_reliability` are optional event columns.
- The bilateral-relationship and middle-power tables, and the derived
  resident profiles, are not in v1.

### Next
Apply v1 to real cases, and let what that shows become v1.1.
