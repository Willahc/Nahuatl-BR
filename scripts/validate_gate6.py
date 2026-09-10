"""Read-only Gate 6 validator with explicit and current-size checkpoints."""
import argparse
import json
import sys
from pathlib import Path
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.pipeline.corpus import validate


CHECKPOINT_BY_TOTAL = {100: 1, 150: 2, 200: 3, 250: 4, 300: 5,
                       350: 6, 400: 7, 450: 8, 500: 9}


def checkpoint_for_total(total):
    try:
        return CHECKPOINT_BY_TOTAL[total]
    except KeyError:
        raise ValueError(f'INVALID_GATE6_CHECKPOINT_SIZE: {total}') from None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--checkpoint', type=int, choices=range(1, 10))
    parser.add_argument('--check-current', action='store_true')
    args = parser.parse_args()
    if args.checkpoint and args.check_current:
        parser.error('--checkpoint and --check-current are mutually exclusive')
    if args.check_current:
        from src.pipeline.corpus import records
        current_total = len(records(ROOT))
        try:
            checkpoint = checkpoint_for_total(current_total)
        except ValueError as exc:
            print(f'GATE 6 CURRENT: FAIL\n{exc}')
            return True
        expected = current_total
    else:
        checkpoint = args.checkpoint
        expected = 50 + 50 * checkpoint if checkpoint else 500
    try:
        errors = validate(ROOT, expected)
        from src.pipeline.corpus import records
        from src.pipeline.text_integrity import validate_integrity
        errors += validate_integrity(ROOT, records(ROOT))
        from scripts.build_preview_data import build_preview_data, PREVIEW_DATA
        if json.loads(PREVIEW_DATA.read_text(encoding='utf-8')) != build_preview_data(ROOT):
            errors.append('PREVIEW_NOT_REPRODUCIBLE')
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors = [f'GATE6_SCHEMA: {exc}']
    mode = 'CURRENT' if args.check_current else ('CHECKPOINT' if args.checkpoint else 'VALIDATION')
    print(f'GATE 6 {mode}: {"FAIL" if errors else "PASS"}')
    if args.check_current:
        print(f'INFERRED_CHECKPOINT: {checkpoint}; TOTAL_LEMMAS: {expected}')
    for error in errors:
        print(error)
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())
