"""Exercise the CLI in isolated copies; never mutate the canonical corpus."""

import copy
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class Gate3ValidatorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="nahuatl-regression-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for directory in ("data/pilot", "data/source_registry", "data/policies"):
            shutil.copytree(ROOT / directory, self.root / directory)
        (self.root / "scripts").mkdir()
        for name in ("validate_gate3.py", "gate3_integrity.py"):
            shutil.copyfile(ROOT / "scripts" / name, self.root / "scripts" / name)
        self.path = self.root / "data/pilot/lemmas/L0001_amoxtli.yml"

    def mutate(self, action, path=None):
        path = path or self.path
        record = json.loads(path.read_text(encoding="utf-8-sig"))
        action(record)
        path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def snapshot(self):
        return {p.relative_to(self.root).as_posix(): p.read_bytes()
                for p in self.root.rglob("*") if p.is_file()}

    def run_validator(self, *args):
        return subprocess.run(
            [sys.executable, "-B", str(self.root / "scripts/validate_gate3.py"), *args],
            cwd=self.root, capture_output=True, text=True, encoding="utf-8",
            env={**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1"},
        )

    def rejected(self, category, *args):
        before = self.snapshot()
        result = self.run_validator(*args)
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn(category, result.stderr)
        self.assertEqual(before, self.snapshot(), "invalid input modified files")

    def test_positive_canonical_read_only(self):
        before = self.snapshot()
        for args in ((), ("--check",)):
            result = self.run_validator(*args)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("GATE 3 VALIDATION: PASS", result.stdout)
        self.assertEqual(before, self.snapshot())

    def test_T01_claim_missing_appropriate_evidence(self):
        self.mutate(lambda r: r["evidence_links"].pop(0))
        self.rejected("CLAIM_EVIDENCE_REQUIRED")

    def test_T02_modern_source_scope(self):
        self.mutate(lambda r: r["attestations"][0].update(source="C01"))
        self.rejected("SOURCE_VARIETY_MISMATCH")

    def test_T03_form_unresolved_evidence(self):
        self.mutate(lambda r: r["forms"][0].update(evidence=["MISSING"]))
        self.rejected("UNRESOLVED_REFERENCE")

    def test_T04_duplicate_claim_id(self):
        self.mutate(lambda r: r["claims"][1].update(claim_id=r["claims"][0]["claim_id"]))
        self.rejected("DUPLICATE_ID")

    def test_T05_invalid_relation(self):
        self.mutate(lambda r: r["evidence_links"][0].update(relation="INVALID"))
        self.rejected("INVALID_EVIDENCE_RELATION")

    def test_T06_unreviewed_locator_without_reason(self):
        # The canonical underlying_locator is already NOT_REVIEWED.
        self.mutate(lambda r: r["attestations"][0].update(locator_absence_reason=" "))
        self.rejected("LOCATOR_JUSTIFICATION")

    def test_T07_wrong_specific_source_form_chain(self):
        self.mutate(lambda r: r["forms"][0].update(evidence=[r["evidence"][1]["evidence_id"]]))
        self.rejected("SOURCE_FORM_CHAIN")

    def test_T08_empty_translation(self):
        for value in ("", " \t\n"):
            with self.subTest(value=repr(value)):
                self.mutate(lambda r: r["senses"][0]["translations"][0].update(text=value))
                self.rejected("EMPTY_TRANSLATION")

    def test_T09_missing_normalization_profile(self):
        self.mutate(lambda r: r["forms"][2].pop("normalization_profile"))
        self.rejected("NORMALIZATION_PROFILE")

    def test_index_drift(self):
        self.mutate(lambda r: r["lemmas"][0].update(display_form="DRIFT"),
                    self.root / "data/pilot/pilot_index.yml")
        self.rejected("DERIVED_DATA_OUT_OF_DATE", "--check")

    def test_metrics_drift(self):
        self.mutate(lambda r: r.update(total_lemmas=49), self.root / "data/pilot/pilot_metrics.json")
        self.rejected("DERIVED_DATA_OUT_OF_DATE")

    def test_missing_derived(self):
        (self.root / "data/pilot/pilot_metrics.json").unlink()
        self.rejected("DERIVED_DATA_OUT_OF_DATE")

    def test_write_derived_rejects_invalid_data_without_writes(self):
        self.mutate(lambda r: r["evidence_links"].pop(0))
        self.rejected("CLAIM_EVIDENCE_REQUIRED", "--write-derived")

    def test_explicit_write_repairs_derived_only(self):
        self.mutate(lambda r: r.update(total_lemmas=49), self.root / "data/pilot/pilot_metrics.json")
        before = self.snapshot()
        result = self.run_validator("--write-derived")
        self.assertEqual(result.returncode, 0, result.stderr)
        after = self.snapshot()
        self.assertEqual([p for p in before if before[p] != after[p]], ["data/pilot/pilot_metrics.json"])
        self.assertEqual(self.run_validator("--check").returncode, 0)

    def test_typed_reference_regressions(self):
        original = self.path.read_bytes()
        mutations = {
            "link_claim": lambda r: r["evidence_links"][0].update(claim_id="MISSING"),
            "link_evidence": lambda r: r["evidence_links"][0].update(evidence_id="MISSING"),
            "translation": lambda r: r["senses"][0]["translations"][0].update(derived_from="MISSING"),
            "phonology": lambda r: r["phonological_information"]["vowel_length_evidence"][0].update(evidence_id="MISSING"),
            "attestation": lambda r: r["evidence"][0].update(attestation_id="MISSING"),
        }
        for name, mutate in mutations.items():
            with self.subTest(reference=name):
                self.path.write_bytes(original)
                self.mutate(mutate)
                self.rejected("UNRESOLVED_REFERENCE")

    def test_morphology_reference(self):
        self.mutate(lambda r: r["morphology"]["analyses"][0].update(evidence=["MISSING"]),
                    self.root / "data/pilot/lemmas/L0024_mati.yml")
        self.rejected("UNRESOLVED_REFERENCE")

    def test_all_local_id_namespaces(self):
        original = self.path.read_bytes()
        for collection, key in (("forms", "form_id"), ("senses", "sense_id"),
                                ("claims", "claim_id"), ("attestations", "attestation_id"),
                                ("evidence", "evidence_id")):
            with self.subTest(id=key):
                self.path.write_bytes(original)
                self.mutate(lambda r: r[collection].append(copy.deepcopy(r[collection][0])))
                self.rejected("DUPLICATE_ID")
        self.path.write_bytes(original)
        self.mutate(lambda r: r["senses"][0]["translations"].append(copy.deepcopy(r["senses"][0]["translations"][0])))
        self.rejected("DUPLICATE_ID")

    def test_analysis_and_divergence_duplicate_ids(self):
        path = self.root / "data/pilot/lemmas/L0024_mati.yml"
        original = path.read_bytes()
        for mutate in (lambda r: r["morphology"]["analyses"].append(copy.deepcopy(r["morphology"]["analyses"][0])),
                       lambda r: r["divergences"].append(copy.deepcopy(r["divergences"][0]))):
            path.write_bytes(original)
            self.mutate(mutate, path)
            self.rejected("DUPLICATE_ID")

    def test_duplicate_lemma_id(self):
        shutil.copyfile(self.path, self.root / "data/pilot/lemmas/duplicate.yml")
        self.rejected("DUPLICATE_ID")

    def test_unknown_source(self):
        self.mutate(lambda r: r["attestations"][0].update(source="MISSING"))
        self.rejected("SOURCE_REFERENCE")

    def test_wrong_work(self):
        self.mutate(lambda r: r["attestations"][0].update(work="OTHER WORK"))
        self.rejected("WORK_REFERENCE")

    def test_unsupported_profile(self):
        self.mutate(lambda r: r["forms"][2].update(normalization_profile="classical_orthography_v1@0.0.0"))
        self.rejected("NORMALIZATION_PROFILE")

    def test_editorial_claim_requires_evidence(self):
        self.mutate(lambda r: r["evidence_links"].pop(1))
        self.rejected("CLAIM_EVIDENCE_REQUIRED")

    def test_provenance_required(self):
        self.mutate(lambda r: r["claims"][0].pop("editorial_provenance"))
        self.rejected("EDITORIAL_PROVENANCE")

    def test_draft_and_quarantined_without_evidence_allowed(self):
        original = self.path.read_bytes()
        for state in ("DRAFT", "QUARANTINED"):
            with self.subTest(state=state):
                self.path.write_bytes(original)
                def mutate(record):
                    record["evidence_links"].pop(0)
                    record["claims"][0]["editorial_state"] = state
                    record["claims"][0]["editorial_provenance"]["to_state"] = state
                self.mutate(mutate)
                result = self.run_validator("--write-derived")
                self.assertEqual(result.returncode, 0, result.stderr)

    def test_approved_and_published_without_evidence_rejected(self):
        original = self.path.read_bytes()
        for state in ("APPROVED", "PUBLISHED"):
            with self.subTest(state=state):
                self.path.write_bytes(original)
                def mutate(record):
                    record["evidence_links"].pop(0)
                    record["claims"][0]["editorial_state"] = state
                    record["claims"][0]["editorial_provenance"]["to_state"] = state
                self.mutate(mutate)
                self.rejected("CLAIM_EVIDENCE_REQUIRED")

    def test_malformed_record_does_not_write(self):
        self.path.write_text("{}", encoding="utf-8")
        self.rejected("SCHEMA_ERROR")


if __name__ == "__main__":
    unittest.main()
