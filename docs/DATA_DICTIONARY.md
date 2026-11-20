# Data dictionary

This document defines every table in `data/`: what each column means, which
values it allows, and which columns are required.

The ledger has seven tables, each a plain CSV file:

| File | What a row is |
|---|---|
| `data/windows.csv` | A time window |
| `data/instruments.csv` | One instrument in the fixed vocabulary |
| `data/threads.csv` | A cross-sphere context label |
| `data/sources.csv` | A documented source |
| `data/events.csv` | A recorded event |
| `data/edges.csv` | A controller → resident claim in one sphere and window |
| `data/register.csv` | The status of one controller in one sphere |

The rules that check these tables, and what enforces each one, are in
`VALIDATION_RULES.md`.

---

## Global conventions

- **Primary keys.** `window_id`, `source_key`, `thread_id`, `event_id` and
  `role_edge_id` are each unique in their table. An instrument is identified by
  its `instrument_family` and `instrument_class` together. A register row is
  identified by its `controller` and `sphere` together.
- **Blanks.** A blank cell means unknown or not applicable. Never invent a
  value to fill it.
- **Lists.** Where a cell holds several values, they are separated by a pipe
  (`|`) with no spaces and no quotes, for example `E0001|E0002`.
- **Dates.** Dates are `YYYY-MM-DD`.
- **Windows and dates.** An event belongs to a window by its `event_date`, or by
  its `pub_date` when `event_date` is blank. See `TIME_FIELDS_RULES.md`.
- **"Earlier" and "later".** When a rule says one window is earlier or later
  than another, it always means by date (`start_date`), never by window id.
  Window ids are labels and need not be in date order.
- **Evidence.** Every event has `source_key_1`. High-impact events should also
  have `source_key_2` where feasible. See `SOURCES.md`.

---

## Spheres

A sphere is a domain in which one actor can constrain another. Each sphere is
judged on its own, and spheres may overlap.

The `sphere` value is always the full label below, never the bare code (`S1`).
This applies everywhere a sphere appears: `events.sphere`, `edges.sphere`,
`register.sphere`, `instruments.default_sphere` and `threads.spheres_involved`.

| Value | Name | Covers |
|---|---|---|
| `S1_Security` | Security | Force, coercive presence, basing and transit, security assistance |
| `S2_Finance` | Finance | Sanctions, and permission over investment and ownership (payment rails may be added later) |
| `S3_Trade` | Trade | Tariffs, quotas, border enforcement, trade remedies |
| `S4_Energy_Logistics` | Energy and Logistics | Oil and gas services, shipping and insurance, ports, interdiction, price caps |
| `S5_Tech_Compute` | Tech and Compute | Export controls, licensing, chips and tools, cloud and platform access |
| `S6_Legitimacy` | Legitimacy and Diplomatic | Binding UN Security Council action, recognition, bloc alignment. By default only states are controllers here, unless a project decision explicitly says otherwise |

---

## The two roles and their tests

The ledger measures two roles in each sphere.

**A controller** in a sphere is an actor (usually a state) that can impose
constraints there and get others to comply. An actor is promoted to controller
in sphere S only if the evidence supports all three tests:

- **C1 Imposition:** an enforceable action or rule was applied.
- **C2 Compliance capture:** third parties changed their behaviour (banks,
  shippers, vendors, importers, allies).
- **C3 Net effect:** a measurable added cost or constraint, or a strong
  behavioural proxy for one.

No promotion without all three, with linked evidence.

**A resident** in sphere S, relative to controller X, is a state or a scoped
entity that is materially constrained there. It is classed by three tests:

- **R1 Dependence:** it relies on a channel X controls, with few substitutes.
- **R2 Episode evidence:** constraint effects were observed during one or more
  events.
- **R3 Switching costs:** routing around X is slow or expensive.

Residency can be scoped: a firm, a sector, or a state reached through a firm's
asset, rather than a whole state. See `ENTITY_SCOPING_RULES.md`.

### How the edges table records the two roles

Each row of `edges.csv` is one claim: *this controller* constrains *this
resident* in *this sphere* during *this window*.

The `role` column describes **the controller side of that claim only**, and
takes one of three values: `candidate`, `controller` or `contested`.

### The three statuses

The same three values are used for `role` in `edges.csv` and `status` in
`register.csv`:

