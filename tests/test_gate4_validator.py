"""Exercise the Gate 4 validator in isolated copies; never mutate canonical data."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class Gate4ValidatorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="gate4-regression-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for directory in ("data/pilot", "data/source_registry", "data/policies",
                          "data/phonology", "data/fixtures"):
            shutil.copytree(ROOT / directory, self.root / directory)
        (self.root / "scripts").mkdir()
        for name in ("validate_gate4.py", "gate3_integrity.py"):
            shutil.copyfile(ROOT / "scripts" / name, self.root / "scripts" / name)

    def mutate(self, path, action):
        record = json.loads(path.read_text(encoding="utf-8-sig"))
        action(record)
        path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def snapshot(self):
        return {p.relative_to(self.root).as_posix(): p.read_bytes()
                for p in self.root.rglob("*") if p.is_file()}

    def run_validator(self, *args):
        return subprocess.run(
            [sys.executable, "-B", str(self.root / "scripts/validate_gate4.py"), *args],
            cwd=self.root, capture_output=True, text=True, encoding="utf-8",
            env={**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1"},
        )

    def rejected(self, category, *args):
        before = self.snapshot()
        result = self.run_validator(*args)
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn(category, result.stderr)
        self.assertEqual(before, self.snapshot(), "invalid input modified files")

    # ---------------------------------------------------------------- helpers
    def evidence(self):
        return self.root / "data/phonology/evidence.yml"

    def claims(self, cid):
        return self.root / "data/phonology/claims" / f"{cid}.yml"

    def integration(self):
        return self.root / "data/phonology/integration_sample.yml"

    def fixtures(self):
        return self.root / "data/fixtures/gate4_phonology_cases.yml"

    def lemma_file(self, lid):
        return self.root / "data/pilot/lemmas" / f"{lid}_" and next(
            (self.root / "data/pilot/lemmas").glob(f"{lid}_*.yml"))

    # ------------------------------------------------------------------ tests
    def test_positive_canonical_read_only(self):
        before = self.snapshot()
        for args in ((), ("--check",)):
            result = self.run_validator(*args)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("GATE 4 VALIDATION: PASS", result.stdout)
        self.assertEqual(before, self.snapshot())

    def test_T01_saltillo_marked_without_evidence(self):
        self.mutate(self.integration(), lambda r: _item(r, "L0018")["saltillo"].update(evidence=[]))
        self.rejected("SALTILLO_EVIDENCE_REQUIRED")

    def test_T02_vowel_length_marked_without_evidence(self):
        self.mutate(self.integration(), lambda r: _item(r, "L0001")["vowel_length"].update(evidence=[]))
        self.rejected("VOWEL_LENGTH_EVIDENCE_REQUIRED")

    def test_T03_modern_variety_as_direct_classical_evidence(self):
        self.mutate(self.evidence(), lambda r: r["evidence"][2].update(
            source_id="C03", evidence_role="DIRECT_CLASSICAL_EVIDENCE"))
        self.rejected("MODERN_AS_DIRECT_EVIDENCE")

    def test_T04_phonetic_realization_without_evidence_or_confidence(self):
        self.mutate(self.integration(), lambda r: _item(r, "L0001").update(
            phonetic_ipa="[a]", evidence=[]))
        self.rejected("PHONETIC_REALIZATION_GUARD")

    def test_T05_unknown_source_id(self):
        self.mutate(self.evidence(), lambda r: r["evidence"][0].update(source_id="Z99"))
        self.rejected("SOURCE_REFERENCE")

    def test_T06_invalid_mediation_level(self):
        self.mutate(self.evidence(), lambda r: r["evidence"][0].update(mediation_level="INVALID"))
        self.rejected("EVIDENCE_REFERENCE")

    def test_T07_source_form_mutated_against_baseline(self):
        path = self.lemma_file("L0001")
        self.mutate(path, lambda r: _source_form(r, "L0001-FS2").update(value="amoxtli"))
        self.rejected("SOURCE_FORM_MUTATION")

    def test_T08_integration_exceeds_lemma_cap(self):
        def mutate(record):
            extra = json.loads(json.dumps(record["items"][0]))
            extra.update(lemma_id="L0040", case_id="G4F999",
                         source_form_id="L0040-FS2", source_form="teötl")
            record["items"].append(extra)
        self.mutate(self.integration(), mutate)
        self.rejected("INTEGRATION_CAP")

    def test_T09_policy_promoted_to_approved(self):
        path = self.root / "data/policies/classical_phonology_v1.yml"
        self.mutate(path, lambda r: r.update(status="APPROVED"))
        self.rejected("POLICY_STATUS")

    def test_T10_audio_file_present(self):
        (self.root / "data/phonology/sample.mp3").write_bytes(b"\x00\x01")
        self.rejected("AUDIO_PRESENT")

    def test_T11_claim_evidence_unresolved(self):
        self.mutate(self.claims("G4C001"), lambda r: r.update(evidence=["G4E999"]))
        self.rejected("EVIDENCE_REFERENCE")

    def test_T12_fixture_evidence_unresolved(self):
        self.mutate(self.fixtures(), lambda r: r["cases"][0].update(evidence=["G4E999"]))
        self.rejected("EVIDENCE_REFERENCE")

    def test_T13_phonemic_ipa_with_brackets(self):
        self.mutate(self.claims("G4C006"), lambda r: r.update(phonemic_ipa="/a[/"))
        self.rejected("PHONEMIC_IPA_FORMAT")

    def test_T14_phonetic_ipa_with_slashes(self):
        self.mutate(self.integration(), lambda r: _item(r, "L0001").update(phonetic_ipa="/a/"))
        self.rejected("PHONETIC_IPA_FORMAT")

    def test_T15_unmarked_inferred_as_short(self):
        def mutate(record):
            item = _item(record, "L0001")
            item["vowel_length"].update(value="SHORT", evidence=["G4E002"])
        self.mutate(self.integration(), mutate)
        self.rejected("AUTO_SHORT_INFERENCE")


def _item(record, lemma_id):
    return next(item for item in record["items"] if item["lemma_id"] == lemma_id)


def _source_form(record, form_id):
    return next(f for f in record["forms"] if f["form_id"] == form_id)


if __name__ == "__main__":
    unittest.main()