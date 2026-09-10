"""Read-only encoding and reviewed-ledger checks; never repairs text."""
import csv
import hashlib
import json
import unicodedata

SIGNATURES = ('\u00c3\u0192', '\u00c3\u201a', '\u00c2', '\u00e2\u20ac',
              '\u00c6\u2019', '\ufffd')
PATTERNS = ('data/gate6/batches/*.tsv', 'data/canonical/lemmas/*.json',
            'data/gate6/coverage.json', 'data/gate6/duplicate_candidates.json',
            'preview/public/data/nahuatl-br.json', 'docs/gate6/BATCH_*_REPORT.md')


def text_errors(value, path='$'):
    errors = []
    if isinstance(value, str):
        if (any(s in value for s in SIGNATURES) or
                any(unicodedata.category(c) == 'Cc' and c not in '\n\r\t' for c in value)):
            errors.append(f'TEXT_MOJIBAKE_DETECTED: {path}')
    elif isinstance(value, dict):
        for key, item in value.items():
            errors += text_errors(key, path + '.key')
            errors += text_errors(item, path + '.' + str(key))
    elif isinstance(value, list):
        for i, item in enumerate(value):
            errors += text_errors(item, f'{path}[{i}]')
    return errors


def scan(root):
    errors = []
    for pattern in PATTERNS:
        for path in sorted(root.glob(pattern)):
            try:
                value = path.read_text(encoding='utf-8')
                if path.suffix == '.json':
                    value = json.loads(value)
                errors += text_errors(value, path.relative_to(root).as_posix())
            except UnicodeDecodeError:
                errors.append(f'TEXT_MOJIBAKE_DETECTED: invalid UTF-8: {path}')
    return errors


# Declarative batch mapping for Gate 6 reviewed ledgers.
# Batches 01–03 were produced before this control was formalized.
# The mandatory ledger-canonical integrity check applies from Batch 04 onward.
BATCH_LEDGER_MAP = {
    b: {
        'batch': b,
        'batch_name': f'batch{b:02}',
        'start_id': (b) * 50 + 1,
        'end_id': (b + 1) * 50,
        'rel_path': f'data/gate6/batches/batch{b:02}.tsv',
    }
    for b in range(4, 10)
}


def ledger_errors(rows, recs, batch=4, ledger_sha=None):
    errors = []
    cfg = BATCH_LEDGER_MAP.get(batch, {
        'batch': batch,
        'batch_name': f'batch{batch:02}',
        'start_id': (batch) * 50 + 1,
        'end_id': (batch + 1) * 50,
        'rel_path': f'data/gate6/batches/batch{batch:02}.tsv',
    })
    batch_name = cfg['batch_name']
    start_id = cfg['start_id']
    by_id = {r['lemma']['id']: r for r in recs}
    if len(rows) != 50:
        return [f'BATCH_LEDGER_CANONICAL_DRIFT: {batch_name} row count']
    seen_hashes = set()
    for n, row in enumerate(rows, start_id):
        lid = f'L{n:04}'
        try:
            r = by_id[lid]
            capture = r.get('gate6', {}).get('capture', {})
            actual = {
                'source_form': next(f['value'] for f in r['forms'] if f['layer'] == 'SOURCE_FORM'),
                'historical_gloss': r['attestations'][0]['original_gloss'],
                'pt_br': r['senses'][0]['translations'][0]['text'],
                'domain': r['review']['semantic_domain'],
                'page': str(capture.get('page_index_1based', '')),
                'column': capture.get('column', ''),
            }
            for field in ('page', 'column', 'source_form', 'historical_gloss', 'pt_br', 'domain'):
                if row.get(field) != actual[field]:
                    errors.append(f'BATCH_LEDGER_CANONICAL_DRIFT: {batch_name} {lid} {field}')
            if 'image_sha256' in row and row['image_sha256']:
                if row['image_sha256'] != capture.get('sha256'):
                    errors.append(f'BATCH_LEDGER_CANONICAL_DRIFT: {batch_name} {lid} image_sha256')
            rec_hash = capture.get('reviewed_ledger_sha256')
            if ledger_sha is not None and rec_hash != ledger_sha:
                errors.append(f'REVIEWED_LEDGER_HASH_MISMATCH: {batch_name} {lid}')
            if rec_hash:
                seen_hashes.add(rec_hash)
        except (KeyError, IndexError, StopIteration):
            errors.append(f'BATCH_LEDGER_CANONICAL_DRIFT: {batch_name} {lid} missing fields')
    if len(seen_hashes) > 1:
        errors.append(f'REVIEWED_LEDGER_HASH_MISMATCH: {batch_name} conflicting_hashes')
    return errors


REVIEWED_NUMERALS = {
    'L0241': ('ſiete.', 'sete'),
    'L0242': ('ſiete coſas, pares, o partes.', 'sete coisas, pares ou partes'),
    'L0243': ('ſiete vezes.', 'sete vezes'),
}


def numeral_errors(recs):
    errors = []
    for r in recs:
        lid = r['lemma']['id']
        if lid in REVIEWED_NUMERALS:
            gloss, pt = REVIEWED_NUMERALS[lid]
            if (r['attestations'][0]['original_gloss'] != gloss or
                    r['senses'][0]['translations'][0]['text'] != pt):
                errors.append(f'REVIEWED_EDITORIAL_REGRESSION: {lid}')
    return errors


def validate_ledgers(root, recs):
    errors = []
    by_id = {r['lemma']['id']: r for r in recs}
    for b, cfg in sorted(BATCH_LEDGER_MAP.items()):
        batch_name = cfg['batch_name']
        start_id = cfg['start_id']
        end_id = cfg['end_id']
        batch_ids = [f'L{i:04}' for i in range(start_id, end_id + 1)]
        batch_recs = [by_id[lid] for lid in batch_ids if lid in by_id]
        if not batch_recs:
            continue
        ledger_file = root / cfg['rel_path']
        if not ledger_file.exists():
            errors.append(f'BATCH_LEDGER_MISSING: {batch_name}')
            continue
        try:
            content_bytes = ledger_file.read_bytes()
            ledger_sha = hashlib.sha256(content_bytes).hexdigest()
            with ledger_file.open(encoding='utf-8', newline='') as f:
                rows = list(csv.DictReader(f, delimiter='\t'))
            errors += ledger_errors(rows, batch_recs, batch=b, ledger_sha=ledger_sha)
        except UnicodeDecodeError:
            errors.append(f'TEXT_MOJIBAKE_DETECTED: invalid UTF-8: {ledger_file}')
    return errors


def validate_integrity(root, recs):
    errors = scan(root)
    errors += validate_ledgers(root, recs)
    errors += numeral_errors(recs)
    return errors
