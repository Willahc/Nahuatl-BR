"""Gate 6 canonical catalog and checks, using the approved ingestion engine.

The catalog references the immutable pilot; only new records live in canonical/.
No network, writes, linguistic inference or automatic merge occurs here.
"""
from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

from .engine import IngestionEngine

BASE_COMMIT = '1efd8d0d9e6510e335dbedb8d289cd22dcde8557'
TARGET = 500


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def semantic_hash(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                     separators=(',', ':')).encode()).hexdigest()


def pilot_paths(root):
    return sorted((root / 'data/pilot/lemmas').glob('*.yml'))


def records(root):
    paths = pilot_paths(root) + sorted((root / 'data/canonical/lemmas').glob('*.json'))
    return [read(p) for p in paths]


def record_id(rec):
    return rec['lemma']['id']


def duplicate_candidates(recs):
    """Candidate pairs with explicit reasons; equality is never identity."""
    indexes = {k: {} for k in ['SOURCE_FORM', 'NORMALIZED_FORM', 'SEARCH_KEY', 'SENSE_TEXT']}
    for rec in recs:
        lid = record_id(rec)
        for form in rec.get('forms', []):
            layer, value = form['layer'], form['value']
            if layer in indexes and isinstance(value, str):
                indexes[layer].setdefault(value, set()).add(lid)
        for sense in rec.get('senses', []):
            value = sense.get('interpretation')
            if isinstance(value, str) and value not in {'UNKNOWN', 'NOT_REVIEWED'}:
                indexes['SENSE_TEXT'].setdefault(value, set()).add(lid)
    pairs = {}
    for reason, index in indexes.items():
        for value, ids in sorted(index.items()):
            for pair in itertools.combinations(sorted(ids), 2):
                pairs.setdefault(pair, []).append({'field': reason, 'value': value})
    by_id = {record_id(rec): rec for rec in recs}
    report = []
    for pair, reasons in sorted(pairs.items()):
        forms = {lid: {f['layer']: f['value'] for f in by_id[lid].get('forms', [])}
                 for lid in pair}
        glosses = {lid: [a.get('original_gloss', '') for a in by_id[lid].get('attestations', [])]
                   for lid in pair}
        report.append({
            'lemma_ids': list(pair),
            'source_forms': {lid: forms[lid].get('SOURCE_FORM', '') for lid in pair},
            'normalized_forms': {lid: forms[lid].get('NORMALIZED_FORM', '') for lid in pair},
            'search_keys': {lid: forms[lid].get('SEARCH_KEY', '') for lid in pair},
            'historical_glosses': glosses,
            'reason': reasons,
            'reasons': reasons,
            'identity_status': 'LEXICAL_IDENTITY_UNRESOLVED',
            'status': 'CANDIDATE_ONLY',
            'automatic_merge': False,
        })
    return report


def audit_ids(recs):
    return sorted((record_id(r) for r in recs),
                  key=lambda lid: hashlib.sha256((lid + 'gate6-audit-v1').encode()).hexdigest())[:50]


