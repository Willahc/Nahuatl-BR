"""Synthetic fixtures exercise admission, never serve as linguistic Evidence."""
import copy
import json
from pathlib import Path
import shutil
import tempfile
import unittest

from src.pipeline.corpus import derive_record, validate_record, validate, read
from src.pipeline.engine import IngestionEngine

ROOT = Path(__file__).resolve().parents[1]


class Gate6CorpusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = IngestionEngine(ROOT)
        cls.request = {'case_id': 'SYNTHETIC-TEST-NOT-EVIDENCE', 'ingest': {
            'lemma_id': 'L0051', 'lemma_variety': 'Classical Nahuatl',
            'source_id': 'A01', 'component_id': 'jcb_1571_images',
            'use': 'EVIDENCE_CAPTURE', 'mediation_level': 'DIRECT_WITNESS',
            'direct_witness_inspected': True, 'locator': 'SYNTHETIC TEST ONLY',
            'entries': [{'source_form_id': 'L0051-FS1', 'source_form': 'test-only',
                         'original_gloss': 'synthetic test'}],
            'declared_lossy': True, 'claims': [
                {'predicate': 'has_historical_gloss', 'value': 'synthetic test',
                 'modality': 'OBSERVED', 'confidence': 'UNASSESSED'},
                {'predicate': 'has_pt_br_editorial_gloss', 'value': 'teste sintético',
                 'modality': 'EDITORIAL', 'confidence': 'UNASSESSED'}]}}
        cls.good = derive_record(cls.request, {'image_url': 'TEST', 'canvas_id': 'TEST',
            'sha256': '0' * 64, 'attribution': 'TEST', 'column': 'a',
            'inspection': 'VISUALLY_INSPECTED'}, 1, 'TEST', ROOT)

    def rejected(self, change, code):
        rec = copy.deepcopy(self.good)
        change(rec)
        errors = validate_record(rec, self.engine)
        self.assertTrue(any(code in e for e in errors), errors)

    def test_positive_control(self):
        self.assertEqual(validate_record(self.good, self.engine), [])

    def count_fixture(self, count, duplicate=False, mutate=False):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for directory in ['data/pilot', 'data/gate6', 'data/policies', 'data/source_registry', 'data/phonology']:
                shutil.copytree(ROOT / directory, root / directory)
            dest = root / 'data/canonical/lemmas'; dest.mkdir(parents=True)
            # Clone only synthetic test candidates through the actual engine.
            for n in range(51, count + 1):
                req = copy.deepcopy(self.request)
                req['ingest']['lemma_id'] = f'L{n:04}'
                req['ingest']['entries'][0]['source_form_id'] = f'L{n:04}-FS1'
                rec = derive_record(req, self.good['gate6']['capture'], 1, 'TEST', root)
                if duplicate and n == count:
                    rec['lemma']['id'] = 'L0051'
                (dest / f'{n}.json').write_text(json.dumps(rec), encoding='utf-8')
            if mutate:
                p = next((root / 'data/pilot/lemmas').glob('L0001*'))
                rec = read(p); rec['lemma']['display_form'] = 'unauthorized'
                p.write_text(json.dumps(rec), encoding='utf-8')
            return validate(root, check_derived=False)

    def test_T01_499_reject(self): self.assertTrue(any('CORPUS_COUNT' in e for e in self.count_fixture(499)))
    def test_T02_501_reject(self): self.assertTrue(any('CORPUS_COUNT' in e for e in self.count_fixture(501)))
    def test_T03_duplicate_id(self): self.assertTrue(any('DUPLICATE_LEMMA_ID' in e for e in self.count_fixture(500, duplicate=True)))
    def test_T04_baseline_mutation(self): self.assertTrue(any('GATE3_CORPUS_REGRESSION' in e for e in self.count_fixture(500, mutate=True)))
    def test_T05_no_attestation(self): self.rejected(lambda r: r.update(attestations=[]), 'HISTORICAL_ATTESTATION_REQUIRED')
    def test_T06_unknown_source(self): self.rejected(lambda r: r['gate6']['request']['ingest'].update(source_id='ZZZ'), 'SOURCE_REFERENCE')
    def test_T07_modern(self): self.rejected(lambda r: r['lemma'].update(variety='Modern Variety'), 'MODERN_AS_CLASSICAL_EVIDENCE')
    def test_T08_rights(self): self.rejected(lambda r: r['gate6']['request']['ingest'].update(component_id='digital_surrogate'), 'RIGHTS_UNCLEAR')
    def test_T09_no_locator(self): self.rejected(lambda r: r['attestations'][0].update(locator=''), 'LOCATOR_REQUIRED')
    def test_T10_broken_evidence(self): self.rejected(lambda r: r.update(evidence=[]), 'UNRESOLVED_EVIDENCE')
    def test_T11_historical_translation(self): self.rejected(lambda r: r['senses'][0]['translations'][0].update(modality='REPORTED'), 'EDITORIAL_TRANSLATION_REQUIRED')
    def test_T12_published_claim(self): self.rejected(lambda r: r['claims'][0].update(editorial_state='PUBLISHED'), 'NEW_CLAIM_NOT_DRAFT')
    def test_T13_empty_source_form(self): self.rejected(lambda r: r['forms'][0].update(value=''), 'SOURCE_FORM_REQUIRED')
    def test_T14_auto_merge(self): self.rejected(lambda r: r['review'].update(automatic_merge=True), 'SEARCH_KEY_AUTO_MERGE')
    def test_T15_short(self): self.rejected(lambda r: r['phonological_information'].update(vowel_length='SHORT'), 'AUTO_VOWEL_LENGTH')
    def test_T16_saltillo(self): self.rejected(lambda r: r['phonological_information'].update(saltillo='ABSENT'), 'AUTO_SALTILLO')
    def test_T17_ipa(self): self.rejected(lambda r: r['phonological_information'].update(phonemic_ipa='test'), 'AUTO_IPA')
    def test_T18_gdn_bulk(self): self.rejected(lambda r: r['gate6']['request']['ingest'].update(source_id='B01', component_id='lexical_records'), 'SCALE_ACCESS_LAYER_NOT_APPROVED')
    def test_500_synthetic_positive(self): self.assertEqual(self.count_fixture(500), [])


if __name__ == '__main__': unittest.main()
