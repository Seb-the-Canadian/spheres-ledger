# Proposing a change, or challenging a rule

The spheres ledger is meant to be argued with. A rule that can't be
challenged can't be trusted, and "insufficient evidence" is a real answer.

## Two ways in

**Open an issue** if you want to discuss before changing anything. Use one of
the two templates:

- **Challenge a rule:** a rule, a test (C1–C3, R1–R3) or a definition is
  wrong, unclear, or lets something through it shouldn't.
- **Propose a change to the schema:** a new column, an allowed value, an
  instrument class, or a change to a table.

**Open a pull request** if you can show the change. Edit the files, and the
same checks that run here run on your change automatically:

- `frictionless validate datapackage.json`
- `python3 scripts/validate_rules.py data`
- `python3 -m unittest`

On a first contribution, GitHub asks the maintainer to approve the run
before the checks start.

A passing check means the change keeps the rules. It doesn't mean the change
is right. A person reads every proposal and decides.

## What a good challenge includes

- **The rule:** quote it, with its id from
  [`docs/VALIDATION_RULES.md`](docs/VALIDATION_RULES.md) or the section of
  the doc it lives in.
- **The case:** what the rule gets wrong, with an example. Invented examples
  are fine and often clearer.
- **The evidence:** for a claim about the world, a source someone else can
  check: a URL or a full citation.
- **What you'd change it to,** if you know.

## Changing the schema

- A new instrument class goes in `data/instruments.csv` **and**
  `docs/INSTRUMENTS.md`, never in an event alone.
- A new column, allowed value or rule updates `datapackage.json`, the docs
  that describe it, and `CHANGELOG.md`. If it's a new rule for the checker,
  add a test that breaks it.
- Say which kind of version change it is (see the README).

## The data here is invented

`data/` holds invented examples (Controller X, Resident Y, Firm Q…) so the
structure can be shown without making claims about real countries. Please
keep it that way: real cases belong in issues or in your own copy of the
schema, with their sources.

## Decisions

The maintainer, Seb Lathangue, decides what is merged and gives a reason
for every proposal declined.
