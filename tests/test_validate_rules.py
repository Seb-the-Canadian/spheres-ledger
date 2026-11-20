"""Tests for scripts/validate_rules.py.

The example data in data/ is the known-good set: it must pass with no
problems. Every other test copies it, breaks exactly one rule, and checks
that the validator reports that rule, so each rule is shown to be able to
fail. Run with: python3 -m unittest
"""

import csv
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import validate_rules  # noqa: E402


def read(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


class Broken:
    """A temporary copy of data/ that a test can edit."""

    def __enter__(self):
        self.tmp = tempfile.mkdtemp()
        self.dir = Path(self.tmp) / "data"
        shutil.copytree(ROOT / "data", self.dir)
        return self

    def __exit__(self, *exc):
        shutil.rmtree(self.tmp)

    def edit(self, table, key_col, key, **changes):
        path = self.dir / f"{table}.csv"
        rows = read(path)
        hit = [r for r in rows if r[key_col] == key]
        assert hit, f"no {key} in {table}"
        for r in hit:
            r.update({k: str(v) for k, v in changes.items()})
        write(path, rows)

    def problems(self):
        return validate_rules.validate(self.dir)


def rules(problems, severity=None):
    return {p.rule for p in problems if severity is None or p.severity == severity}


class GoodData(unittest.TestCase):
    def test_example_data_passes_with_no_problems(self):
        problems = validate_rules.validate(ROOT / "data")
        self.assertEqual(problems, [], "\n".join(map(str, problems)))

    def test_cli_exit_codes(self):
        ok = subprocess.run([sys.executable, str(ROOT / "scripts/validate_rules.py"), str(ROOT / "data")], capture_output=True, text=True)
        self.assertEqual(ok.returncode, 0, ok.stdout + ok.stderr)
        with Broken() as b:
            b.edit("edges", "role_edge_id", "R0001", evidence_event_ids="E9999")
            bad = subprocess.run([sys.executable, str(ROOT / "scripts/validate_rules.py"), str(b.dir)], capture_output=True, text=True)
        self.assertEqual(bad.returncode, 1)
        self.assertIn("ERROR", bad.stdout)
        self.assertIn("B3", bad.stdout)


class EachRuleCanFail(unittest.TestCase):
    def check(self, rule, severity, table, key_col, key, **changes):
        with Broken() as b:
            b.edit(table, key_col, key, **changes)
            got = b.problems()
        self.assertIn(rule, rules(got, severity), "\n".join(map(str, got)) or "no problems reported")

    def test_B3_edge_cites_missing_event(self):
        self.check("B3", "ERROR", "edges", "role_edge_id", "R0001", evidence_event_ids="E0002|E9999")

    def test_B3_register_basis_cites_missing_event(self):
        self.check("B3", "ERROR", "register", "sphere", "S5_Tech_Compute", promotion_basis_event_ids="E9999")

    def test_B5_unknown_thread(self):
        self.check("B5", "ERROR", "events", "event_id", "E0002", thread_ids="T01|T99")

    def test_D1_blank_event_date_without_notes(self):
        self.check("D1", "ERROR", "events", "event_id", "E0002", event_date="", event_date_confidence="Low", notes="")

    def test_D2_event_date_without_confidence(self):
        self.check("D2", "ERROR", "events", "event_id", "E0002", event_date_confidence="")

    def test_D3_event_date_outside_its_window(self):
        self.check("D3", "ERROR", "events", "event_id", "E0002", event_date="2030-09-01")

    def test_D3_blank_event_date_needs_low_confidence(self):
        self.check("D3", "ERROR", "events", "event_id", "E0002", event_date="", event_date_confidence="High", notes="Date not reported.")

    def test_E1_non_state_resident_without_parent_or_note(self):
        self.check("E1", "WARN", "events", "event_id", "E0004", notes="")

    def test_E2_edge_resident_matches_no_evidence_event(self):
        self.check("E2", "ERROR", "edges", "role_edge_id", "R0001", resident="Resident W")

    def test_E3_state_claimed_from_asset_evidence(self):
        self.check("E3", "ERROR", "edges", "role_edge_id", "R0002", resident="Parent State P", resident_entity_type="state", resident_parent_state="")

    def test_P1_controller_edge_missing_a_proof(self):
        self.check("P1", "ERROR", "edges", "role_edge_id", "R0001", proof_C3="0")

    def test_P1_controller_edge_without_evidence(self):
        self.check("P1", "ERROR", "edges", "role_edge_id", "R0001", evidence_event_ids="")

    def test_P1_evidence_from_another_sphere(self):
        self.check("P1", "ERROR", "edges", "role_edge_id", "R0001", evidence_event_ids="E0002|E0004")

    def test_P1_evidence_after_the_edges_window(self):
        self.check("P1", "ERROR", "edges", "role_edge_id", "R0004", evidence_event_ids="E0005|E0006")

    def test_F1_controller_without_promoted_window(self):
        self.check("F1", "ERROR", "register", "sphere", "S5_Tech_Compute", promoted_window="")

    def test_F1_controller_without_a_qualifying_edge(self):
        self.check("F1", "ERROR", "edges", "role_edge_id", "R0001", role="candidate")

    def test_F2_candidate_although_an_edge_qualifies(self):
        self.check("F2", "WARN", "register", "sphere", "S5_Tech_Compute", status="candidate", promoted_window="", promotion_basis_event_ids="")

    def test_F3_contested_without_a_promotion(self):
        self.check("F3", "ERROR", "register", "sphere", "S3_Trade", promoted_window="")

    def test_W1_overlapping_windows(self):
        self.check("W1", "ERROR", "windows", "window_id", "W2", start_date="2030-06-01")


if __name__ == "__main__":
    unittest.main()
