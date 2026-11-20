# Entity scoping

Rules for telling a whole state apart from a firm, an asset or a sector, so that
a claim about who controls whom never reaches further than its evidence.

All names in the examples below (Controller X, Resident Y, Firm Q, Sector S,
Parent State P) are invented placeholders.

---

## Purpose

To avoid false generalisation, such as treating a constraint on one firm's
asset as if a whole state were a resident.

Every edge must match the scope of its evidence.

---

## Resident entity types

`resident_entity_type` must be exactly one of:

| Value | Meaning | Example |
|---|---|---|
| `state` | A sovereign state is directly constrained. | Resident Y |
| `firm` | A specific company is constrained, not necessarily its whole state. | Firm Q |
| `sector` | A sector or category is constrained. | Sector S: exporters of one metal to Controller X |
| `state_via_firm_asset` | An asset of a firm linked to a state is constrained. This is not residency of the whole state. | Firm Q's plant (tool imports) |

---

## Required fields by entity type

### When `resident_entity_type` is `state`

- `resident_entity_name` is the state's name, for example "Resident Y".
- `resident_parent_state` is blank.

### When `resident_entity_type` is not `state`

- `resident_entity_name` must name a specific object a person can recognise,
  for example "Firm Q's plant (tool imports under an annual Controller X
  licence)".
- `resident_parent_state` must be filled in if the entity is clearly tied to a
  state (for example, Parent State P for Firm Q's plant). Otherwise leave it
  blank and say why in `notes`. A blank here is a warning, not an error.

---

## Building an edge from events

When you create a row in `data/edges.csv`:

- `resident` must equal the evidence event's `resident_entity_name`, unless that
  event is itself scoped to a state.
- `resident_entity_type` and `resident_parent_state` on the edge must match the
  event row used as evidence.

Do not widen a scoped resident into a state unless you have separate evidence
scoped to the state.

---

## When widening to the state is allowed

You may treat a scoped constraint as residency of the whole state only if there
is explicit evidence that the constraint:

- applies broadly to the state, not just to one firm or asset, **or**
- creates dependence or constraint at national level across several firms or
  sectors,

**and** you can link at least one event scoped to the state as evidence.

At a minimum:

- add a new event row with `resident_entity_type` = `state`;
- create a matching edge that cites that event.

---

## Common mistakes

- **Widening one asset into a state.** Writing "Controller X controls Parent
  State P" when the evidence is a licence covering only Firm Q's plant, which
  sits in another state.
  Correct: "Controller X controls tool access to Firm Q's plant (an asset
  linked to Parent State P)."

- **Treating a sector as a country.**
  Correct: keep "Exporters of two metals to Controller X" (Sector S) scoped to
  the sector, unless a specific state is explicitly targeted and evidenced.

- **Mixing scopes in one resident label.** If several entities are
  constrained, create several events and edges, or use one sector label
  consistently.

---

## Naming conventions

For `resident_entity_name`:

| Type | Pattern | Example |
|---|---|---|
| `state` | The state's name | "Resident Y" |
| `firm` | The company's name | "Firm Q" |
| `sector` | Who is constrained, and where | "Exporters of one metal to Controller X" |
| `state_via_firm_asset` | "FirmName AssetName (constraint mechanism)" | "Firm Q's plant (tool imports under an annual Controller X licence)" |

Add the mechanism in brackets when it makes the scope clearer.

---

## Institutions as controllers, and the Legitimacy sphere (S6)

By default, controllers are states. An institution (for example, the permanent
members of a security council acting together) may be a controller only where a
project decision explicitly allows it. It must then be shown consistently in
the `actor_type` and `controller` columns.

In `S6_Legitimacy`:

- The **target** of a recognition act may be typed `institution`, for example
  a contested government or a government in exile (`Resident_Y_government`).
  That is separate from the resident, which stays the affected **state**
  (Resident Y).
- `target_type` = `institution` is valid in S6 when the recognition act is
  aimed at a governing body rather than at the state itself.
- The **resident** on an S6 edge is usually the state whose access to
  international systems is affected, not the institution that the recognition
  act was aimed at.
