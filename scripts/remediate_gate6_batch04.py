"""Rebuild only Batch 04 via Gate 5 from visually reviewed UTF-8 ledger.

Default is read-only. Requires the inspected local JCB image; never decodes or
repairs corrupted strings. Writes occur only after all 50 records validate.
"""
import argparse
import copy
import csv
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.pipeline.corpus import derive_record, read, validate_record, duplicate_candidates, records
from src.pipeline.engine import IngestionEngine
from src.pipeline.text_integrity import text_errors, ledger_errors, numeral_errors

ROOT = Path(__file__).resolve().parents[1]


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--image', type=Path, required=True)
    p.add_argument('--write', action='store_true')
    args = p.parse_args()
    ledger = ROOT / 'data/gate6/batches/batch04.tsv'
    with ledger.open(encoding='utf-8', newline='') as f:
        rows = list(csv.DictReader(f, delimiter='\t'))
    if len(rows) != 50 or text_errors(rows):
        raise ValueError('Invalid reviewed ledger')
    sha = hashlib.sha256(args.image.read_bytes()).hexdigest()
    engine = IngestionEngine(ROOT)
    rebuilt = []
    for i, row in enumerate(rows, 201):
        lid = f'L{i:04}'
        old = read(ROOT / f'data/canonical/lemmas/{lid}.json')
        request = copy.deepcopy(old['gate6']['request'])
        ing = request['ingest']
        capture = copy.deepcopy(old['gate6']['capture'])
        if sha != capture['sha256'] or row['page'] != '300':
            raise ValueError('JCB image hash/page mismatch')
        ing['locator'] = f'JCB 1571, part II, manifest page 300, column {row["column"]}, headword {row["source_form"]}'
        ing['entries'][0]['source_form'] = row['source_form']
        ing['entries'][0]['original_gloss'] = row['historical_gloss']
        for claim in ing['claims']:
            claim['value'] = row['pt_br'] if claim['predicate'] == 'has_pt_br_editorial_gloss' else row['historical_gloss']
        capture.update(column=row['column'], inspected_at='2026-09-10',
                       inspection_method='VISUAL_RECHECK_JCB_PAGE_300',
                       reviewed_ledger_sha256=hashlib.sha256(ledger.read_bytes()).hexdigest())
        capture['transcription_convention'] = (
            'Visual transcription; historical spelling, spaces and long s preserved. '
            'Typographic ct ligatures represented by c + t; entry separators excluded '
            'from headwords. Glosses are short contiguous excerpts; line wrapping '
            'and line-end hyphenation joined. No inferred expansion of abbreviations.')
        record = derive_record(request, capture, 4, row['domain'], ROOT)
        errors = validate_record(record, engine)
        if errors:
            raise ValueError(errors)
        rebuilt.append(record)
    errors = ledger_errors(rows, rebuilt) + numeral_errors(rebuilt)
    if errors:
        raise ValueError(errors)
    if args.write:
        for rec in rebuilt:
            (ROOT / f'data/canonical/lemmas/{rec["lemma"]["id"]}.json').write_text(
                json.dumps(rec, ensure_ascii=False, indent=2, sort_keys=True) + '\n', encoding='utf-8')
        (ROOT / 'data/gate6/duplicate_candidates.json').write_text(
            json.dumps(duplicate_candidates(records(ROOT)), ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'BATCH04_REBUILD: PASS; 50 records; write={args.write}')


if __name__ == '__main__':
    main()