def derive_record(request, capture, batch, domain, root):
    """Explicit canonical adapter. All linguistic candidates pass Gate 5 first."""
    result = IngestionEngine(root).ingest(request)
    if result.outcome != 'ACCEPT':
        raise ValueError(result.to_json())
    artifact = result.artifacts
    lid = request['ingest']['lemma_id']
    claims = artifact['claims']
    editorial = [c for c in claims if c['predicate'] == 'has_pt_br_editorial_gloss']
    if len(editorial) != 1:
        raise ValueError('one explicit editorial translation candidate required')
    claim = editorial[0]
    evs = [e['evidence_id'] for e in artifact['evidence']]
    source = request['ingest']['entries'][0]
    forms = [{'form_id': source['source_form_id'], 'layer': 'SOURCE_FORM',
              'value': source['source_form'], 'evidence': evs,
              'normalization_profile': 'NOT_APPLICABLE'}]
    forms += artifact['forms'] + artifact['search_keys']
    translation = {'translation_id': lid + '-T1', 'language': 'pt-BR',
                   'text': json.loads(claim['value']), 'modality': claim['modality'],
                   'editorial_state': claim['editorial_state'], 'derived_from': evs,
                   'confidence': claim['confidence'], 'claim_id': claim['claim_id'],
                   'editorial_provenance': claim['editorial_provenance']}
    return {
        'schema': 'nahuatl-br-gate6-canonical-v1',
        'lemma': {'id': lid, 'display_form': source['source_form'],
                  'variety': request['ingest']['lemma_variety'], 'status': 'DRAFT'},
        'forms': forms, 'attestations': artifact['attestations'],
        'evidence': artifact['evidence'], 'claims': claims,
        'evidence_links': artifact['evidence_links'],
        'senses': [{'sense_id': lid + '-S1', 'original_gloss': source['original_gloss'],
                    'interpretation': translation['text'], 'editorial_status': 'DRAFT',
                    'translations': [translation]}],
        'phonological_information': {'vowel_length': 'UNKNOWN', 'saltillo': 'UNKNOWN',
                                    'status': 'NOT_REVIEWED'},
        'morphology': {'status': 'NOT_REVIEWED'}, 'corpus_references': [],
        'review': {'coverage_status': 'SINGLE_SOURCE',
                   'semantic_status': 'NEEDS_SEMANTIC_REVIEW',
                   'lexical_class': 'NOT_REVIEWED', 'semantic_domain': domain,
                   'domain_modality': 'EDITORIAL', 'automatic_merge': False},
        'gate6': {'batch': batch, 'request': request, 'pipeline_digest': result.digest,
                  'capture': capture},
        'notes': 'Selective visual transcription of a historical entry; Portuguese is an editorial DRAFT. '
                 'Courtesy of the John Carter Brown Library (CC BY 4.0). '
                 'No phonology or morphology inferred; source headword is preserved. '
                 'A selected historical gloss may not exhaust the entry or its senses.',
    }


