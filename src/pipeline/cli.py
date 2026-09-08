"""Command-line interface for the Gate 5 ingestion pipeline (read-only).

Usage:
    python -m src.pipeline.cli ingest <fixture.json|yml> --dry-run
    python -m src.pipeline.cli ingest-all [--root PATH]

The dry run never writes to data/pilot/ or any canonical store. Accepted
fixtures print the derived artifact JSON plus a digest; rejected fixtures print
the rejected stage/code and exit non-zero.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True

from .engine import IngestionEngine, run_fixture
from .loader import canonical_load


def load_fixture(path: Path) -> dict:
    try:
        data = canonical_load(path)
    except Exception as exc:
        raise RuntimeError(f"unreadable fixture {path.name}: {exc}") from exc
    if "ingest" not in data:
        raise RuntimeError(f"{path.name}: fixture has no ingest block")
    return data


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    ingest = sub.add_parser("ingest", help="run one ingestion fixture (dry run)")
    ingest.add_argument("fixture", type=Path)
    ingest.add_argument("--dry-run", action="store_true", default=True, help="read-only (always on)")

    allp = sub.add_parser("ingest-all", help="run every fixture under data/fixtures/gate5_ingestion_cases/")
    allp.add_argument("--root", type=Path, default=Path.cwd())
    allp.add_argument("--fixture-dir", type=Path, default=None)

    args = parser.parse_args(argv)
    root = Path(args.root if hasattr(args, "root") and args.root else Path.cwd())
    engine = IngestionEngine(root)

    if args.command == "ingest":
        fixture = load_fixture(args.fixture)
        result = run_fixture(engine, fixture)
        print(result.to_json())
        return 0 if result.outcome == "ACCEPT" else 1

    fixture_dir = args.fixture_dir or (root / "data" / "fixtures" / "gate5_ingestion_cases")
    failures = 0
    rejected = 0
    for path in sorted(fixture_dir.glob("*.yml")):
        try:
            fixture = load_fixture(path)
            result = run_fixture(engine, fixture)
        except Exception as exc:
            print(f"ERROR {path.name}: {exc}", file=sys.stderr)
            failures += 1
            continue
        status = "PASS" if result.outcome == "ACCEPT" else "REJECT"
        codes = ",".join(result.error_codes() or "-")
        print(f"{status} {path.name} [{codes}]")
        if result.outcome != "ACCEPT":
            rejected += 1
    print(f"RESULT: {rejected} rejected fixtures, {failures} load errors")
    return 1 if failures else 0


if __name__ == "__main__":
    try:
        code = main()
    except Exception as exc:
        print(f"PIPELINE ERROR: {exc}", file=sys.stderr)
        code = 1
    raise SystemExit(code)