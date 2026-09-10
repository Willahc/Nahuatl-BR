"""Read-only encoding and reviewed-ledger checks; never repairs text."""
import csv
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


def ledger_errors(rows, recs):
    errors = []
    by_id = {r['lemma']['id']: r for r in recs}
    if len(rows) != 50:
        return ['BATCH_LEDGER_CANONICAL_DRIFT: batch04 row count']
    for n, row in enumerate(rows, 201):
        lid = f'L{n:04}'
        try:
            r = by_id[lid]
            actual = {
                'source_form': next(f['value'] for f in r['forms'] if f['layer'] == 'SOURCE_FORM'),
                'historical_gloss': r['attestations'][0]['original_gloss'],
                'pt_br': r['senses'][0]['translations'][0]['text'],
                'domain': r['review']['semantic_domain'],
                'page': str(r['gate6']['capture']['page_index_1based']),
                'column': r['gate6']['capture']['column'],
            }
            for field, value in actual.items():
                if row[field] != value:
                    errors.append(f'BATCH_LEDGER_CANONICAL_DRIFT: {lid}.{field}')
        except (KeyError, IndexError, StopIteration):
            errors.append(f'BATCH_LEDGER_CANONICAL_DRIFT: {lid} missing fields')
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


def validate_integrity(root, recs):
    errors = scan(root)
    if any(r['lemma']['id'] == 'L0201' for r in recs):
        with (root / 'data/gate6/batches/batch04.tsv').open(encoding='utf-8', newline='') as f:
            errors += ledger_errors(list(csv.DictReader(f, delimiter='\t')), recs)
        errors += numeral_errors(recs)
    return errors
