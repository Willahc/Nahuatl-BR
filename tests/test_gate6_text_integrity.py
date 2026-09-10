"""Text rejection and record-specific editorial regressions; no auto-repair."""
import copy
import csv
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from src.pipeline.text_integrity import text_errors, ledger_errors, numeral_errors, scan, validate_ledgers

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

    def test_LEDGER01_batch04_pass(self):
        p = ROOT / 'data/gate6/batches/batch04.tsv'
        with p.open(encoding='utf-8') as f:
            rows = list(csv.DictReader(f, delimiter='\t'))
        recs = [json.loads((ROOT / f'data/canonical/lemmas/L{i:04}.json').read_text(encoding='utf-8'))
                for i in range(201, 251)]
        sha = hashlib.sha256(p.read_bytes()).hexdigest()
        self.assertEqual(ledger_errors(rows, recs, batch=4, ledger_sha=sha), [])

    @unittest.skipUnless((ROOT / 'data/gate6/batches/batch05.tsv').exists(), "batch05.tsv not present")
    def test_LEDGER02_batch05_pass(self):
        p = ROOT / 'data/gate6/batches/batch05.tsv'
        with p.open(encoding='utf-8') as f:
            rows = list(csv.DictReader(f, delimiter='\t'))
        recs = [json.loads((ROOT / f'data/canonical/lemmas/L{i:04}.json').read_text(encoding='utf-8'))
                for i in range(251, 301)]
        sha = hashlib.sha256(p.read_bytes()).hexdigest()
        self.assertEqual(ledger_errors(rows, recs, batch=5, ledger_sha=sha), [])

    @unittest.skipUnless((ROOT / 'data/gate6/batches/batch05.tsv').exists(), "batch05.tsv not present")
    def test_LEDGER03_batch05_source_form_mismatch(self):
        p = ROOT / 'data/gate6/batches/batch05.tsv'
        with p.open(encoding='utf-8') as f:
            rows = list(csv.DictReader(f, delimiter='\t'))
        recs = [json.loads((ROOT / f'data/canonical/lemmas/L{i:04}.json').read_text(encoding='utf-8'))
                for i in range(251, 301)]
        rows[0]['source_form'] = 'divergent_source_form'
        errs = ledger_errors(rows, recs, batch=5)
        self.assertTrue(any('BATCH_LEDGER_CANONICAL_DRIFT: batch05 L0251 source_form' in e for e in errs), errs)

    @unittest.skipUnless((ROOT / 'data/gate6/batches/batch05.tsv').exists(), "batch05.tsv not present")
    def test_LEDGER04_batch05_historical_gloss_mismatch(self):
        p = ROOT / 'data/gate6/batches/batch05.tsv'
        with p.open(encoding='utf-8') as f:
            rows = list(csv.DictReader(f, delimiter='\t'))
        recs = [json.loads((ROOT / f'data/canonical/lemmas/L{i:04}.json').read_text(encoding='utf-8'))
                for i in range(251, 301)]
        rows[0]['historical_gloss'] = 'divergent historical gloss'
        errs = ledger_errors(rows, recs, batch=5)
        self.assertTrue(any('BATCH_LEDGER_CANONICAL_DRIFT: batch05 L0251 historical_gloss' in e for e in errs), errs)

    @unittest.skipUnless((ROOT / 'data/gate6/batches/batch05.tsv').exists(), "batch05.tsv not present")
    def test_LEDGER05_batch05_pt_br_mismatch(self):
        p = ROOT / 'data/gate6/batches/batch05.tsv'
        with p.open(encoding='utf-8') as f:
            rows = list(csv.DictReader(f, delimiter='\t'))
        recs = [json.loads((ROOT / f'data/canonical/lemmas/L{i:04}.json').read_text(encoding='utf-8'))
                for i in range(251, 301)]
        rows[0]['pt_br'] = 'tradução divergente'
        errs = ledger_errors(rows, recs, batch=5)
        self.assertTrue(any('BATCH_LEDGER_CANONICAL_DRIFT: batch05 L0251 pt_br' in e for e in errs), errs)

    @unittest.skipUnless((ROOT / 'data/gate6/batches/batch05.tsv').exists(), "batch05.tsv not present")
    def test_LEDGER06_batch05_domain_mismatch(self):
        p = ROOT / 'data/gate6/batches/batch05.tsv'
        with p.open(encoding='utf-8') as f:
            rows = list(csv.DictReader(f, delimiter='\t'))
        recs = [json.loads((ROOT / f'data/canonical/lemmas/L{i:04}.json').read_text(encoding='utf-8'))
                for i in range(251, 301)]
        rows[0]['domain'] = 'domínio_divergente'
        errs = ledger_errors(rows, recs, batch=5)
        self.assertTrue(any('BATCH_LEDGER_CANONICAL_DRIFT: batch05 L0251 domain' in e for e in errs), errs)

    @unittest.skipUnless((ROOT / 'data/gate6/batches/batch05.tsv').exists(), "batch05.tsv not present")
    def test_LEDGER07_batch05_page_mismatch(self):
        p = ROOT / 'data/gate6/batches/batch05.tsv'
        with p.open(encoding='utf-8') as f:
            rows = list(csv.DictReader(f, delimiter='\t'))
        recs = [json.loads((ROOT / f'data/canonical/lemmas/L{i:04}.json').read_text(encoding='utf-8'))
                for i in range(251, 301)]
        rows[0]['page'] = '999'
        errs = ledger_errors(rows, recs, batch=5)
        self.assertTrue(any('BATCH_LEDGER_CANONICAL_DRIFT: batch05 L0251 page' in e for e in errs), errs)

    @unittest.skipUnless((ROOT / 'data/gate6/batches/batch05.tsv').exists(), "batch05.tsv not present")
    def test_LEDGER08_batch05_column_mismatch(self):
        p = ROOT / 'data/gate6/batches/batch05.tsv'
        with p.open(encoding='utf-8') as f:
            rows = list(csv.DictReader(f, delimiter='\t'))
        recs = [json.loads((ROOT / f'data/canonical/lemmas/L{i:04}.json').read_text(encoding='utf-8'))
                for i in range(251, 301)]
        rows[0]['column'] = 'z'
        errs = ledger_errors(rows, recs, batch=5)
        self.assertTrue(any('BATCH_LEDGER_CANONICAL_DRIFT: batch05 L0251 column' in e for e in errs), errs)

    @unittest.skipUnless((ROOT / 'data/gate6/batches/batch05.tsv').exists(), "batch05.tsv not present")
    def test_LEDGER09_ledger_49_rows_reject(self):
        p = ROOT / 'data/gate6/batches/batch05.tsv'
        with p.open(encoding='utf-8') as f:
            rows = list(csv.DictReader(f, delimiter='\t'))
        recs = [json.loads((ROOT / f'data/canonical/lemmas/L{i:04}.json').read_text(encoding='utf-8'))
                for i in range(251, 301)]
        errs = ledger_errors(rows[:49], recs, batch=5)
        self.assertTrue(any('row count' in e for e in errs), errs)

    @unittest.skipUnless((ROOT / 'data/gate6/batches/batch05.tsv').exists(), "batch05.tsv not present")
    def test_LEDGER10_ledger_51_rows_reject(self):
        p = ROOT / 'data/gate6/batches/batch05.tsv'
        with p.open(encoding='utf-8') as f:
            rows = list(csv.DictReader(f, delimiter='\t'))
        recs = [json.loads((ROOT / f'data/canonical/lemmas/L{i:04}.json').read_text(encoding='utf-8'))
                for i in range(251, 301)]
        errs = ledger_errors(rows + [rows[0]], recs, batch=5)
        self.assertTrue(any('row count' in e for e in errs), errs)

    @unittest.skipUnless((ROOT / 'data/gate6/batches/batch05.tsv').exists(), "batch05.tsv not present")
    def test_LEDGER11_reviewed_ledger_sha256_mismatch(self):
        p = ROOT / 'data/gate6/batches/batch05.tsv'
        with p.open(encoding='utf-8') as f:
            rows = list(csv.DictReader(f, delimiter='\t'))
        recs = [json.loads((ROOT / f'data/canonical/lemmas/L{i:04}.json').read_text(encoding='utf-8'))
                for i in range(251, 301)]
        errs = ledger_errors(rows, recs, batch=5, ledger_sha='0' * 64)
        self.assertTrue(any('REVIEWED_LEDGER_HASH_MISMATCH' in e for e in errs), errs)

    @unittest.skipUnless((ROOT / 'data/gate6/batches/batch05.tsv').exists(), "batch05.tsv not present")
    def test_LEDGER12_batch05_missing_when_lemmas_exist(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            (tmp_root / 'data/gate6/batches').mkdir(parents=True)
            p04 = ROOT / 'data/gate6/batches/batch04.tsv'
            (tmp_root / 'data/gate6/batches/batch04.tsv').write_bytes(p04.read_bytes())
            recs = [json.loads((ROOT / f'data/canonical/lemmas/L{i:04}.json').read_text(encoding='utf-8'))
                for i in range(201, 301)]
            errs = validate_ledgers(tmp_root, recs)
            self.assertTrue(any('BATCH_LEDGER_MISSING: batch05' in e for e in errs), errs)
