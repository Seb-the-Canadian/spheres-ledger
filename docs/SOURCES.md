# Sources

The source policy: what counts as evidence, and what `data/sources.csv` must
hold.

---

## Purpose

To keep the ledger:

- verifiable;
- auditable;
- resistant to rumour and misinformation;
- fit for comparing one time window with another.

---

## Source tiers

### Tier 1 (preferred)

Use as the main support for the facts of an event.

- Primary legal and institutional documents: from government departments,
  regulators, official gazettes and registers, and the councils and
  commissions of regional blocs.
- Major international wire services and widely recognised outlets of record.

### Tier 2 (supporting)

Use to add context or to cross-check, not as the only evidence for a major
claim.

- Reputable think tanks, academic publications, international financial
  institutions, major non-governmental organisations, datasets.

### Tier 3 (avoid unless there is no other way)

- Blogs, anonymous social media posts, partisan outlets, unverified claims.

---

## Minimum evidence

### For every event

- It must have `source_key_1`.
- `source_key_1` must exist as a row in `data/sources.csv`.

### For high-impact claims

For example:

- strikes against a capital city;
- the capture or seizure of a head of state;
- claims of annexation;
- major shifts in a legal or policy regime with geopolitical consequences.

Requirements:

- Prefer at least two independent Tier 1 sources (`source_key_1` and
  `source_key_2`), **or** one Tier 1 source plus a primary document where one
  exists.
- If only one Tier 1 source is available, state the limits in `notes`.

---

## Attribution

- Write neutral summaries.
- Attribute contested claims to whoever made them: the outlet that reported
  them or the official statement. For example:
  - "Outlet A reports X…"
  - "The official statement claims Y…"

Do not turn a reported claim into a stated fact unless it is corroborated.

---

## Rules for `sources.csv`

Every `source_key` used in `data/events.csv` must have a row in
`data/sources.csv`.

Required fields:

- `source_key` (unique)
- `publisher`
- `doc_type` (`news`, `primary`, `primary+news`, `dataset` or `other`)
- `title_or_description`
- `pub_date`
- `url_or_citation_note`

`url_or_citation_note` must be stable and enough to find the source again. If
there is no URL, give a clear note on where to find it. (The example data in
this repository uses invented sources at `example.org`.)

---

## Reproducibility

For each event, someone else should be able to:

1. look up `source_key_1` in `sources.csv`;
2. retrieve the source using `url_or_citation_note`;
3. check the event's description and the basis for its date.

If that cannot be done, mark the event, then either strengthen its sources or
remove it.

---

## When sources disagree

If Tier 1 sources disagree:

- keep a single event row only if the core action is undisputed, and record the
  differences in `notes`; **or**
- create separate rows if the disagreement changes the mechanism or the sphere.

Never merge contradictions silently.

---

## Institutions as controllers

By default, controllers are **states**.

If **institutions** are included (for example, a bloc acting as an institution,
a national export-control agency, or a standing body of an international
organisation), they must be:

- typed consistently (`actor_type` = `institution`);
- named consistently;
- explicitly allowed by a project decision.
