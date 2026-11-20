# Validation rules

Every rule the ledger keeps, and what enforces it:

- **Schema:** `frictionless validate datapackage.json` (structure: columns,
  types, allowed values, keys, links between tables)
- **Checker:** `python3 scripts/validate_rules.py data` (the ledger's own
  rules). An `ERROR` fails the check; a `WARN` asks a person to look.
- **Person:** judgement no check can make. A reviewer reads for these on
  every change.

A passing check means the data keeps the rules. It does not mean the claims
are right: that is what sources, review and challenge are for.

## A. Files and columns

| Id | Rule | Enforced by |
|---|---|---|
| A1 | The seven tables exist in `data/`: windows, instruments, threads, sources, events, edges, register | Schema |
| A2 | Each table's columns match `datapackage.json` and `DATA_DICTIONARY.md` | Schema |

## B. Identifiers and links

| Id | Rule | Enforced by |
|---|---|---|
| B1 | `event_id` is unique (`E####`) | Schema |
| B2 | `role_edge_id` is unique (`R####`) | Schema |
| B3 | Every id in an edge's `evidence_event_ids`, and in a register row's `promotion_basis_event_ids`, exists in events | Checker (ERROR) |
| B4 | Every event's `source_key_1`, and `source_key_2` and `primary_doc_key` when set, exists in sources | Schema |
| B5 | Every id in an event's `thread_ids` exists in threads | Checker (ERROR) |
| B6 | Every `window_id` (events, edges) and every register window exists in windows | Schema |

## C. Controlled vocabulary

| Id | Rule | Enforced by |
|---|---|---|
| C1 | An event's `instrument_family` and `instrument_class` together appear in `instruments.csv` | Schema |
| C2 | No new instrument class appears in an event alone: add it to `instruments.csv` and `INSTRUMENTS.md`, and note it in the changelog | Schema (for the event) and Person (for the docs) |
| C3 | `thread_ids` is blank or pipe-separated ids (`T01`, `T01\|T02`); no spaces or other separators | Schema |
| C4 | Spheres, roles, statuses, confidence levels, entity types and the other listed values are only the allowed ones | Schema |

## D. Time fields

| Id | Rule | Enforced by |
|---|---|---|
| D1 | Every event has `pub_date`. A blank `event_date` needs a reason in `notes` | Schema (`pub_date`) and Checker (ERROR) |
| D2 | A filled `event_date` needs `event_date_confidence` and `event_date_basis` | Checker (ERROR) |
| D3 | `event_date` falls inside its window, inclusive. When `event_date` is blank, `pub_date` places the event and `event_date_confidence` must be `Low` | Checker (ERROR) |
| W1 | Windows have start on or before end, and don't overlap. "Earlier" and "later" always mean by date, not by id | Checker (ERROR) |

## E. Entity scoping

| Id | Rule | Enforced by |
|---|---|---|
| E1 | Every event names `resident_entity_type` and `resident_entity_name`. A non-state resident names its `resident_parent_state` when it is clearly tied to one; if it is left blank, `notes` says why | Schema (the first two) and Checker (WARN) |
| E2 | An edge's `resident` and `resident_entity_type` match at least one of its evidence events | Checker (ERROR) |
| E4 | Every edge's evidence events are in the edge's sphere, and on or before the end of the edge's window | Checker (ERROR) |
| E3 | No state-level overreach: an edge claims a whole state as resident only when at least one evidence event is scoped to that state | Checker (ERROR) |

## P and F. Promotion and the register

| Id | Rule | Enforced by |
|---|---|---|
| P1 | An edge with `role = controller` has `proof_C1`, `proof_C2` and `proof_C3` all `1`, and names evidence events | Checker (ERROR) |
| P2 | Each proof rests on what the evidence events actually show, not on how the edge is labelled | Person |
| F1 | A register row with `status = controller` has `promoted_window` and `promotion_basis_event_ids`, and an edge for that controller and sphere with all three proofs cites at least one of those events | Checker (ERROR) |
| F2 | `candidate` is used where C1 is evidenced but C2 or C3 is not. A candidate whose edge already meets all three tests is flagged for a person to decide | Checker (WARN) and Person |
| F3 | `contested` follows a promotion (it has `promoted_window` and basis events). It's used when a later window shows compliance weakening or the effect fading, with the events and a note that show it | Checker (ERROR) and Person |

## G. Sources

| Id | Rule | Enforced by |
|---|---|---|
| G1 | High-impact events (force, leadership capture, annexation claims, major regime shifts) have two strong sources, or one plus a primary document; with only one, `notes` says so | Person |
| G2 | Every source has publisher, doc_type, title or description, pub_date, and a stable locator | Schema |

## H. Writing

| Id | Rule | Enforced by |
|---|---|---|
| H1 | Observable flags O1–O5 are `0` or `1` | Schema |
| H2 | `summary` is neutral. `notes` explains ambiguity, inference or scope limits, and speculation is never unattributed | Person |
| H3 | A suggestion from an AI or any other tool becomes an event only after a person has checked it against a source | Person |

## Before a change is merged

- The schema check, the rules checker and the tests all pass.
- Every `WARN` has been read and either fixed or explained.
- A person has read the change for the rules marked **Person**.
