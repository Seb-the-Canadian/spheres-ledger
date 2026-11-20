# Spheres ledger

A schema for reading power sphere by sphere: **who can constrain whom, in
which domain, and on what evidence.**

Spheres of influence used to be regions on a map. Today control travels
through finance, trade, shipping, chips, platforms and recognition, often
with no shared border at all. The spheres ledger is a small information
architecture for recording that: six spheres, two roles, tests a claim has
to pass before it counts, and a trail from every claim back to its sources.

It is a measurement structure, not a set of findings. **All data in this
repository is invented**, to show the structure. The story behind it is in
[Reading power, sphere by sphere](https://sebthecanadian.ca/writing/reading-power-sphere-by-sphere/).

## The model

**Six spheres.** They overlap; the same two actors can meet in several of
them on different terms.

| Sphere | Covers |
|---|---|
| `S1_Security` | Force, basing and access, security assistance |
| `S2_Finance` | Sanctions, investment and ownership permissions |
| `S3_Trade` | Tariffs, quotas, border enforcement, trade remedies |
| `S4_Energy_Logistics` | Shipping, insurance, ports, energy supply and pricing |
| `S5_Tech_Compute` | Export controls, licensing, chips and tools, cloud and platform access |
| `S6_Legitimacy` | Recognition, binding multilateral action, diplomatic standing |

**Two roles, joined by an edge.** A *controller* constrains a *resident*
inside one sphere. Each edge is its own claim, with its own evidence.

**A controller is earned, not asserted.** All three must hold, each backed
by linked events:

- **C1, imposition:** an enforceable rule or action was applied.
- **C2, compliance capture:** third parties (banks, shippers, vendors,
  allies) changed what they did because of it.
- **C3, net effect:** a measurable cost or constraint, or a strong sign of one.

Fewer than three, and it stays a **candidate**. A controller whose hold
weakens in a later window is **contested**.

**A resident is scoped, not generalised.** It depends on a channel the
controller holds (R1), felt the constraint during an event (R2), and would
find it slow or costly to route around (R3). A resident can be a state, a
firm, a sector, or a state reached through one firm's asset, and the ledger
keeps those apart rather than stretching a claim about a company into a
claim about a nation.

**Every claim has a trail.**

```
sources ──▶ events ──▶ edges ──▶ register
documented   recorded    judged     kept
```

A suggestion from an AI or any other tool is only a suggestion. A person
checks it against a source before it becomes an event, and a person decides
every edge and every promotion. The checks here refuse what breaks the rules.
They never promote anything.

## What's here

| Path | What it is |
|---|---|
| `datapackage.json` | The schema, as a [Frictionless Data Package](https://specs.frictionlessdata.io/): every table, column, allowed value and link between tables |
| `data/` | Seven tables as CSV: `windows`, `instruments`, `threads`, `sources`, `events`, `edges`, `register`. **Invented example data.** |
| `scripts/validate_rules.py` | Checks the ledger's own rules, which a table schema can't express |
| `tests/` | Tests for the rules checker: each rule is broken on purpose and must be caught |
| `docs/` | The method: data dictionary, instruments, time fields, entity scoping, sources policy, validation rules |

## Run the checks

You need Python 3.10 or later.

Install the schema checker:

```bash
pip install -r requirements.txt
```

Check the structure (types, allowed values, keys, links between tables):

```bash
frictionless validate datapackage.json
```

Check the ledger's rules (promotion, scoping, dates and windows):

```bash
python3 scripts/validate_rules.py data
```

Run the tests:

```bash
python3 -m unittest
```

The same three checks run on GitHub for every push and pull request.
[`docs/VALIDATION_RULES.md`](docs/VALIDATION_RULES.md) lists every rule and
says what enforces it: the schema, the rules checker, or a person.

## Propose a change, or challenge a rule

The ledger is meant to be argued with. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Versions

The schema is versioned like software, and every release says what changed
and why in [CHANGELOG.md](CHANGELOG.md).

- **Patch** (1.0.x): wording and docs.
- **Minor** (1.x.0): new optional columns or rules that valid data still passes.
- **Major** (x.0.0): anything that makes valid data invalid.

v1.0.0 is the first public version. Later versions record what applying it
taught.

## Licence

- **Code** (`scripts/`, `tests/`, `.github/`): MIT, see [LICENSE](LICENSE).
- **Documents, schema and data:** CC BY 4.0, see
  [LICENSE-DOCS-DATA.md](LICENSE-DOCS-DATA.md).

Maintained by Seb Lathangue, for the
[Cognitive Architecture Collaborative](https://cognitivearchitecture.ca/Home).
