"""Admit one visually captured 50-entry batch through Gate 5; no networking.

Input is a reviewed TSV of page/column/source_form/short historical gloss/PT-BR/
editorial domain. Image bytes are supplied outside Git and verified by checksum.
The default is dry-run. --write persists candidates only after full validation.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import sys
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.pipeline.corpus import derive_record, records, validate_record, duplicate_candidates, read, validate
from src.pipeline.engine import IngestionEngine


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('batch', type=int, choices=range(1, 10))
    parser.add_argument('--images', type=Path, required=True)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    existing = records(ROOT)
    expected_before = 50 * args.batch
    if len(existing) != expected_before:
        raise ValueError(f'batch order: expected {expected_before} existing records')
    if args.batch > 1:
        prior_errors = validate(ROOT, expected_before)
        if prior_errors:
            raise ValueError(prior_errors)
    path = ROOT / f'data/gate6/batches/batch{args.batch:02}.tsv'
    with path.open(encoding='utf-8', newline='') as handle:
        rows = list(csv.DictReader(handle, delimiter='\t'))
    if len(rows) != 50:
        raise ValueError(f'exactly 50 captures required, got {len(rows)}')
    canvases = read(args.images / 'manifest.json')['sequences'][0]['canvases']
    engine = IngestionEngine(ROOT)
    built = []
    for i, row in enumerate(rows, expected_before + 1):
        lid = f'L{i:04}'
        page = int(row['page'])
        canvas = canvases[page - 1]
        image_url = canvas['images'][0]['resource']['service']['@id'] + '/full/2000,/0/default.jpg'
        sha = hashlib.sha256((args.images / f'page-{page}.jpg').read_bytes()).hexdigest()
        locator = f'JCB 1571, part II, manifest page {page}, column {row["column"]}, headword {row["source_form"]}'
        request = {'case_id': f'G6-{lid}', 'ingest': {
            'lemma_id': lid, 'lemma_variety': 'Classical Nahuatl',
            'source_id': 'A01', 'component_id': 'jcb_1571_images', 'use': 'EVIDENCE_CAPTURE',
            'mediation_level': 'DIRECT_WITNESS', 'direct_witness_inspected': True,
            'edition': 'Mexico, Antonio de Spinosa, 1571; part II, mexicana-castellana',
            'witness': 'John Carter Brown Library, 1-SIZE B571 .M722v',
            'locator': locator, 'url': image_url, 'accessed_at': '2026-09-10',
            'declared_lossy': True,
            'entries': [{'source_form_id': lid + '-FS1', 'source_form': row['source_form'],
                         'original_gloss': row['historical_gloss']}],
            'claims': [
                {'predicate': 'has_historical_gloss', 'value': row['historical_gloss'],
                 'modality': 'OBSERVED', 'confidence': 'MEDIUM'},
                {'predicate': 'has_pt_br_editorial_gloss', 'value': row['pt_br'],
                 'modality': 'EDITORIAL', 'confidence': 'MEDIUM'}]}}
        capture = {'canvas_id': canvas['@id'], 'page_index_1based': page,
                   'image_url': image_url, 'sha256': sha, 'column': row['column'],
                   'inspection': 'VISUALLY_INSPECTED', 'inspector': 'EXECUTION_AGENT',
                   'attribution': 'Courtesy of the John Carter Brown Library',
                   'license': 'CC BY 4.0', 'rights_url': 'https://jcblibrary.org/permissions/',
                   'transcription_convention': 'Headword glyphs preserved; terminal separator excluded. '
                       'Short contiguous historical gloss; line breaks joined as spaces. '
                       'No morphological expansion or historical spelling modernization.',
                   'confidence_rationale': 'Legible selected headword/gloss in image; single witness '
                       'and editorial translation require independent semantic review.'}
        rec = derive_record(request, capture, args.batch, row['domain'], ROOT)
        errors = validate_record(rec, engine)
        if errors:
            raise ValueError(errors)
        built.append(rec)
    collisions = duplicate_candidates(existing + built)
    if args.write:
        for rec in built:
            out = ROOT / f'data/canonical/lemmas/{rec["lemma"]["id"]}.json'
            if out.exists():
                raise ValueError('never overwrite canonical lemma')
            out.write_text(json.dumps(rec, ensure_ascii=False, indent=2, sort_keys=True) + '\n', encoding='utf-8')
        (ROOT / 'data/gate6/duplicate_candidates.json').write_text(
            json.dumps(collisions, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'BATCH {args.batch:02}: 50 accepted; total {expected_before + 50}; '
          f'{len(collisions)} duplicate candidates; mode {"WRITE" if args.write else "DRY_RUN"}')


if __name__ == '__main__':
    main()
