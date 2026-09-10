"""Exercise the Gate 5 ingestion pipeline and preview data in isolated copies.

Each test copies the canonical data tree and the preview file into a temporary
directory, plants (or mutates) fixtures there, and runs the pipeline engine and
exporter against that copy. The canonical repository is never touched.
"""

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
FIXTURES_DIR = ROOT / "data" / "fixtures" / "gate5_ingestion_cases"
PREVIEW_DATA_REL = Path("preview/public/data/nahuatl-br.json")


class Gate5PipelineTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="gate5-regression-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for directory in ("data/pilot", "data/source_registry", "data/policies",
                          "data/phonology", "data/fixtures"):
            shutil.copytree(ROOT / directory, self.root / directory)
        (self.root / "docs").mkdir()
        shutil.copyfile(ROOT / "docs/GATE_STATUS.md", self.root / "docs/GATE_STATUS.md")
        shutil.copytree(ROOT / "src", self.root / "src")
        shutil.copytree(ROOT / "scripts", self.root / "scripts")
        (self.root / "preview/public").mkdir(parents=True, exist_ok=True)
        if (ROOT / PREVIEW_DATA_REL).exists():
            (self.root / PREVIEW_DATA_REL.parent).mkdir(parents=True)
            shutil.copyfile(ROOT / PREVIEW_DATA_REL, self.root / PREVIEW_DATA_REL)

    def plant(self, fixture: dict):
        path = self.root / "data/fixtures/gate5_ingestion_cases" / f"{fixture['fixture_id']}.yml"
        path.write_text(json.dumps(fixture, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return path

    def run_python(self, *args):
        return subprocess.run(
            [sys.executable, "-B", "-m", "src.pipeline.cli", *args],
            cwd=self.root, capture_output=True, text=True, encoding="utf-8",
            env={**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1"},
        )

    def run_validator(self, *args):
        return subprocess.run(
            [sys.executable, "-B", "scripts/validate_gate5.py", *args],
            cwd=self.root, capture_output=True, text=True, encoding="utf-8",
            env={**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1"},
        )

    def snapshot(self):
        return {p.relative_to(self.root).as_posix(): p.read_bytes()
                for p in self.root.rglob("*") if p.is_file()}

    # ------------------------------------------------------------- fixtures
    def basic_accept(self, **overrides):
        fixture = {
            "fixture_id": "G5T001",
            "version": "1.0.0",
            "purpose": "positive control fixture planted for regression",
            "expect": {"outcome": "ACCEPT", "codes": []},
            "ingest": {
                "lemma_variety": "Classical Nahuatl",
                "lemma_id": "L0050",
                "requested_forms": ["DIPLOMATIC_FORM", "NORMALIZED_FORM", "PEDAGOGICAL_FORM", "SEARCH_KEY"],
                "declared_lossy": True,
                "source_id": "A01",
                "component_id": "historical_work",
                "use": "EVIDENCE_CAPTURE",
                "mediator": "B01",
                "mediation_level": "AGGREGATOR",
                "locator": "GDN entry 168847",
                "url": "https://gdn.iib.unam.mx/diccionario/xochitl/168847",
                "accessed_at": "2026-09-03",
                "entries": [{"source_form_id": "L0050-FS1", "source_form": "Xochitl", "original_gloss": "rosa, o flor."}],
                "claims": [{"predicate": "has_historical_gloss", "value": "rosa, o flor.",
                            "modality": "REPORTED", "confidence": "HIGH", "requested_state": "DRAFT"}],
            },
        }
        self._apply(fixture["ingest"], overrides)
        return fixture

    @staticmethod
    def _apply(dest, overrides):
        for key, value in overrides.items():
            dest[key] = value

    def run_ingest(self, fixture, expectation="REJECT"):
        path = self.plant(fixture)
        result = self.run_python("ingest", str(path))
        if expectation == "ACCEPT":
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn('"outcome": "ACCEPT"', result.stdout)
        else:
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        return json.loads(result.stdout.splitlines()[0]) if result.stdout else {}

    # ------------------------------------------------------------------ tests
    def test_T01_positive_control_accept_and_artifact_shape(self):
        result = self.run_ingest(self.basic_accept(), expectation="ACCEPT")
        artifacts = result.get("artifacts")
        self.assertIsNotNone(artifacts)
        self.assertEqual(artifacts["lemma"]["id"], "L0050")
        layers = {f["layer"] for f in artifacts["forms"]}
        self.assertTrue({"DIPLOMATIC_FORM", "NORMALIZED_FORM", "PEDAGOGICAL_FORM"} <= layers)
        keys = {s["value"] for s in artifacts["search_keys"]}
        self.assertIn("xochitl", keys)
        claim = artifacts["claims"][0]
        self.assertEqual(claim["editorial_state"], "DRAFT")
        self.assertEqual(claim["origin"], "PIPELINE")
        self.assertTrue(claim["evidence"], "DRAFT claim must carry Evidence")

    def test_T02_variant_preserved_and_search_folded(self):
        # Historical diaeresis remains intact in attestation and search key.
        fixture = self.basic_accept(requested_forms=["SEARCH_KEY"], entries=[
            {"source_form_id": "L0050-FS1", "source_form": "Xochitl", "original_gloss": "rosa, o flor."},
            {"source_form_id": "L0050-FS2", "source_form": "xöchitl", "original_gloss": "flor / flor(es)"},
        ])
        result = self.run_ingest(fixture, expectation="ACCEPT")
        artifacts = result["artifacts"]
        attestations = {a["source_form"] for a in artifacts["attestations"]}
        self.assertEqual(attestations, {"Xochitl", "xöchitl"})
        keys = [s["value"] for s in artifacts["search_keys"]]
        self.assertEqual(keys, ["xochitl", "xöchitl"])
        self.assertEqual(len({s["form_id"] for s in artifacts["search_keys"]}), 2)

    def test_macron_key_equality_does_not_create_identity_claim(self):
        fixture = self.basic_accept(lemma_id="TEST-RETRIEVAL", requested_forms=["SEARCH_KEY"], claims=[], entries=[
            {"source_form_id": "test-a", "source_form": "xochitl"},
            {"source_form_id": "test-b", "source_form": "xōchitl"},
        ])
        artifacts = self.run_ingest(fixture, expectation="ACCEPT")["artifacts"]
        self.assertEqual([s["value"] for s in artifacts["search_keys"]], ["xochitl", "xochitl"])
        self.assertEqual(artifacts["claims"], [])
        self.assertEqual(len({s["form_id"] for s in artifacts["search_keys"]}), 2)

    def test_search_diacritic_whitelist(self):
        from src.pipeline.loader import load_policy_orthography
        from src.pipeline.normalize import OrthographyNormalizer
        normalizer = OrthographyNormalizer(load_policy_orthography(ROOT))
        for original, expected in [("āēīōĀĒĪŌ", "aeioaeio"), ("ā", "a"),
                                   ("xōchitl", "xochitl"), ("xöchitl", "xöchitl"),
                                   ("à", "à"), ("á", "á"), ("ç", "ç"),
                                   ("âãäëïö", "âãäëïö"), ("a\u035c", "a\u035c")]:
            with self.subTest(original=original):
                result = normalizer.transform(original, "SEARCH_KEY", declared_lossy=True)
                self.assertEqual(result.result, expected)
        for value in ["a\u0300", "a\u0301", "c\u0327", "a\u035c", "xöchitl"]:
            self.assertEqual(normalizer._apply("search-diacritic-001", value), value)

    def test_T03_rights_gate_requires_no_name(self):
        # mandatory negative: rename the Hueyapan label to a neutral id and
        # confirm the engine still refuses on structured metadata alone.
        registry_dir = self.root / "data/source_registry"
        for path in registry_dir.glob("*.yml"):
            text = path.read_text(encoding="utf-8-sig").replace("Hueyapan", "Variant-Alpha")
            path.write_text(text, encoding="utf-8")
        fixture = self.basic_accept(source_id="C01", component_id="spanish_nahuatl_dictionary")
        path = self.plant(fixture)
        result = self.run_python("ingest", str(path))
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("MODERN_AS_CLASSICAL_EVIDENCE", result.stdout)
        self.assertIn("RIGHTS_PERMISSION", result.stdout)

    def test_T04_modern_aggregator_rejected_as_classical(self):
        result = self.run_ingest(
            self.basic_accept(source_id="B01", component_id="translations_examples_locators"))
        codes = {e["code"] for e in result.get("errors", [])}
        self.assertTrue({"MODERN_AS_CLASSICAL_EVIDENCE", "RIGHTS_UNCLEAR"} <= codes)
        self.assertIn("MODERN_AS_CLASSICAL_EVIDENCE", {e["code"] for e in result.get("errors", [])})

    def test_T05_search_key_lossy_undeclared_rejected(self):
        result = self.run_ingest(
            self.basic_accept(requested_forms=["SEARCH_KEY"], declared_lossy=False))
        self.assertEqual(result.get("outcome"), "REJECT")
        codes = {e["code"] for e in result.get("errors", [])}
        self.assertIn("LOSSY_UNDECLARED", codes)

    def test_T06_auto_short_inference_rejected(self):
        result = self.run_ingest(self.basic_accept(
            phonology_hints={"vowel_length": {"value": "SHORT", "evidence": []}}))
        self.assertEqual(result.get("outcome"), "REJECT")
        codes = {e["code"] for e in result.get("errors", [])}
        self.assertIn("AUTO_SHORT_INFERENCE", codes)

    def test_T07_direct_witness_inspection_required(self):
        result = self.run_ingest(self.basic_accept(
            mediation_level="DIRECT_WITNESS", direct_witness_inspected=False,
            mediator=None))
        codes = {e["code"] for e in result.get("errors", [])}
        self.assertIn("DIRECT_WITNESS_INSPECTION", codes)

    def test_T08_duplicate_entry_rejected(self):
        entries = [
            {"source_form_id": "L0050-FS1", "source_form": "Xochitl", "original_gloss": "rosa, o flor."},
            {"source_form_id": "L0050-FS1", "source_form": "Xochitl", "original_gloss": "second capture"},
        ]
        result = self.run_ingest(self.basic_accept(entries=entries))
        codes = {e["code"] for e in result.get("errors", [])}
        self.assertIn("DUPLICATE_ENTRY", codes)

    def test_T09_unknown_source_rejected(self):
        result = self.run_ingest(self.basic_accept(source_id="ZZ9"))
        codes = {e["code"] for e in result.get("errors", [])}
        self.assertIn("SOURCE_REFERENCE", codes)

    def test_T10_call_validation_positive(self):
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("GATE 5 VALIDATION: PASS", result.stdout)

    def test_T11_mandatory_negative_removal_fails_validation(self):
        # Removing the only fixture that exercises RIGHTS_DO_NOT_INGEST must
        # make the validator fail its mandatory-negative coverage.
        path = self.root / "data/fixtures/gate5_ingestion_cases/G5-010-reject-c01-donotingest.yml"
        self.assertTrue(path.exists(), "expected G5-010 mandatory negative present")
        path.unlink()
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("MANDATORY_NEGATIVE", result.stderr)
        self.assertIn("RIGHTS_DO_NOT_INGEST", result.stderr)


if __name__ == "__main__":
    unittest.main()
