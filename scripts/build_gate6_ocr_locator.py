"""Build an OCR-only discovery queue; never writes canonical lemmas or Evidence."""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / 'build/gate6/locator_candidates.json'
HEADWORD = re.compile(r'^\s*([A-Za-zſꝑꝛ][A-Za-zſꝑꝛ-]{2,})\s*[.]')


def build(text: str, page_numbers: dict | None = None) -> dict:
    # Page markers vary by ABBYY export; retain line index when no mapping exists.
    part_two = bool(re.search(r'vocabulario\s+en\s+lengua\s+mexicana\s+y\s+castellana', text, re.I))
    candidates = []
    page = 0
    for index, line in enumerate(text.splitlines()):
        if line.startswith('\x0c'):
            page += 1
        match = HEADWORD.match(line)
        if not match or len(match.group(1)) < 3:
            continue
        headword = match.group(1)
        # OCR candidates deliberately retain the raw line and technical locator.
        candidate_id = 'OCR-' + hashlib.sha256(f'{index}|{headword}|{page}'.encode()).hexdigest()[:16]
        candidates.append({
            'candidate_id': candidate_id,
            'ocr_headword_candidate': headword,
            'ocr_gloss_candidate': line[match.end():].strip(),
            'ocr_page_index': page or None,
            'page_mapping': (page_numbers or {}).get(str(page), page or None),
            'ocr_line_index': index,
            'confidence_technical': 'UNASSESSED',
            'needs_visual_verification': True,
            'direct_witness_inspected': False,
            'evidence_eligible': False,
            'provenance': {'source': 'IA_OCR', 'role': 'locator_assist'},
        })
    return {'schema': 'gate6-ocr-locator-v1', 'source': 'A01',
            'identifier': 'vocabularioenlen00moli', 'part_ii_detected': part_two,
            'ocr_role': 'LOCATOR_ASSIST_ONLY', 'candidates': candidates}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--page-numbers', type=Path)
    parser.add_argument('--output', type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    text = args.input.read_text(encoding='utf-8-sig')
    page_numbers = json.loads(args.page_numbers.read_text(encoding='utf-8')) if args.page_numbers else None
    result = build(text, page_numbers)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    print(f"OCR LOCATOR: {len(result['candidates'])} candidates; no canonical records written")


if __name__ == '__main__':
    main()