| Value | Use it when |
|---|---|
| `candidate` | C1 Imposition is evidenced, but C2 Compliance capture or C3 Net effect is not. |
| `controller` | C1, C2 and C3 are all evidenced, with the supporting events linked. |
| `contested` | The actor was promoted earlier, and later windows show compliance capture weakening or net effects shrinking because the constraint is cheap to get around. Contestation needs explicit evidence event ids and notes. |

### No resident role

There is no `resident` role value and no `mixed` value. The resident side of
the claim is not a role label; it is described by the resident columns on the
same row (`resident`, `resident_entity_type`, `resident_parent_state`) and
judged against R1–R3, using the events listed in `evidence_event_ids`.

---

## Observable flags (O1–O5)

Each event carries five coarse yes/no flags for what the evidence shows. They
make filtering quick and feed the promotion tests.

| Flag | Meaning | Example |
|---|---|---|
| `observable_O1` | Capability: the instrument exists; the action is feasible and initiated | |
| `observable_O2` | Enactment: the policy was enacted, the strike occurred, the interdiction was carried out | |
| `observable_O3` | Stated objective: the intent is stated explicitly | deterrence, cutting revenue, gating a capability |
| `observable_O4` | Compliance capture: third parties adjust their behaviour | insurers, shippers, vendors, importers |
| `observable_O5` | Net effect: measurable outcomes or strong proxies | exports down, prices spike, access denied |

Each flag is `0` or `1`. Flags are conservative: if unsure, use `0` and explain
in `notes`.

---

## `data/windows.csv`

Defines the time windows that events are grouped into.

| Column | Required | Meaning and allowed values |
|---|---|---|
| `window_id` | Yes | Unique id, for example `W1`. A label only: it does not show date order. |
| `start_date` | Yes | First day of the window, `YYYY-MM-DD`, inclusive. |
| `end_date` | Yes | Last day of the window, `YYYY-MM-DD`, inclusive. |
| `notes` | No | Free text, such as what the window focuses on. |

---

## `data/instruments.csv`

The fixed vocabulary of instruments: the mechanisms an actor uses. Each event
picks exactly one instrument from this table. The full list, with design and
change rules, is in `INSTRUMENTS.md`.

| Column | Required | Meaning and allowed values |
|---|---|---|
| `instrument_family` | Yes | The broad bucket, for example `F4 sanctions_financial`. |
| `instrument_class` | Yes | The precise mechanism within the family, for example `sanctions_designation`. Family and class together are unique. |
| `default_sphere` | Yes | The sphere this instrument usually belongs to, as a sphere label (for example `S2_Finance`). A convenience only: each event still chooses its own sphere. |
| `definition` | Yes | A short definition of the mechanism. |
| `notes` | No | Free text. |

---

## `data/threads.csv`

Cross-sphere context labels. A thread marks events that belong to the same
wider campaign, across spheres.

| Column | Required | Meaning and allowed values |
|---|---|---|
| `thread_id` | Yes | Unique id, `T` plus two digits, for example `T01`. |
| `name` | Yes | Short machine-readable label in `snake_case`. |
| `description` | Yes | A summary of the campaign the thread follows. |
| `spheres_involved` | Yes | Sphere labels, pipe-separated, for example `S1_Security|S4_Energy_Logistics|S6_Legitimacy`. |
| `windows_active` | Yes | Window ids in which the thread is active, pipe-separated, for example `W1|W4`. |
| `notes` | No | Free text. |

Constraints:

- Which events belong to a thread is a judgement call. It does not affect how
  C1, C2 or C3 are judged for any event.
- Threads never create edges and never override the promotion rule.
- Every id in an event's `thread_ids` must exist in this table. Add the thread
  here first.

---

## `data/sources.csv`

The index of every source the events cite. Every `source_key` used in
`events.csv` must have a row here. See `SOURCES.md` for the source policy.

| Column | Required | Meaning and allowed values |
|---|---|---|
| `source_key` | Yes | Unique key for the source. |
| `publisher` | Yes | Who published it. |
| `doc_type` | Yes | One of `news`, `primary`, `primary+news`, `dataset`, `other`. |
| `title_or_description` | Yes | The title, or a description if there is no title. |
| `pub_date` | Yes | Publication date, `YYYY-MM-DD`. |
| `url_or_citation_note` | Yes | A stable locator: a URL if there is one, otherwise a note clear enough to find the source again. |

---

## `data/events.csv`

The fact table: one row per event. Columns are listed in file order.

