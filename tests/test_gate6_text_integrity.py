"""Text rejection and record-specific editorial regressions; no auto-repair."""
import copy
import csv
import json
from pathlib import Path
import tempfile
import unittest
from src.pipeline.text_integrity import text_errors, ledger_errors, numeral_errors, scan

ROOT = Path(__file__).resolve().parents[1]


class TextIntegrityTests(unittest.TestCase):
    def test_UTF01_headword(self):
        self.assertTrue(text_errors('ChicoquiÃƒÆ’Ã‚Â§a'))

    def test_UTF02_domain(self):
        self.assertTrue(text_errors('relaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Âµes'))

    def test_UTF03_replacement(self):
        self.assertTrue(text_errors('\ufffd'))

    def test_UTF04_cedilla(self):
        self.assertEqual(text_errors('ç'), [])

    def test_UTF05_long_s(self):
        self.assertEqual(text_errors('ſanguijuela'), [])

    def test_UTF06_enye(self):
        self.assertEqual(text_errors('ñ'), [])

    def test_UTF07_valid_nfc(self):
        self.assertEqual(text_errors('tradução: pão, café, niño; ā'), [])

    def test_controls(self):
        for c in ('\x00', '\x1b', '\x85', '\x9f'):
            self.assertTrue(text_errors(c))
        self.assertEqual(text_errors('line\n\tline\r\n'), [])

    def test_scan_decodes_json_escapes_without_modifying(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            p = root / 'data/canonical/lemmas/L0201.json'
            p.parent.mkdir(parents=True)
            p.write_text(json.dumps({'value': '\ufffd'}), encoding='utf-8')
            before = p.read_bytes()
            self.assertTrue(scan(root))
            self.assertEqual(p.read_bytes(), before)

    def test_ledger_fields_and_missing_row(self):
        with (ROOT / 'data/gate6/batches/batch04.tsv').open(encoding='utf-8') as f:
            rows = list(csv.DictReader(f, delimiter='\t'))
        recs = [json.loads((ROOT / f'data/canonical/lemmas/L{i:04}.json').read_text(encoding='utf-8'))
                for i in range(201, 251)]
        self.assertEqual(ledger_errors(rows, recs), [])
        for field in ('source_form', 'historical_gloss', 'pt_br', 'domain', 'page', 'column'):
            changed = copy.deepcopy(rows)
            changed[0][field] = 'synthetic mismatch'
            self.assertTrue(any('BATCH_LEDGER_CANONICAL_DRIFT' in e for e in ledger_errors(changed, recs)))
        self.assertTrue(ledger_errors(rows[:-1], recs))

    def check_numeral(self, lid, expected):
        r = json.loads((ROOT / f'data/canonical/lemmas/{lid}.json').read_text(encoding='utf-8'))
        self.assertEqual(r['senses'][0]['translations'][0]['text'], expected)
        self.assertEqual(numeral_errors([r]), [])
        r['senses'][0]['translations'][0]['text'] = 'nove'
        self.assertTrue(numeral_errors([r]))

    def test_L0241(self):
        self.check_numeral('L0241', 'sete')

    def test_L0242(self):
        self.check_numeral('L0242', 'sete coisas, pares ou partes')

    def test_L0243(self):
        self.check_numeral('L0243', 'sete vezes')