def validate_record(rec, engine):
    errors = []
    lid = rec.get('lemma', {}).get('id', '?')
    def fail(code):
        errors.append(f'{code}: {lid}')
    if rec.get('lemma', {}).get('variety') != 'Classical Nahuatl':
        fail('MODERN_AS_CLASSICAL_EVIDENCE')
    if not rec.get('attestations'):
        fail('HISTORICAL_ATTESTATION_REQUIRED')
    evs = {e.get('evidence_id') for e in rec.get('evidence', [])}
    forms = rec.get('forms', [])
    source_forms = [f for f in forms if f.get('layer') == 'SOURCE_FORM']
    if not source_forms or any(not f.get('value', '').strip() for f in source_forms):
        fail('SOURCE_FORM_REQUIRED')
    for a in rec.get('attestations', []):
        if not a.get('locator') or a['locator'] in {'UNKNOWN', 'NOT_RECORDED'}:
            fail('LOCATOR_REQUIRED')
    for c in rec.get('claims', []):
        if c.get('editorial_state') != 'DRAFT':
            fail('NEW_CLAIM_NOT_DRAFT')
        if not c.get('evidence') or any(e not in evs for e in c['evidence']):
            fail('UNRESOLVED_EVIDENCE')
        if c.get('predicate') == 'has_pt_br_editorial_gloss' and c.get('modality') != 'EDITORIAL':
            fail('EDITORIAL_TRANSLATION_REQUIRED')
    translations = [t for s in rec.get('senses', []) for t in s.get('translations', [])
                    if t.get('language') == 'pt-BR']
    if not translations:
        fail('PT_BR_REQUIRED')
    for t in translations:
        if t.get('modality') != 'EDITORIAL' or t.get('editorial_state') != 'DRAFT':
            fail('EDITORIAL_TRANSLATION_REQUIRED')
        if not t.get('text') or not t.get('editorial_provenance') or not t.get('derived_from'):
            fail('EDITORIAL_PROVENANCE_REQUIRED')
        if any(e not in evs for e in t.get('derived_from', [])):
            fail('UNRESOLVED_EVIDENCE')
    phon = rec.get('phonological_information', {})
    if phon.get('vowel_length') != 'UNKNOWN':
        fail('AUTO_VOWEL_LENGTH')
    if phon.get('saltillo') != 'UNKNOWN':
        fail('AUTO_SALTILLO')
    if any('ipa' in k.lower() for k in phon):
        fail('AUTO_IPA')
    if rec.get('review', {}).get('automatic_merge') is not False:
        fail('SEARCH_KEY_AUTO_MERGE')
    g6 = rec.get('gate6', {})
    request = g6.get('request', {})
    ing = request.get('ingest', {})
    # Scope-specific layer allowlist: cannot launder GDN or a restricted
    # surrogate through the public-domain status of the underlying Work.
    if (ing.get('source_id'), ing.get('component_id')) != ('A01', 'jcb_1571_images'):
        fail('SCALE_ACCESS_LAYER_NOT_APPROVED')
    if ing.get('lemma_id') != lid or ing.get('use') != 'EVIDENCE_CAPTURE':
        fail('CAPTURE_IDENTITY')
    capture = g6.get('capture', {})
    if capture.get('provenance_source') in {'IA_OCR', 'ABBYY', 'DJVU_TEXT', 'HOCR'}:
        fail('OCR_NOT_LINGUISTIC_EVIDENCE')
    if capture.get('ocr_only') is True or capture.get('technical_role') == 'LOCATOR_ASSIST_ONLY':
        fail('OCR_NOT_LINGUISTIC_EVIDENCE')
    required = ['image_url', 'canvas_id', 'sha256', 'attribution', 'column', 'inspection']
    if any(not capture.get(k) for k in required) or capture.get('inspection') != 'VISUALLY_INSPECTED':
        fail('WITNESS_INSPECTION_REQUIRED')
    try:
        replay = engine.ingest(request)
        if replay.outcome != 'ACCEPT':
            errors += [f'{e.code}: {lid}' for e in replay.errors]
        elif replay.digest != g6.get('pipeline_digest'):
            fail('PIPELINE_REPLAY_MISMATCH')
        else:
            a = replay.artifacts
            for field in ['attestations', 'evidence', 'claims', 'evidence_links']:
                if rec.get(field) != a[field]:
                    fail('PIPELINE_ARTIFACT_MUTATION_' + field.upper())
            if forms[1:] != a['forms'] + a['search_keys']:
                fail('HIDDEN_TRANSFORMATION')
            entries = ing.get('entries', [])
            if len(source_forms) != 1 or len(entries) != 1 or source_forms[0]['value'] != entries[0]['source_form']:
                fail('SOURCE_FORM_MUTATION')
            for t in translations:
                c = next((c for c in a['claims'] if c['claim_id'] == t.get('claim_id')), {})
                if (t.get('text') != json.loads(c.get('value', 'null')) or
                        t.get('derived_from') != c.get('evidence')):
                    fail('TRANSLATION_DERIVATION')
    except (KeyError, TypeError, ValueError, AttributeError):
        fail('CAPTURE_SCHEMA')
    return errors


def validate(root, expected=TARGET, check_derived=True):
    errors = []
    baseline = read(root / 'data/gate6/baseline.json')
    if baseline.get('commit') != BASE_COMMIT:
        errors.append('GATE3_CORPUS_REGRESSION: baseline commit')
    paths = pilot_paths(root)
    actual = {p.relative_to(root).as_posix(): semantic_hash(read(p)) for p in paths}
    if actual != baseline['semantic_sha256']:
        errors.append('GATE3_CORPUS_REGRESSION: baseline files changed')
    recs = records(root)
    ids = [record_id(r) for r in recs]
    if len(recs) != expected:
        errors.append(f'CORPUS_COUNT: expected {expected}, found {len(recs)}')
    if len(set(ids)) != len(ids):
        errors.append('DUPLICATE_LEMMA_ID')
    if set(ids) != {f'L{i:04}' for i in range(1, expected + 1)}:
        errors.append('CORPUS_IDS')
    if len(recs) - len(paths) != expected - 50:
        errors.append('NEW_LEMMAS_COUNT')
    engine = IngestionEngine(root)
    for rec in recs[len(paths):]:
        errors += validate_record(rec, engine)
    # Baseline attestations and Claims remain under the unchanged Gate 3 validator.
    if check_derived:
        wanted = duplicate_candidates(recs)
        if read(root / 'data/gate6/duplicate_candidates.json') != wanted:
            errors.append('DUPLICATE_REPORT_DRIFT')
        if expected == TARGET and read(root / 'data/gate6/audit_sample.json')['lemma_ids'] != audit_ids(recs):
            errors.append('AUDIT_SAMPLE_DRIFT')
    return errors
