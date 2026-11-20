#!/usr/bin/env python3
"""Check the spheres ledger's own rules.

datapackage.json (checked with `frictionless validate datapackage.json`)
covers structure: columns, types, allowed values, keys and links between
tables. This script covers the rules a table schema can't express. Rule ids
follow docs/VALIDATION_RULES.md.

Usage:  python3 scripts/validate_rules.py [data_dir]
Prints one line per problem and exits 1 if any is an ERROR.
Standard library only; Python 3.10+.
"""

from __future__ import annotations

import csv
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path


@dataclass(frozen=True)
class Problem:
    severity: str  # "ERROR" or "WARN"
    rule: str
    where: str
    message: str

    def __str__(self) -> str:
        return f"{self.severity} {self.rule} {self.where}: {self.message}"


def _read(data_dir: Path, name: str) -> list[dict[str, str]]:
    with open(data_dir / f"{name}.csv", newline="", encoding="utf-8") as f:
        return [{k: (v or "").strip() for k, v in row.items()} for row in csv.DictReader(f)]


def _ids(value: str) -> list[str]:
    return [x.strip() for x in value.split("|") if x.strip()]


def _date(value: str) -> date | None:
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def _all_proofs(edge: dict[str, str]) -> bool:
    return all(edge.get(f"proof_C{i}") == "1" for i in (1, 2, 3))


def validate(data_dir: str | Path) -> list[Problem]:
    d = Path(data_dir)
    windows = _read(d, "windows")
    threads = _read(d, "threads")
    events = _read(d, "events")
    edges = _read(d, "edges")
    register = _read(d, "register")

    out: list[Problem] = []

    def err(rule, where, msg):
        out.append(Problem("ERROR", rule, where, msg))

    def warn(rule, where, msg):
        out.append(Problem("WARN", rule, where, msg))

    # Windows: dates, and no overlaps. "Earlier" is always by date.
    win = {}
    for w in windows:
        s, e = _date(w["start_date"]), _date(w["end_date"])
        where = f"windows.csv {w['window_id']}"
        if not s or not e or s > e:
            err("W1", where, "start_date and end_date must be dates with start on or before end")
            continue
        win[w["window_id"]] = (s, e)
    spans = sorted((s, e, k) for k, (s, e) in win.items())
    for (s1, e1, k1), (s2, e2, k2) in zip(spans, spans[1:]):
        if s2 <= e1:
            err("W1", f"windows.csv {k1}/{k2}", "windows overlap")

    ev = {e["event_id"]: e for e in events}
    thread_ids = {t["thread_id"] for t in threads}

    def event_day(e):
        return _date(e["event_date"]) or _date(e["pub_date"])

    # Events
    for e in events:
        where = f"events.csv {e['event_id']}"
        for t in _ids(e.get("thread_ids", "")):
            if t not in thread_ids:
                err("B5", where, f"thread_ids names {t}, which is not in threads.csv")
        if not e["event_date"]:
            if not e["notes"]:
                err("D1", where, "event_date is blank, so notes must say why")
            if e["event_date_confidence"] != "Low":
                err("D3", where, "event_date is blank, so the window rests on pub_date and event_date_confidence must be Low")
        else:
            if not e["event_date_confidence"] or not e["event_date_basis"]:
                err("D2", where, "event_date is set, so event_date_confidence and event_date_basis are required")
        day = event_day(e)
        span = win.get(e["window_id"])
        if day and span and not (span[0] <= day <= span[1]):
            err("D3", where, f"{'event_date' if e['event_date'] else 'pub_date'} {day} is outside window {e['window_id']} ({span[0]} to {span[1]})")
        if e["resident_entity_type"] != "state" and not e["resident_parent_state"] and not e["notes"]:
            warn("E1", where, "a non-state resident with no resident_parent_state should say why in notes")

    # Edges
    for g in edges:
        where = f"edges.csv {g['role_edge_id']}"
        cited = _ids(g["evidence_event_ids"])
        missing = [i for i in cited if i not in ev]
        for i in missing:
            err("B3", where, f"evidence_event_ids names {i}, which is not in events.csv")
        found = [ev[i] for i in cited if i in ev]
        if found and not any(
            x["resident_entity_name"] == g["resident"] and x["resident_entity_type"] == g["resident_entity_type"] for x in found
        ):
            err("E2", where, "resident and resident_entity_type match none of the evidence events")
        if g["resident_entity_type"] == "state" and found and not any(x["resident_entity_type"] == "state" for x in found):
            err("E3", where, "claims a whole state as resident, but every evidence event is scoped to a firm, sector or asset")
        span = win.get(g["window_id"])
        for x in found:
            if x["sphere"] != g["sphere"]:
                err("E4", where, f"evidence event {x['event_id']} is in {x['sphere']}, not {g['sphere']}")
            day = event_day(x)
            if span and day and day > span[1]:
                err("E4", where, f"evidence event {x['event_id']} ({day}) is after window {g['window_id']} ends ({span[1]})")
        if g["role"] == "controller":
            if not _all_proofs(g):
                err("P1", where, "role is controller, so proof_C1, proof_C2 and proof_C3 must all be 1")
            if not cited:
                err("P1", where, "role is controller, so evidence_event_ids must name at least one event")

    # Register
    for r in register:
        where = f"register.csv {r['controller']} {r['sphere']}"
        basis = _ids(r["promotion_basis_event_ids"])
        for i in basis:
            if i not in ev:
                err("B3", where, f"promotion_basis_event_ids names {i}, which is not in events.csv")
        qualifying = [
            g for g in edges
            if g["controller"] == r["controller"] and g["sphere"] == r["sphere"] and g["role"] == "controller" and _all_proofs(g)
        ]
        if r["status"] == "controller":
            if not r["promoted_window"] or not basis:
                err("F1", where, "status is controller, so promoted_window and promotion_basis_event_ids are required")
            if not any(set(_ids(g["evidence_event_ids"])) & set(basis) for g in qualifying):
                err("F1", where, "no controller edge with all three proofs cites the promotion basis events")
        elif r["status"] == "candidate":
            if qualifying:
                warn("F2", where, f"status is candidate, but {qualifying[0]['role_edge_id']} meets all three tests")
        elif r["status"] == "contested":
            if not r["promoted_window"] or not basis:
                err("F3", where, "contested follows a promotion, so promoted_window and promotion_basis_event_ids are required")

    return out


def main(argv: list[str]) -> int:
    data_dir = Path(argv[1]) if len(argv) > 1 else Path(__file__).resolve().parent.parent / "data"
    problems = validate(data_dir)
    for p in problems:
        print(p)
    errors = sum(p.severity == "ERROR" for p in problems)
    warnings = len(problems) - errors
    print(f"{errors} error(s), {warnings} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
