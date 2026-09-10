"""Read-only Gate 6 validator. --check requires exactly 500; checkpoints are explicit."""
import argparse
import json
import sys
from pathlib import Path
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.pipeline.corpus import validate


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--checkpoint', type=int, choices=range(1, 10))
    args = parser.parse_args()
    expected = 50 + 50 * args.checkpoint if args.checkpoint else 500
    try:
        errors = validate(ROOT, expected)
        from scripts.build_preview_data import build_preview_data, PREVIEW_DATA
        if json.loads(PREVIEW_DATA.read_text(encoding='utf-8')) != build_preview_data(ROOT):
            errors.append('PREVIEW_NOT_REPRODUCIBLE')
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors = [f'GATE6_SCHEMA: {exc}']
    print(f'GATE 6 {"CHECKPOINT" if args.checkpoint else "VALIDATION"}: {"FAIL" if errors else "PASS"}')
    for error in errors:
        print(error)
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())