| Column | Required | Meaning and allowed values |
|---|---|---|
| `event_id` | Yes | Stable unique id, `E` plus four digits, for example `E0001`. |
| `window_id` | Yes | The window the event belongs to. Must exist in `windows.csv`. See `TIME_FIELDS_RULES.md`. |
| `event_date` | When known | When the event happened, `YYYY-MM-DD`. Prefer dates stated in the sources. Leave blank only when genuinely unknown, and explain in `notes`. |
| `event_date_confidence` | Yes | `High`, `Med` or `Low`. Must be `Low` when `event_date` is blank. |
| `event_date_basis` | Yes | `explicit_in_report`, `inferred_from_weekday`, `primary_doc_effective_date` or `other`. Must be `other` when `event_date` is blank. |
| `pub_date` | Yes | When the source was published, `YYYY-MM-DD`. |
| `source_pub_datetime_utc` | No | Exact publication time in ISO 8601 UTC, for example `2026-01-03T23:15:00Z`, when it matters. |
| `sphere` | Yes | One sphere label, for example `S3_Trade`. |
| `instrument_family` | Yes | From `instruments.csv`. |
| `instrument_class` | Yes | From `instruments.csv`; the family and class pair must exist there. |
| `actor` | Yes | The entity that took the action: a state, or an institution where allowed. |
| `actor_type` | Yes | `state`, `institution` or `other`. |
| `target` | Yes | What the action was aimed at: a state, sector, asset or policy object. |
| `target_type` | Yes | `state`, `sector`, `asset`, `policy` or `other`. In S6, `institution` is also valid when a recognition act is aimed at a governing body rather than the state (see `ENTITY_SCOPING_RULES.md`). |
| `region` | No | Where the constraint is felt. See [`region`](#region) below. |
| `resident_entity_type` | Yes | `state`, `firm`, `sector` or `state_via_firm_asset`. See `ENTITY_SCOPING_RULES.md`. |
| `resident_entity_name` | Yes | A human-readable name for the constrained entity, at the scope the evidence supports. |
| `resident_parent_state` | Conditional | Blank when `resident_entity_type` is `state`. Otherwise, fill it when the entity is clearly tied to a state; if it is not, or the tie is genuinely unknown, leave it blank and say why in `notes`. A blank here is a warning, not an error. |
| `summary` | Yes | A neutral one- or two-line description of the event. |
| `observable_O1` … `observable_O5` | Yes | `0` or `1` each. See [Observable flags](#observable-flags-o1o5). |
| `source_key_1` | Yes | The main source. Must exist in `sources.csv`. |
| `source_key_2` | No | A second source. If filled, must exist in `sources.csv`. Expected for high-impact events. |
| `source_reliability` | No | The reliability class of `source_key_1`. See [`source_reliability`](#source_reliability) below. |
| `primary_doc_key` | No | The primary document, when it is a different source from `source_key_1`. If filled, must exist in `sources.csv`. |
| `notes` | Conditional | Free text. Required to explain a blank `event_date`, a `Low` date confidence, an `other` date basis, a blank `resident_parent_state` on a non-state resident, a `0` flag you were unsure of, and the limits of a high-impact event with only one strong source. |
| `thread_ids` | No | Ids from `threads.csv`, pipe-separated, for example `T01|T02`. Blank when the event is not part of any thread; a blank does not mean the event has no wider context. |

### `region`

Optional. Where the constraint is felt: the location or main economic exposure
of the target or resident, not of the actor.

| Value | Scope |
|---|---|
| `Americas` | North, Central and South America and the Caribbean |
| `Europe` | All of Europe, inside and outside regional unions; also a state that spans Europe and Asia, when the target faces Europe |
| `East_Asia` | East Asia, including its island and special-status territories |
| `South_Asia` | The South Asian subcontinent and its island states |
| `Southeast_Asia` | Mainland and maritime Southeast Asia |
| `Middle_East` | The Gulf, the Levant and neighbouring states of western Asia |
| `Central_Asia` | The Central Asian states |
| `Africa` | Sub-Saharan and North Africa |
| `Oceania` | Australia, New Zealand and the Pacific islands |
| `Global` | The constraint spans several regions or is genuinely global |

How to assign it:

- Use where the target or resident is physically located or most exposed, not
  where the actor is.
- Firm Q's plant located in East Asia is `East_Asia`, even when Firm Q is
  headquartered in another region.
- A sector spread around the world (Sector S, made up of exporters of one
  commodity from many states, or a fleet of vessels operating across many seas)
  is `Global`.
- A domestic court ruling on a state's own policy takes that state's region: a
  ruling inside a state in the Americas is `Americas`.

### `source_reliability`

Optional. The reliability class of the event's main source.

| Value | Meaning |
|---|---|
| `primary_verified` | A primary government or legal document: a regulation, a court ruling, a sanctions designation notice, an entry in an official gazette or journal |
| `news_major` | A major international wire service, or a specialist publication with strong editorial standards (for example a law firm's sanctions bulletin) |
| `news_regional` | A regional news outlet or a smaller specialist publication |
| `think_tank` | A think tank, academic or analytical publication |
| `leaked_unverified` | Leaked documents or unverified sourcing |
| `aggregated` | An aggregated dataset or secondary compilation |

How to assign it: judge it on `source_key_1`. When the main source is a
government or legal primary document, use `primary_verified` even if news
outlets also reported it. For example, a source that pairs an export-control
agency's rule with its notice in the official gazette is `primary_verified`.

---

## `data/edges.csv`

The edge list: each row claims that a controller constrains a resident in one
sphere during one window. See [How the edges table records the two
roles](#how-the-edges-table-records-the-two-roles).

| Column | Required | Meaning and allowed values |
|---|---|---|
| `role_edge_id` | Yes | Stable unique id, `R` plus four digits, for example `R0001`. |
| `window_id` | Yes | The window the claim applies to. Must exist in `windows.csv`. |
| `sphere` | Yes | One sphere label. |
| `controller` | Yes | The controller side of the claim: usually a state; an institution only where a project decision allows it. Use the same name for the same actor everywhere. |
| `resident` | Yes | The constrained entity, at the same scope as the evidence events. Do not widen it: a firm-scoped event gives a firm-scoped resident. |
| `resident_entity_type` | Yes | `state`, `firm`, `sector` or `state_via_firm_asset`. Must match the evidence event's `resident_entity_type`. |
| `resident_parent_state` | Conditional | As in `events.csv`: blank for a `state` resident; otherwise filled when the resident is clearly tied to a state, else blank, with the reason given in the evidence event's `notes`. Must match the evidence event. A blank on a non-state resident is a warning. |
| `role` | Yes | The controller side only: `candidate`, `controller` or `contested`, with the meanings given under [The three statuses](#the-three-statuses). `controller` needs all three proofs set to `1` and linked evidence. |
| `confidence` | Yes | `High`, `Med` or `Low`. |
| `proof_C1` | Yes | `1` if the evidence shows C1 Imposition, else `0`. |
| `proof_C2` | Yes | `1` if the evidence shows C2 Compliance capture, else `0`. |
| `proof_C3` | Yes | `1` if the evidence shows C3 Net effect, else `0`. |
| `circumvention_notes` | No | A short note on ways around the constraint and what they cost (bears on R3 Switching costs). |
| `evidence_event_ids` | Yes | The supporting events, pipe-separated, for example `E0001|E0004`. Each must exist in `events.csv`, be in the same sphere, and fall in the edge's window or an earlier one. At least one must have the same resident and resident type as the edge. |

---

## `data/register.csv`

The register: one row per controller per sphere, holding its current status
and the windows in which that status changed.

| Column | Required | Meaning and allowed values |
|---|---|---|
| `controller` | Yes | The actor, named as in `edges.csv`. |
| `sphere` | Yes | One sphere label. `controller` and `sphere` together are unique. |
| `status` | Yes | `candidate`, `controller` or `contested`. See [The three statuses](#the-three-statuses). |
| `first_seen_window` | Yes | The window in which the actor first appears as a possible controller in this sphere. Must exist in `windows.csv`. |
| `promoted_window` | Conditional | The window in which the actor was promoted to controller. Required when `status` is `controller` or `contested`. |
| `demoted_window` | No | The window in which a promotion was withdrawn, if it was. |
| `promotion_basis_event_ids` | Conditional | The events the promotion rests on, pipe-separated. Required when `status` is `controller` or `contested`; an edge for this actor and sphere must meet C1, C2 and C3 with linked evidence. |
| `latest_evidence_window` | No | The most recent window with evidence about this actor in this sphere. |
| `confidence` | Yes | `High`, `Med` or `Low`. |
| `notes` | No | Free text. |

All window columns, when filled, must exist in `windows.csv`.
